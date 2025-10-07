import 'package:flutter/material.dart';
import '../models/allergy_classification_response.dart';
import '../models/allergy_profile_request.dart';
import 'detailed_profile_form_screen.dart';
import 'user_selection_screen.dart';

class AllergyClassificationResultScreen extends StatelessWidget {
  final AllergyClassificationResponse response;
  final AllergyProfileRequest request;

  const AllergyClassificationResultScreen({
    Key? key,
    required this.response,
    required this.request,
  }) : super(key: key);

  Color _getGroupColor() {
    switch (response.groupId) {
      case 1:
        return Colors.red.shade700;
      case 2:
        return Colors.orange.shade700;
      case 3:
        return Colors.yellow.shade700;
      case 4:
        return Colors.blue.shade700;
      case 5:
        return Colors.purple.shade700;
      default:
        return Colors.grey.shade700;
    }
  }

  IconData _getGroupIcon() {
    switch (response.groupId) {
      case 1:
        return Icons.warning;
      case 2:
        return Icons.info;
      case 3:
        return Icons.healing;
      case 4:
        return Icons.help_outline;
      case 5:
        return Icons.child_care;
      default:
        return Icons.person;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Alerji Analiz Sonucu'),
        backgroundColor: _getGroupColor(),
        foregroundColor: Colors.white,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () {
            Navigator.pushAndRemoveUntil(
              context,
              MaterialPageRoute(builder: (context) => const UserSelectionScreen()),
              (route) => false,
            );
          },
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildGroupCard(context),
            const SizedBox(height: 16),
            _buildImmunologicProfileCard(context),
            const SizedBox(height: 16),
            _buildPollenRisksCard(context),
            const SizedBox(height: 16),
            _buildEnvironmentalSensitivityCard(context),
            const SizedBox(height: 16),
            _buildRiskModifiersCard(context),
            const SizedBox(height: 16),
            _buildRecommendationsCard(context),
            const SizedBox(height: 24),
            _buildActionButtons(context),
          ],
        ),
      ),
    );
  }

  Widget _buildGroupCard(BuildContext context) {
    return Card(
      elevation: 4,
      child: Container(
        width: double.infinity,
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(12),
          gradient: LinearGradient(
            colors: [
              _getGroupColor(),
              _getGroupColor().withOpacity(0.8),
            ],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        child: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            children: [
              Icon(
                _getGroupIcon(),
                size: 48,
                color: Colors.white,
              ),
              const SizedBox(height: 12),
              Text(
                'GRUP ${response.groupId}',
                style: const TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                ),
              ),
              const SizedBox(height: 8),
              Text(
                response.groupName,
                style: const TextStyle(
                  fontSize: 18,
                  color: Colors.white,
                  fontWeight: FontWeight.w500,
                ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 12),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(0.2),
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Text(
                  response.groupDescription,
                  style: const TextStyle(
                    fontSize: 14,
                    color: Colors.white,
                  ),
                  textAlign: TextAlign.center,
                ),
              ),
              const SizedBox(height: 12),
              Text(
                'Atanma Nedeni: ${response.assignmentReason}',
                style: const TextStyle(
                  fontSize: 12,
                  color: Colors.white70,
                ),
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildImmunologicProfileCard(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(Icons.biotech, color: Theme.of(context).primaryColor),
                const SizedBox(width: 8),
                Text(
                  'İmmünolojik Profil',
                  style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            ..._buildDynamicProfileItems(),
          ],
        ),
      ),
    );
  }

  List<Widget> _buildDynamicProfileItems() {
    List<Widget> items = [];
    final profile = response.immunologicProfile;
    
    // Ana 4 alan - sadece dolu olanları göster
    if (profile.igeLevel.isNotEmpty) {
      items.add(_buildProfileItem('IgE Seviyesi', _translateProfileValue(profile.igeLevel), Icons.science));
    }
    
    if (profile.antihistamineResponse.isNotEmpty) {
      items.add(_buildProfileItem('Antihistaminik Yanıt', _translateProfileValue(profile.antihistamineResponse), Icons.medication));
    }
    
    if (profile.inflammatoryResponse.isNotEmpty) {
      items.add(_buildProfileItem('İnflamatuar Yanıt', _translateProfileValue(profile.inflammatoryResponse), Icons.local_fire_department));
    }
    
    if (profile.seasonalPattern.isNotEmpty) {
      items.add(_buildProfileItem('Mevsimsel Patern', _translateProfileValue(profile.seasonalPattern), Icons.calendar_month));
    }
    
    // SEVERE_ALLERGIC grubu için ek alanlar
    if (profile.th2Activation != null && profile.th2Activation!.isNotEmpty) {
      items.add(_buildProfileItem('TH2 Aktivasyonu', _translateProfileValue(profile.th2Activation!), Icons.biotech));
    }
    
    if (profile.mastCellDegranulation != null && profile.mastCellDegranulation!.isNotEmpty) {
      items.add(_buildProfileItem('Mast Hücre Degranülasyonu', _translateProfileValue(profile.mastCellDegranulation!), Icons.scatter_plot));
    }
    
    if (profile.cytokineProfile != null && profile.cytokineProfile!.isNotEmpty) {
      items.add(_buildProfileItem('Sitokin Profili', profile.cytokineProfile!.join(', '), Icons.coronavirus));
    }
    
    // GENETIC_PREDISPOSITION grubu için ek alanlar
    if (profile.atopicStructure != null) {
      items.add(_buildProfileItem('Atopik Yapı', profile.atopicStructure! ? 'Var' : 'Yok', Icons.medical_information));
    }
    
    if (profile.familyLoading != null) {
      items.add(_buildProfileItem('Aile Yükü', profile.familyLoading! ? 'Var' : 'Yok', Icons.family_restroom));
    }
    
    if (profile.igeProductionCapacity != null && profile.igeProductionCapacity!.isNotEmpty) {
      items.add(_buildProfileItem('IgE Üretim Kapasitesi', _translateProfileValue(profile.igeProductionCapacity!), Icons.precision_manufacturing));
    }
    
    if (profile.th1Th2Imbalance != null) {
      items.add(_buildProfileItem('TH1/TH2 Dengesizliği', profile.th1Th2Imbalance! ? 'Var' : 'Yok', Icons.scale));
    }
    
    if (profile.sensitizationRisk != null && profile.sensitizationRisk!.isNotEmpty) {
      items.add(_buildProfileItem('Sensitizasyon Riski', _translateProfileValue(profile.sensitizationRisk!), Icons.warning));
    }
    
    // UNDIAGNOSED grubu için ek alanlar
    if (profile.sensitization != null && profile.sensitization!.isNotEmpty) {
      items.add(_buildProfileItem('Sensitizasyon', _translateProfileValue(profile.sensitization!), Icons.help));
    }
    
    if (profile.environmentalTriggers != null) {
      items.add(_buildProfileItem('Çevresel Tetikleyiciler', profile.environmentalTriggers! ? 'Var' : 'Yok', Icons.eco));
    }
    
    // VULNERABLE_POPULATION grubu için ek alanlar
    if (profile.immuneSystem != null && profile.immuneSystem!.isNotEmpty) {
      items.add(_buildProfileItem('Bağışıklık Sistemi', _translateProfileValue(profile.immuneSystem!), Icons.shield));
    }
    
    if (profile.immuneTolerance != null && profile.immuneTolerance!.isNotEmpty) {
      items.add(_buildProfileItem('Bağışıklık Toleransı', _translateProfileValue(profile.immuneTolerance!), Icons.security));
    }
    
    if (profile.multisystemRisk != null && profile.multisystemRisk!.isNotEmpty) {
      items.add(_buildProfileItem('Multisistem Riski', _translateProfileValue(profile.multisystemRisk!), Icons.medical_services));
    }
    
    return items;
  }
  
  String _translateProfileValue(String value) {
    final translations = {
      // IgE Levels
      'very_high': 'Çok Yüksek',
      'moderate_high': 'Orta-Yüksek',
      'normal_borderline': 'Normal-Sınırda',
      'high': 'Yüksek',
      'low': 'Düşük',
      'normal': 'Normal',
      
      // Responses
      'good': 'İyi',
      'poor': 'Zayıf',
      'excellent': 'Mükemmel',
      'moderate': 'Orta',
      
      // Activation/Response Levels
      'maximal': 'Maksimal',
      'local': 'Lokal',
      'non_specific': 'Spesifik Olmayan',
      'rapid_widespread': 'Hızlı Yaygın',
      'increased': 'Artmış',
      
      // Patterns
      'rhinitis': 'Rinit',
      'asthma': 'Astım',
      'eczema': 'Egzama',
      
      // Clarity
      'unclear': 'Belirsiz',
      'clear': 'Net',
      
      // System Status
      'immature_aged': 'Olgunlaşmamış/Yaşlı',
      'mature': 'Olgun',
      'compromised': 'Bozulmuş',
    };
    
    return translations[value.toLowerCase()] ?? value.toUpperCase();
  }

  Widget _buildProfileItem(String label, String value, IconData icon) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4.0),
      child: Row(
        children: [
          Icon(icon, size: 20, color: Colors.grey.shade600),
          const SizedBox(width: 12),
          Expanded(
            child: Text(
              label,
              style: const TextStyle(fontWeight: FontWeight.w500),
            ),
          ),
          Text(
            value,
            style: TextStyle(
              color: Colors.grey.shade700,
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildPollenRisksCard(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(Icons.grass, color: Colors.green.shade700),
                const SizedBox(width: 8),
                Text(
                  'Polen Risk Analizi',
                  style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            if (response.pollenSpecificRisks.highRiskPollens.isEmpty && 
                response.pollenSpecificRisks.moderateRiskPollens.isEmpty && 
                response.pollenSpecificRisks.crossReactiveFoods.isEmpty) ...[
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(16.0),
                decoration: BoxDecoration(
                  color: Colors.blue.shade50,
                  borderRadius: BorderRadius.circular(8.0),
                  border: Border.all(color: Colors.blue.shade200),
                ),
                child: Row(
                  children: [
                    Icon(Icons.info_outline, color: Colors.blue.shade600),
                    const SizedBox(width: 12),
                    const Expanded(
                      child: Text(
                        'Polen riski yoktur. Mevcut veriler doğrultusunda herhangi bir polen alerjisi riski tespit edilmemiştir.',
                        style: TextStyle(fontSize: 14),
                      ),
                    ),
                  ],
                ),
              ),
            ] else ...[
              if (response.pollenSpecificRisks.highRiskPollens.isNotEmpty) ...[
                _buildRiskSection(
                  'Yüksek Risk Polenleri',
                  response.pollenSpecificRisks.highRiskPollens,
                  Colors.red.shade600,
                  Icons.dangerous,
                ),
                const SizedBox(height: 12),
              ],
              if (response.pollenSpecificRisks.moderateRiskPollens.isNotEmpty) ...[
                _buildRiskSection(
                  'Orta Risk Polenleri',
                  response.pollenSpecificRisks.moderateRiskPollens,
                  Colors.orange.shade600,
                  Icons.warning,
                ),
                const SizedBox(height: 12),
              ],
              if (response.pollenSpecificRisks.crossReactiveFoods.isNotEmpty) ...[
                _buildRiskSection(
                  'Çapraz Reaktif Besinler',
                  response.pollenSpecificRisks.crossReactiveFoods,
                  Colors.blue.shade600,
                  Icons.restaurant,
                ),
              ],
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildRiskSection(String title, List<String> items, Color color, IconData icon) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Icon(icon, size: 18, color: color),
            const SizedBox(width: 8),
            Text(
              title,
              style: TextStyle(
                fontWeight: FontWeight.bold,
                color: color,
              ),
            ),
          ],
        ),
        const SizedBox(height: 8),
        Wrap(
          spacing: 6.0,
          runSpacing: 6.0,
          children: items.map((item) {
            return Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
              decoration: BoxDecoration(
                color: color.withOpacity(0.1),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: color.withOpacity(0.3)),
              ),
              child: Text(
                item,
                style: TextStyle(
                  fontSize: 12,
                  color: color,
                  fontWeight: FontWeight.w500,
                ),
              ),
            );
          }).toList(),
        ),
      ],
    );
  }

  Widget _buildEnvironmentalSensitivityCard(BuildContext context) {
    final sensitivities = [
      ('Hava Kirliliği', response.environmentalSensitivityFactors.airPollutionSensitivity),
      ('Ev Tozu Akarı', response.environmentalSensitivityFactors.dustMiteSensitivity),
      ('Hayvan Tüyü', response.environmentalSensitivityFactors.petDanderSensitivity),
      ('Küf', response.environmentalSensitivityFactors.moldSensitivity),
      ('Duman', response.environmentalSensitivityFactors.smokeSensitivity),
    ];

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(Icons.air, color: Colors.blue.shade700),
                const SizedBox(width: 8),
                Text(
                  'Çevresel Hassasiyetler',
                  style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            ...sensitivities.map((sensitivity) {
              return Padding(
                padding: const EdgeInsets.symmetric(vertical: 4.0),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      sensitivity.$1,
                      style: const TextStyle(fontWeight: FontWeight.w500),
                    ),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                      decoration: BoxDecoration(
                        color: sensitivity.$2 ? Colors.red.shade100 : Colors.green.shade100,
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Text(
                        sensitivity.$2 ? 'Hassas' : 'Normal',
                        style: TextStyle(
                          color: sensitivity.$2 ? Colors.red.shade700 : Colors.green.shade700,
                          fontWeight: FontWeight.bold,
                          fontSize: 12,
                        ),
                      ),
                    ),
                  ],
                ),
              );
            }).toList(),
          ],
        ),
      ),
    );
  }

  Widget _buildRiskModifiersCard(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(Icons.tune, color: Colors.purple.shade700),
                const SizedBox(width: 8),
                Text(
                  'Kişisel Risk Faktörleri',
                  style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            _buildModifierItem('Mevsimsel Çarpan', response.personalRiskModifiers.seasonalModifier),
            _buildModifierItem('Çevresel Amplifikatör', response.personalRiskModifiers.environmentalAmplifier),
            _buildModifierItem('Komorbidite Faktörü', response.personalRiskModifiers.comorbidityFactor),
            _buildModifierItem('Temel Hassasiyet', response.personalRiskModifiers.baseSensitivity),
            const SizedBox(height: 8),
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.purple.shade50,
                borderRadius: BorderRadius.circular(8),
                border: Border.all(color: Colors.purple.shade200),
              ),
              child: Row(
                children: [
                  Icon(Icons.calculate, color: Colors.purple.shade700),
                  const SizedBox(width: 8),
                  Text(
                    'Model Ağırlığı: ${(response.modelWeight * 100).toStringAsFixed(1)}%',
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      color: Colors.purple.shade700,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildModifierItem(String label, double value) {
    Color color = value > 1.0 ? Colors.red : (value < 1.0 ? Colors.green : Colors.orange);
    
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            label,
            style: const TextStyle(fontWeight: FontWeight.w500),
          ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
            decoration: BoxDecoration(
              color: color.withOpacity(0.1),
              borderRadius: BorderRadius.circular(8),
              border: Border.all(color: color.withOpacity(0.3)),
            ),
            child: Text(
              value.toStringAsFixed(2),
              style: TextStyle(
                color: color,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildRecommendationsCard(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(Icons.medical_services, color: Colors.teal.shade700),
                const SizedBox(width: 8),
                Text(
                  'Öneriler ve Takip',
                  style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            _buildRecommendationItem(
              'Çevresel Kontrol',
              response.recommendationAdjustments.environmentalControlLevel,
              Icons.home,
            ),
            _buildRecommendationItem(
              'İlaç Önceliği',
              response.recommendationAdjustments.medicationPriority,
              Icons.medication,
            ),
            _buildRecommendationItem(
              'Takip Sıklığı',
              response.recommendationAdjustments.monitoringFrequency,
              Icons.schedule,
            ),
            const SizedBox(height: 12),
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: response.recommendationAdjustments.emergencyPreparedness
                    ? Colors.red.shade50
                    : Colors.green.shade50,
                borderRadius: BorderRadius.circular(8),
                border: Border.all(
                  color: response.recommendationAdjustments.emergencyPreparedness
                      ? Colors.red.shade200
                      : Colors.green.shade200,
                ),
              ),
              child: Row(
                children: [
                  Icon(
                    response.recommendationAdjustments.emergencyPreparedness
                        ? Icons.emergency
                        : Icons.check_circle,
                    color: response.recommendationAdjustments.emergencyPreparedness
                        ? Colors.red.shade700
                        : Colors.green.shade700,
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      response.recommendationAdjustments.emergencyPreparedness
                          ? 'Acil durum hazırlığı gerekli'
                          : 'Acil durum riski düşük',
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        color: response.recommendationAdjustments.emergencyPreparedness
                            ? Colors.red.shade700
                            : Colors.green.shade700,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildRecommendationItem(String label, String value, IconData icon) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4.0),
      child: Row(
        children: [
          Icon(icon, size: 20, color: Colors.grey.shade600),
          const SizedBox(width: 12),
          Expanded(
            child: Text(
              label,
              style: const TextStyle(fontWeight: FontWeight.w500),
            ),
          ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
            decoration: BoxDecoration(
              color: Colors.teal.shade50,
              borderRadius: BorderRadius.circular(8),
              border: Border.all(color: Colors.teal.shade200),
            ),
            child: Text(
              value.toUpperCase(),
              style: TextStyle(
                color: Colors.teal.shade700,
                fontWeight: FontWeight.bold,
                fontSize: 12,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildActionButtons(BuildContext context) {
    return Column(
      children: [
        SizedBox(
          width: double.infinity,
          child: ElevatedButton.icon(
            onPressed: () {
              Navigator.pushAndRemoveUntil(
                context,
                MaterialPageRoute(builder: (context) => const UserSelectionScreen()),
                (route) => false,
              );
            },
            icon: const Icon(Icons.home),
            label: const Text('Ana Sayfaya Dön'),
            style: ElevatedButton.styleFrom(
              padding: const EdgeInsets.symmetric(vertical: 16),
              backgroundColor: _getGroupColor(),
              foregroundColor: Colors.white,
            ),
          ),
        ),
        const SizedBox(height: 12),
        SizedBox(
          width: double.infinity,
          child: OutlinedButton.icon(
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => DetailedProfileFormScreen(
                    existingRequest: request,
                    isEditing: true,
                  ),
                ),
              );
            },
            icon: const Icon(Icons.edit),
            label: const Text('Profil Güncelle'),
            style: OutlinedButton.styleFrom(
              padding: const EdgeInsets.symmetric(vertical: 16),
              side: BorderSide(color: _getGroupColor()),
              foregroundColor: _getGroupColor(),
            ),
          ),
        ),
      ],
    );
  }


}