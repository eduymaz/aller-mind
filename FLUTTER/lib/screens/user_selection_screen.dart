import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';
import '../models/allergy_profile_request.dart';
import '../models/allergy_classification_response.dart';
import '../models/user_profile_response.dart';
import '../models/prediction_response.dart';
import '../services/user_storage_service.dart';
import '../services/allergy_classification_service.dart';
import 'detailed_profile_form_screen.dart';
import 'allergy_classification_result_screen.dart';
import 'prediction_result_screen.dart';

class UserSelectionScreen extends StatefulWidget {
  const UserSelectionScreen({super.key});

  @override
  State<UserSelectionScreen> createState() => _UserSelectionScreenState();
}

class _UserSelectionScreenState extends State<UserSelectionScreen> with WidgetsBindingObserver {
  bool _isLoading = true;
  bool _hasExistingProfile = false;
  UserProfileResponse? _userProfile;
  AllergyProfileRequest? _userRequest;
  AllergyClassificationResponse? _lastClassification;

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
            final userProfile = await AllergyClassificationService.getUserProfile(userPreferenceId);
            final userRequest = await UserStorageService.getUserRequest();
            final lastClassification = await UserStorageService.getLastClassification();
            
            setState(() {
              _hasExistingProfile = true;
              _userProfile = userProfile;
              _userRequest = userRequest;
              _lastClassification = lastClassification;
            });
            
            return; // Exit early on success
          } catch (e) {
            // If API call fails, we might have local data
            final userRequest = await UserStorageService.getUserRequest();
            final lastClassification = await UserStorageService.getLastClassification();
            
            if (userRequest != null && lastClassification != null) {
              setState(() {
                _hasExistingProfile = true;
                _userRequest = userRequest;
                _lastClassification = lastClassification;
              });
              
              return; // Exit early on success
            }
          }
        } else {
          // Check for local data even without userPreferenceId
          final userRequest = await UserStorageService.getUserRequest();
          final lastClassification = await UserStorageService.getLastClassification();
          
          if (userRequest != null && lastClassification != null) {
            setState(() {
              _hasExistingProfile = true;
              _userRequest = userRequest;
              _lastClassification = lastClassification;
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
    // Always fetch the latest data before navigating
    try {
      final userRequest = await UserStorageService.getUserRequest();
      final lastClassification = await UserStorageService.getLastClassification();
      
      if (lastClassification != null && userRequest != null) {
        if (mounted) {
          final result = await Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => AllergyClassificationResultScreen(
                response: lastClassification,
                request: userRequest,
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
              content: Text('Sonuç bulunamadı. Lütfen önce analiz yapın.'),
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
        _userProfile = null;
        _userRequest = null;
        _lastClassification = null;
      });
      
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Profil başarıyla silindi'),
          backgroundColor: Colors.green,
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('AllerMind'),
        backgroundColor: Colors.teal,
        foregroundColor: Colors.white,
        actions: _hasExistingProfile ? [
          PopupMenuButton<String>(
            onSelected: (value) {
              if (value == 'clear') {
                _clearUserData();
              }
            },
            itemBuilder: (context) => [
              const PopupMenuItem(
                value: 'clear',
                child: Row(
                  children: [
                    Icon(Icons.delete, color: Colors.red),
                    SizedBox(width: 8),
                    Text('Profil Sil'),
                  ],
                ),
              ),
            ],
          ),
        ] : null,
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
                padding: const EdgeInsets.all(24.0),
                physics: const AlwaysScrollableScrollPhysics(),
                child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Welcome Card
                  Card(
                    elevation: 4,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Padding(
                      padding: const EdgeInsets.all(20.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: [
                              Icon(
                                Icons.health_and_safety,
                                size: 32,
                                color: Colors.teal.shade700,
                              ),
                              const SizedBox(width: 12),
                              const Expanded(
                                child: Text(
                                  'AllerMind\'e Hoş Geldiniz',
                                  style: TextStyle(
                                    fontSize: 22,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.teal,
                                  ),
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 16),
                          Text(
                            _hasExistingProfile 
                              ? 'Alerji profiliniz mevcut. Aşağıda son analiz sonucunuzu görebilir, profilinizi güncelleyebilir veya detaylı sonuçları inceleyebilirsiniz.'
                              : 'Kişiselleştirilmiş alerji tahmini için detaylı profilinizi oluşturun.',
                            style: const TextStyle(fontSize: 16),
                          ),
                        ],
                      ),
                    ),
                  ),
                  
                  const SizedBox(height: 24),

                  // Profile Status Card (only show if user has existing profile)
                  if (_hasExistingProfile) ...[
                    Card(
                      elevation: 4,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Padding(
                        padding: const EdgeInsets.all(16.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              children: [
                                Icon(Icons.analytics, color: Colors.green.shade700),
                                const SizedBox(width: 8),
                                const Text(
                                  'Son Analiz Sonucunuz',
                                  style: TextStyle(
                                    fontSize: 18,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.green,
                                  ),
                                ),
                              ],
                            ),
                            const SizedBox(height: 16),
                            if (_userProfile != null) ...[
                              Container(
                                width: double.infinity,
                                padding: const EdgeInsets.all(12.0),
                                decoration: BoxDecoration(
                                  color: Colors.green.shade50,
                                  borderRadius: BorderRadius.circular(8),
                                  border: Border.all(color: Colors.green.shade200),
                                ),
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      'Alerji Grubu: ${_userProfile!.groupName}',
                                      style: const TextStyle(
                                        fontSize: 16,
                                        fontWeight: FontWeight.w600,
                                      ),
                                    ),
                                    const SizedBox(height: 8),
                                    Text(
                                      _userProfile!.groupDescription,
                                      style: TextStyle(
                                        fontSize: 14,
                                        color: Colors.grey.shade700,
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            ] else if (_lastClassification != null) ...[
                              Container(
                                width: double.infinity,
                                padding: const EdgeInsets.all(16.0),
                                decoration: BoxDecoration(
                                  color: Colors.blue.shade50,
                                  borderRadius: BorderRadius.circular(8),
                                  border: Border.all(color: Colors.blue.shade200),
                                ),
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Row(
                                      children: [
                                        Icon(
                                          Icons.group,
                                          color: Colors.blue.shade700,
                                          size: 20,
                                        ),
                                        const SizedBox(width: 8),
                                        Expanded(
                                          child: Text(
                                            'Alerji Grubu: ${_lastClassification!.groupName}',
                                            style: TextStyle(
                                              fontSize: 16,
                                              fontWeight: FontWeight.w600,
                                              color: Colors.blue.shade800,
                                            ),
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
                                        borderRadius: BorderRadius.circular(6),
                                        border: Border.all(color: Colors.blue.shade100),
                                      ),
                                      child: Text(
                                        _lastClassification!.groupDescription,
                                        style: TextStyle(
                                          fontSize: 14,
                                          color: Colors.grey.shade700,
                                          height: 1.4,
                                        ),
                                      ),
                                    ),
                                    const SizedBox(height: 12),
                                    Row(
                                      children: [
                                        Icon(
                                          Icons.info_outline,
                                          color: Colors.blue.shade600,
                                          size: 18,
                                        ),
                                        const SizedBox(width: 8),
                                        Text(
                                          'Grup ID: ${_lastClassification!.groupId}',
                                          style: TextStyle(
                                            fontSize: 14,
                                            fontWeight: FontWeight.w500,
                                            color: Colors.blue.shade600,
                                          ),
                                        ),
                                      ],
                                    ),
                                  ],
                                ),
                              ),
                            ],
                            const SizedBox(height: 16),
                            SizedBox(
                              width: double.infinity,
                              child: OutlinedButton.icon(
                                onPressed: _navigateToDetailedResults,
                                style: OutlinedButton.styleFrom(
                                  padding: const EdgeInsets.symmetric(vertical: 12),
                                  side: BorderSide(color: Colors.teal.shade600),
                                  foregroundColor: Colors.teal.shade600,
                                  shape: RoundedRectangleBorder(
                                    borderRadius: BorderRadius.circular(8),
                                  ),
                                ),
                                icon: const Icon(Icons.visibility),
                                label: const Text(
                                  'Detaylı Sonuçları Görüntüle',
                                  style: TextStyle(
                                    fontSize: 16,
                                    fontWeight: FontWeight.w500,
                                  ),
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                    const SizedBox(height: 24),
                  ],

                  // Action Buttons
                  if (_hasExistingProfile) ...[
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton.icon(
                        onPressed: _isLoading ? null : _makePrediction,
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.teal,
                          foregroundColor: Colors.white,
                          padding: const EdgeInsets.symmetric(vertical: 16),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(12),
                          ),
                          elevation: 5,
                        ),
                        icon: _isLoading 
                            ? const SizedBox(
                                width: 20,
                                height: 20,
                                child: CircularProgressIndicator(
                                  strokeWidth: 2,
                                  valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                                ),
                              )
                            : const Icon(Icons.analytics),
                        label: Text(
                          _isLoading ? 'Tahmin yapılıyor...' : 'Tahmin Yap',
                          style: const TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ),
                  ] else ...[
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton.icon(
                        onPressed: _navigateToProfileForm,
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.teal,
                          foregroundColor: Colors.white,
                          padding: const EdgeInsets.symmetric(vertical: 16),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(12),
                          ),
                          elevation: 5,
                        ),
                        icon: const Icon(Icons.person_add),
                        label: const Text(
                          'Detaylı Profil Oluştur',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
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