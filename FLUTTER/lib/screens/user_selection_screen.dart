import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:geolocator/geolocator.dart';
import '../models/allergy_profile_request.dart';
import '../models/allergy_classification_response.dart';
import '../models/prediction_response.dart';
import '../services/user_storage_service.dart';
import '../services/allergy_classification_service.dart';
import 'detailed_profile_form_screen.dart';
import 'prediction_result_screen.dart';
import 'allergy_classification_result_screen.dart';

class UserSelectionScreen extends StatefulWidget {
  const UserSelectionScreen({super.key});

  @override
  State<UserSelectionScreen> createState() => _UserSelectionScreenState();
}

class _UserSelectionScreenState extends State<UserSelectionScreen> with WidgetsBindingObserver {
  bool _isLoading = true;
  bool _hasExistingProfile = false;
  AllergyProfileRequest? _userRequest;
  AllergyClassificationResponse? _lastClassification;
  PredictionResponse? _lastPrediction;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    _checkExistingProfile();
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    super.dispose();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    super.didChangeAppLifecycleState(state);
    if (state == AppLifecycleState.resumed) {
      // Refresh data when app comes to foreground
      _checkExistingProfile();
    }
  }

  Future<void> _checkExistingProfile() async {
    setState(() {
      _isLoading = true;
    });

    try {
      final hasProfile = await UserStorageService.hasUserProfile();
      
      if (hasProfile) {
        final userPreferenceId = await UserStorageService.getUserPreferenceId();
        
        if (userPreferenceId != null) {
          // Try to get user profile from API
          try {
            // Get user data from storage
            final userRequest = await UserStorageService.getUserRequest();
            final lastClassification = await UserStorageService.getLastClassification();
            final lastPrediction = await UserStorageService.getLastPrediction();
            
            setState(() {
              _hasExistingProfile = true;
              _userRequest = userRequest;
              _lastClassification = lastClassification;
              _lastPrediction = lastPrediction;
            });
            
            return; // Exit early on success
          } catch (e) {
            // If API call fails, we might have local data
            final userRequest = await UserStorageService.getUserRequest();
            final lastClassification = await UserStorageService.getLastClassification();
            final lastPrediction = await UserStorageService.getLastPrediction();
            
            if (userRequest != null && lastClassification != null) {
              setState(() {
                _hasExistingProfile = true;
                _userRequest = userRequest;
                _lastClassification = lastClassification;
                _lastPrediction = lastPrediction;
              });
              
              return; // Exit early on success
            }
          }
        } else {
          // Check for local data even without userPreferenceId
          final userRequest = await UserStorageService.getUserRequest();
          final lastClassification = await UserStorageService.getLastClassification();
          final lastPrediction = await UserStorageService.getLastPrediction();
          
          if (userRequest != null && lastClassification != null) {
            setState(() {
              _hasExistingProfile = true;
              _userRequest = userRequest;
              _lastClassification = lastClassification;
              _lastPrediction = lastPrediction;
            });
            
            return; // Exit early on success
          }
        }
      }
      
      // Only set to false if no profile data found
      setState(() {
        _hasExistingProfile = false;
      });
      
    } catch (e) {
      setState(() {
        _hasExistingProfile = false;
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  Future<void> _navigateToProfileForm() async {
    final result = await Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => DetailedProfileFormScreen(
          existingRequest: _userRequest,
          isEditing: _hasExistingProfile && _userRequest != null,
        ),
      ),
    );
    
    // Refresh data when returning from profile form
    if (result == true || result == null) {
      await _checkExistingProfile();
    }
  }

  Future<void> _makePrediction() async {
    try {
      setState(() {
        _isLoading = true;
      });

      // Get current location
      Position position = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
      );

      // Get user preference ID
      final userPreferenceId = await UserStorageService.getUserPreferenceId();
      
      if (userPreferenceId == null) {
        throw Exception('Kullanıcı profili bulunamadı. Lütfen önce profil oluşturun.');
      }

      // Make prediction API call
      final prediction = await AllergyClassificationService.getPrediction(
        latitude: position.latitude,
        longitude: position.longitude,
        userId: userPreferenceId,
      );

      if (mounted) {
        // Parse the prediction response
        final predictionResponse = PredictionResponse.fromJson(prediction);
        
        // Save prediction results to local storage
        await UserStorageService.saveLastPrediction(prediction);
        
        // Update local state to refresh UI immediately
        setState(() {
          _lastPrediction = predictionResponse;
        });
        
        // Show prediction results
        _showPredictionResults(prediction);
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Tahmin hatası: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  void _showPredictionResults(Map<String, dynamic> prediction) {
    try {
      // Debug print - JSON'u console'a yazdır
      print('🔍 Received prediction JSON:');
      print(prediction);
      
      // Parse the prediction response
      final predictionResponse = PredictionResponse.fromJson(prediction);
      
      // Navigate to the detailed prediction result screen
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => PredictionResultScreen(
            predictionResponse: predictionResponse,
          ),
        ),
      );
    } catch (e, stackTrace) {
      // Enhanced error handling with detailed logging
      print('❌ JSON Parsing Error: $e');
      print('📋 Stack Trace: $stackTrace');
      print('📄 Raw JSON: $prediction');
      
      // Show error dialog with more details
      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          title: const Text('Parsing Hatası'),
          content: SingleChildScrollView(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Hata: $e'),
                const SizedBox(height: 16),
                const Text(
                  'Raw JSON Data:',
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 8),
                Container(
                  padding: const EdgeInsets.all(8),
                  decoration: BoxDecoration(
                    color: Colors.grey.shade100,
                    borderRadius: BorderRadius.circular(4),
                  ),
                  child: Text(
                    prediction.toString(),
                    style: const TextStyle(
                      fontFamily: 'monospace',
                      fontSize: 12,
                    ),
                  ),
                ),
              ],
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Tamam'),
            ),
          ],
        ),
      );
    }
  }

  Future<void> _navigateToDetailedResults() async {
    // Always fetch the latest prediction data before navigating
    try {
      final lastPrediction = await UserStorageService.getLastPrediction();
      
      if (lastPrediction != null) {
        if (mounted) {
          final result = await Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => PredictionResultScreen(
                predictionResponse: lastPrediction,
              ),
            ),
          );
          
          // Refresh data when returning from detailed results
          if (result == true || result == null) {
            await _checkExistingProfile();
          }
        }
      } else {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('Risk analizi sonucu bulunamadı. Lütfen önce "Risk Analizi Başlat" butonuna tıklayın.'),
              backgroundColor: Colors.orange,
            ),
          );
        }
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Hata: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  Future<void> _navigateToAllergyReport() async {
    try {
      final userRequest = await UserStorageService.getUserRequest();
      final lastClassification = await UserStorageService.getLastClassification();
      
      if (lastClassification != null && userRequest != null) {
        if (mounted) {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => AllergyClassificationResultScreen(
                response: lastClassification,
                request: userRequest,
              ),
            ),
          );
        }
      } else {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('Alerji analiz sonucu bulunamadı. Lütfen önce profil oluşturun.'),
              backgroundColor: Colors.orange,
            ),
          );
        }
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Hata: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  String _formatTimestamp(String timestamp) {
    try {
      final dateTime = DateTime.parse(timestamp);
      final now = DateTime.now();
      final difference = now.difference(dateTime);
      
      if (difference.inMinutes < 1) {
        return 'Az önce';
      } else if (difference.inMinutes < 60) {
        return '${difference.inMinutes} dakika önce';
      } else if (difference.inHours < 24) {
        return '${difference.inHours} saat önce';
      } else if (difference.inDays < 7) {
        return '${difference.inDays} gün önce';
      } else {
        // Format as date for older entries
        return '${dateTime.day}/${dateTime.month}/${dateTime.year} ${dateTime.hour.toString().padLeft(2, '0')}:${dateTime.minute.toString().padLeft(2, '0')}';
      }
    } catch (e) {
      return 'Zaman bilinmiyor';
    }
  }

  void _exitApp() async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Uygulamadan Çık'),
        content: const Text('Uygulamadan çıkmak istediğinizden emin misiniz?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('İptal'),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context, true),
            style: TextButton.styleFrom(foregroundColor: Colors.red),
            child: const Text('Çık'),
          ),
        ],
      ),
    );

    if (confirmed == true) {
      try {
        // Close the app - works on Android
        await SystemNavigator.pop();
      } catch (e) {
        // If SystemNavigator.pop() doesn't work, try alternative approach
        if (Navigator.of(context).canPop()) {
          Navigator.of(context).pop();
        }
      }
    }
  }

  void _clearUserData() async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Profil Sil'),
        content: const Text('Mevcut profilinizi silmek istediğinizden emin misiniz? Bu işlem geri alınamaz.'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('İptal'),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context, true),
            style: TextButton.styleFrom(foregroundColor: Colors.red),
            child: const Text('Sil'),
          ),
        ],
      ),
    );

    if (confirmed == true) {
      await UserStorageService.clearUserData();
      setState(() {
        _hasExistingProfile = false;
        _userRequest = null;
        _lastClassification = null;
        _lastPrediction = null;
      });
      
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Profil başarıyla silindi'),
          backgroundColor: Colors.green,
        ),
      );
    }
  }

  Widget _buildRecommendationItem(String title, String description, IconData icon) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Icon(
          icon,
          color: Colors.green.shade600,
          size: 18,
        ),
        const SizedBox(width: 8),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title,
                style: TextStyle(
                  fontSize: 13,
                  fontWeight: FontWeight.w600,
                  color: Colors.green.shade800,
                ),
              ),
              Text(
                description,
                style: TextStyle(
                  fontSize: 12,
                  color: Colors.grey.shade700,
                  height: 1.3,
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'AllerMind',
          style: TextStyle(
            fontSize: 26,
            fontWeight: FontWeight.bold,
            letterSpacing: 0.5,
          ),
        ),
        backgroundColor: Colors.teal,
        foregroundColor: Colors.white,
        elevation: 2,
        leading: IconButton(
          icon: const Icon(Icons.notifications_outlined),
          onPressed: () {
            // TODO: Implement notifications screen
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(
                content: Text('Bildirimler yakında aktif olacak'),
                backgroundColor: Colors.orange,
              ),
            );
          },
        ),
        actions: [
          PopupMenuButton<String>(
            icon: const Icon(
              Icons.account_circle,
              size: 28,
            ),
            onSelected: (value) {
              switch (value) {
                case 'profile':
                  _navigateToProfileForm();
                  break;
                case 'report':
                  _navigateToAllergyReport();
                  break;
                case 'data':
                  _clearUserData();
                  break;
                case 'logout':
                  _exitApp();
                  break;
              }
            },
            itemBuilder: (context) => [
              if (_hasExistingProfile)
                const PopupMenuItem(
                  value: 'profile',
                  child: Row(
                    children: [
                      Icon(Icons.edit, color: Colors.blue),
                      SizedBox(width: 8),
                      Text('Profil Güncelle'),
                    ],
                  ),
                ),
              if (_hasExistingProfile && _lastClassification != null)
                const PopupMenuItem(
                  value: 'report',
                  child: Row(
                    children: [
                      Icon(Icons.analytics, color: Colors.teal),
                      SizedBox(width: 8),
                      Text('Alerji Raporu Görüntüle'),
                    ],
                  ),
                ),
              if (_hasExistingProfile)
                const PopupMenuItem(
                  value: 'data',
                  child: Row(
                    children: [
                      Icon(Icons.delete_forever, color: Colors.orange),
                      SizedBox(width: 8),
                      Text('Profili Kaldır'),
                    ],
                  ),
                ),
              const PopupMenuItem(
                value: 'logout',
                child: Row(
                  children: [
                    Icon(Icons.logout, color: Colors.red),
                    SizedBox(width: 8),
                    Text('Güvenli Çıkış Yap'),
                  ],
                ),
              ),
            ],
          ),
        ],
      ),
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [
              Color(0xFFF5F5F5),
              Color(0xFFE0E0E0),
            ],
          ),
        ),
        child: _isLoading 
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: _checkExistingProfile,
              child: SingleChildScrollView(
                padding: const EdgeInsets.all(16.0),
                physics: const AlwaysScrollableScrollPhysics(),
                child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Status Overview Card
                  Card(
                    elevation: 6,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: Container(
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(16),
                        gradient: LinearGradient(
                          begin: Alignment.topLeft,
                          end: Alignment.bottomRight,
                          colors: [
                            Colors.teal.shade50,
                            Colors.white,
                          ],
                        ),
                      ),
                      child: Padding(
                        padding: const EdgeInsets.all(18.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              children: [
                                Container(
                                  padding: const EdgeInsets.all(6),
                                  decoration: BoxDecoration(
                                    color: Colors.teal.shade100,
                                    borderRadius: BorderRadius.circular(10),
                                  ),
                                  child: Icon(
                                    Icons.shield,
                                    size: 22,
                                    color: Colors.teal.shade700,
                                  ),
                                ),
                                const SizedBox(width: 12),
                                const Expanded(
                                  child: Text(
                                    'Klinik Durum Özeti',
                                    style: TextStyle(
                                      fontSize: 20,
                                      fontWeight: FontWeight.bold,
                                      color: Colors.teal,
                                      letterSpacing: 0.2,
                                    ),
                                  ),
                                ),
                              ],
                            ),
                            const SizedBox(height: 14),
                            Text(
                              _hasExistingProfile 
                                ? 'Profilinizdeki mevcut verilere göre alerjik durumunuzun kısa bir özeti sunulmaktadır.'
                                : 'Kişiselleştirilmiş alerji risk analizi için detaylı klinik profilinizi oluşturun ve güncel sağlık durumunuzu değerlendirin.',
                              style: TextStyle(
                                fontSize: 14,
                                height: 1.4,
                                color: Colors.grey.shade700,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                  
                  const SizedBox(height: 16),

                  // Clinical Analysis Report Card (only show if user has existing profile)
                  if (_hasExistingProfile) ...[
                    Card(
                      elevation: 5,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(16),
                      ),
                      child: Container(
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(16),
                          border: Border.all(
                            color: Colors.blue.shade100,
                            width: 1,
                          ),
                        ),
                        child: Padding(
                          padding: const EdgeInsets.all(16.0),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              InkWell(
                                onTap: _lastPrediction != null ? () => _navigateToDetailedResults() : null,
                                borderRadius: BorderRadius.circular(12),
                                child: Container(
                                  padding: const EdgeInsets.all(12),
                                  decoration: BoxDecoration(
                                    color: _lastPrediction != null ? Colors.blue.shade50 : Colors.grey.shade100,
                                    borderRadius: BorderRadius.circular(12),
                                    border: Border.all(
                                      color: _lastPrediction != null ? Colors.blue.shade200 : Colors.grey.shade300,
                                      width: 1,
                                    ),
                                  ),
                                  child: Row(
                                    children: [
                                      Container(
                                        padding: const EdgeInsets.all(8),
                                        decoration: BoxDecoration(
                                          color: _lastPrediction != null ? Colors.blue.shade100 : Colors.grey.shade200,
                                          borderRadius: BorderRadius.circular(10),
                                        ),
                                        child: Icon(
                                          Icons.medical_services,
                                          color: _lastPrediction != null ? Colors.blue.shade700 : Colors.grey.shade600,
                                          size: 24,
                                        ),
                                      ),
                                      const SizedBox(width: 12),
                                      Expanded(
                                        child: Column(
                                          crossAxisAlignment: CrossAxisAlignment.start,
                                          children: [
                                            Text(
                                              'Son Analiz Raporu',
                                              style: TextStyle(
                                                fontSize: 18,
                                                fontWeight: FontWeight.w700,
                                                color: _lastPrediction != null ? Colors.blue : Colors.grey.shade600,
                                                letterSpacing: 0.2,
                                              ),
                                            ),
                                            if (_lastPrediction != null) ...[
                                              const SizedBox(height: 4),
                                              Text(
                                                _formatTimestamp(_lastPrediction!.modelPrediction.timestamp),
                                                style: TextStyle(
                                                  fontSize: 12,
                                                  color: Colors.blue.shade600,
                                                  fontWeight: FontWeight.w500,
                                                ),
                                              ),
                                            ],
                                          ],
                                        ),
                                      ),
                                      if (_lastPrediction != null) ...[
                                        Icon(
                                          Icons.arrow_forward_ios,
                                          color: Colors.blue.shade600,
                                          size: 16,
                                        ),
                                      ],
                                    ],
                                  ),
                                ),
                              ),
                            const SizedBox(height: 20),
                            // Only show recommendations now - removed clinical status sections
                            
                            // Recommendations Card - Show from last prediction if available
                            if (_lastPrediction != null && _lastPrediction!.modelPrediction.recommendations.isNotEmpty) ...[
                              Container(
                                width: double.infinity,
                                padding: const EdgeInsets.all(16.0),
                                decoration: BoxDecoration(
                                  color: Colors.amber.shade50,
                                  borderRadius: BorderRadius.circular(12),
                                  border: Border.all(color: Colors.amber.shade200),
                                ),
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Row(
                                      children: [
                                        Icon(
                                          Icons.lightbulb_outline,
                                          color: Colors.amber.shade700,
                                          size: 20,
                                        ),
                                        const SizedBox(width: 8),
                                        Text(
                                          'Güncel Öneriler',
                                          style: TextStyle(
                                            fontSize: 16,
                                            fontWeight: FontWeight.w600,
                                            color: Colors.amber.shade800,
                                          ),
                                        ),
                                      ],
                                    ),
                                    const SizedBox(height: 12),
                                    Container(
                                      width: double.infinity,
                                      padding: const EdgeInsets.all(12.0),
                                      decoration: BoxDecoration(
                                        color: Colors.white,
                                        borderRadius: BorderRadius.circular(8),
                                        border: Border.all(color: Colors.amber.shade100),
                                      ),
                                      child: Column(
                                        crossAxisAlignment: CrossAxisAlignment.start,
                                        children: _lastPrediction!.modelPrediction.recommendations.map((recommendation) => 
                                          Padding(
                                            padding: const EdgeInsets.only(bottom: 8.0),
                                            child: Row(
                                              crossAxisAlignment: CrossAxisAlignment.start,
                                              children: [
                                                Container(
                                                  width: 6,
                                                  height: 6,
                                                  margin: const EdgeInsets.only(top: 6),
                                                  decoration: BoxDecoration(
                                                    color: Colors.amber.shade700,
                                                    shape: BoxShape.circle,
                                                  ),
                                                ),
                                                const SizedBox(width: 12),
                                                Expanded(
                                                  child: Text(
                                                    recommendation,
                                                    style: TextStyle(
                                                      fontSize: 13,
                                                      height: 1.4,
                                                      color: Colors.grey.shade700,
                                                    ),
                                                  ),
                                                ),
                                              ],
                                            ),
                                          ),
                                        ).toList(),
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                              const SizedBox(height: 16),
                            ] else if (_lastClassification != null) ...[
                              // Fallback to clinical recommendations if no prediction recommendations
                              Container(
                                width: double.infinity,
                                padding: const EdgeInsets.all(16.0),
                                decoration: BoxDecoration(
                                  color: Colors.green.shade50,
                                  borderRadius: BorderRadius.circular(12),
                                  border: Border.all(color: Colors.green.shade200),
                                ),
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Row(
                                      children: [
                                        Icon(
                                          Icons.medical_services,
                                          color: Colors.green.shade700,
                                          size: 20,
                                        ),
                                        const SizedBox(width: 8),
                                        Text(
                                          'Klinik Öneriler',
                                          style: TextStyle(
                                            fontSize: 16,
                                            fontWeight: FontWeight.w600,
                                            color: Colors.green.shade800,
                                          ),
                                        ),
                                      ],
                                    ),
                                    const SizedBox(height: 12),
                                    Container(
                                      width: double.infinity,
                                      padding: const EdgeInsets.all(12.0),
                                      decoration: BoxDecoration(
                                        color: Colors.white,
                                        borderRadius: BorderRadius.circular(8),
                                        border: Border.all(color: Colors.green.shade100),
                                      ),
                                      child: Column(
                                        crossAxisAlignment: CrossAxisAlignment.start,
                                        children: [
                                          if (_lastClassification!.recommendationAdjustments.medicationPriority.isNotEmpty) ...[
                                            _buildRecommendationItem(
                                              'İlaç Önceliği',
                                              _lastClassification!.recommendationAdjustments.medicationPriority,
                                              Icons.medication,
                                            ),
                                            const SizedBox(height: 8),
                                          ],
                                          if (_lastClassification!.recommendationAdjustments.environmentalControlLevel.isNotEmpty) ...[
                                            _buildRecommendationItem(
                                              'Çevresel Kontrol',
                                              _lastClassification!.recommendationAdjustments.environmentalControlLevel,
                                              Icons.home,
                                            ),
                                            const SizedBox(height: 8),
                                          ],
                                          if (_lastClassification!.recommendationAdjustments.monitoringFrequency.isNotEmpty) ...[
                                            _buildRecommendationItem(
                                              'İzlem Sıklığı',
                                              _lastClassification!.recommendationAdjustments.monitoringFrequency,
                                              Icons.schedule,
                                            ),
                                            const SizedBox(height: 8),
                                          ],
                                          if (_lastClassification!.recommendationAdjustments.emergencyPreparedness) ...[
                                            _buildRecommendationItem(
                                              'Acil Durum Hazırlığı',
                                              'Acil durum planı oluşturun ve epipen taşıyın',
                                              Icons.emergency,
                                            ),
                                          ],
                                        ],
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                              const SizedBox(height: 16),
                            ],
                          ],
                        ),
                      ),
                    ),
                  ),
                    const SizedBox(height: 16),
                  ],

                  // Primary Action Button
                  if (_hasExistingProfile) ...[
                    Center(
                      child: Container(
                        width: 200,
                        height: 200,
                        child: ElevatedButton(
                          onPressed: _isLoading ? null : _makePrediction,
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.teal.shade600,
                            foregroundColor: Colors.white,
                            shape: const CircleBorder(),
                            elevation: 8,
                            shadowColor: Colors.teal.shade300,
                          ),
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              if (_isLoading) ...[
                                const SizedBox(
                                  width: 40,
                                  height: 40,
                                  child: CircularProgressIndicator(
                                    strokeWidth: 3,
                                    valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                                  ),
                                ),
                                const SizedBox(height: 16),
                                const Text(
                                  'Analiz\nYapılıyor...',
                                  textAlign: TextAlign.center,
                                  style: TextStyle(
                                    fontSize: 16,
                                    fontWeight: FontWeight.w600,
                                    height: 1.3,
                                  ),
                                ),
                              ] else ...[
                                Container(
                                  padding: const EdgeInsets.all(10),
                                  decoration: BoxDecoration(
                                    color: Colors.white.withOpacity(0.2),
                                    borderRadius: BorderRadius.circular(18),
                                  ),
                                  child: const Icon(
                                    Icons.shield_outlined,
                                    size: 32,
                                    color: Colors.white,
                                  ),
                                ),
                                const SizedBox(height: 14),
                                const Text(
                                  'Risk Analizi\nBaşlat',
                                  textAlign: TextAlign.center,
                                  style: TextStyle(
                                    fontSize: 18,
                                    fontWeight: FontWeight.bold,
                                    height: 1.2,
                                    letterSpacing: 0.3,
                                  ),
                                ),
                                const SizedBox(height: 12),
                                Text(
                                  'Güncel konum ve hava\nverilerine göre alerji\nrisk tahminini görün',
                                  textAlign: TextAlign.center,
                                  style: TextStyle(
                                    fontSize: 13,
                                    fontWeight: FontWeight.w500,
                                    color: Colors.white.withOpacity(0.9),
                                    height: 1.3,
                                  ),
                                ),
                              ],
                            ],
                          ),
                        ),
                      ),
                    ),
                  ] else ...[
                    Center(
                      child: Container(
                        width: 200,
                        height: 200,
                        child: ElevatedButton(
                          onPressed: _navigateToProfileForm,
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.teal.shade600,
                            foregroundColor: Colors.white,
                            shape: const CircleBorder(),
                            elevation: 8,
                            shadowColor: Colors.teal.shade300,
                          ),
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Container(
                                padding: const EdgeInsets.all(10),
                                decoration: BoxDecoration(
                                  color: Colors.white.withOpacity(0.2),
                                  borderRadius: BorderRadius.circular(20),
                                ),
                                child: const Icon(
                                  Icons.person_add_alt_1,
                                  size: 32,
                                  color: Colors.white,
                                ),
                              ),
                              const SizedBox(height: 16),
                              const Text(
                                'Klinik Profil\nOluştur',
                                textAlign: TextAlign.center,
                                style: TextStyle(
                                  fontSize: 18,
                                  fontWeight: FontWeight.bold,
                                  height: 1.2,
                                  letterSpacing: 0.3,
                                ),
                              ),
                              const SizedBox(height: 12),
                              Text(
                                'Kişiselleştirilmiş\nAlerji Analizi',
                                textAlign: TextAlign.center,
                                style: TextStyle(
                                  fontSize: 15,
                                  fontWeight: FontWeight.w500,
                                  color: Colors.white.withOpacity(0.9),
                                  height: 1.3,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                  ],
                  
                  const SizedBox(height: 16),

                  // Information Cards - Sadece profil yokken göster
                  if (!_hasExistingProfile) ...[
                    Container(
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: Colors.blue.shade50,
                        borderRadius: BorderRadius.circular(8),
                        border: Border.all(color: Colors.blue.shade200),
                      ),
                      child: Row(
                        children: [
                          Icon(Icons.medical_information, color: Colors.blue.shade700),
                          const SizedBox(width: 12),
                          const Expanded(
                            child: Text(
                              'Detaylı profil oluşturarak daha hassas alerji tahminleri alabilir, polen ve besin alerjilerinizi belirtebilirsiniz.',
                              style: TextStyle(fontSize: 13),
                            ),
                          ),
                        ],
                      ),
                    ),

                    const SizedBox(height: 16),
                  ],
                  
                  Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: Colors.green.shade50,
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(color: Colors.green.shade200),
                    ),
                    child: Row(
                      children: [
                        Icon(Icons.security, color: Colors.green.shade700),
                        const SizedBox(width: 12),
                        const Expanded(
                          child: Text(
                            'Verileriniz güvenli şekilde saklanır ve sadece size özel tahminler için kullanılır.',
                            style: TextStyle(fontSize: 13),
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
                ),
              ),
            ),
      ),
    );
  }
}