import 'package:flutter/material.dart';
import '../models/prediction_response.dart';

class PredictionResultScreen extends StatelessWidget {
  final PredictionResponse predictionResponse;

  const PredictionResultScreen({
    Key? key,
    required this.predictionResponse,
  }) : super(key: key);

  Color _getRiskColor() {
    switch (predictionResponse.overallRiskLevel.toLowerCase()) {
      case 'düşük':
      case 'low':
        return Colors.green;
      case 'orta':
      case 'moderate':
        return Colors.orange;
      case 'yüksek':
      case 'high':
        return Colors.red;
      default:
        return Colors.grey;
    }
  }

  String _getRiskEmoji() {
    // API'den gelen emoji varsa onu kullan, yoksa risk seviyesine göre emoji döndür
    if (predictionResponse.overallRiskEmoji.isNotEmpty && predictionResponse.overallRiskEmoji != '⚪') {
      return predictionResponse.overallRiskEmoji;
    }
    
    switch (predictionResponse.overallRiskLevel.toLowerCase()) {
      case 'düşük':
      case 'low':
        return '🟢';
      case 'orta':
      case 'moderate':
        return '🟡';
      case 'yüksek':
      case 'high':
        return '🔴';
      default:
        return '⚪';
    }
  }

  String _formatTimestamp(String timestamp) {
    try {
      final DateTime dateTime = DateTime.parse(timestamp);
      return '${dateTime.day}/${dateTime.month}/${dateTime.year} ${dateTime.hour}:${dateTime.minute.toString().padLeft(2, '0')}';
    } catch (e) {
      return timestamp;
    }
  }

  String _formatConfidence(double confidence) {
    return '${(confidence * 100).toInt()}%';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Tahmin Sonucu'),
        backgroundColor: _getRiskColor(),
        foregroundColor: Colors.white,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Risk Overview Card
            _buildRiskOverviewCard(),
            const SizedBox(height: 16),
            
            // Predictions Info Card
            _buildPredictionInfoCard(),
            const SizedBox(height: 16),
            
            // Recommendations Card
            _buildRecommendationsCard(),
            const SizedBox(height: 16),
            
            // User Group Card
            _buildUserGroupCard(),
            const SizedBox(height: 16),
            
            // Personal Modifiers Card
            if (predictionResponse.modelPrediction.personalModifiers != null)
              _buildPersonalModifiersCard(),
            const SizedBox(height: 16),
            
            // Environmental Risks Card
            if (predictionResponse.modelPrediction.environmentalRisks != null)
              _buildEnvironmentalRisksCard(),
            const SizedBox(height: 16),
            
            // Pollen Specific Risks Card
            if (predictionResponse.modelPrediction.pollenSpecificRisks != null)
              _buildPollenRisksCard(),
            const SizedBox(height: 24),
            
            // Action Buttons
            _buildActionButtons(context),
          ],
        ),
      ),
    );
  }

  Widget _buildRiskOverviewCard() {
    return Card(
      elevation: 4,
      child: Container(
        width: double.infinity,
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(12),
          gradient: LinearGradient(
            colors: [
              _getRiskColor(),
              _getRiskColor().withOpacity(0.8),
            ],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        child: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            children: [
              Text(
                _getRiskEmoji(),
                style: const TextStyle(fontSize: 48),
              ),
              const SizedBox(height: 12),
              Text(
                'Genel Risk Seviyesi',
                style: const TextStyle(
                  fontSize: 16,
                  color: Colors.white70,
                ),
              ),
              const SizedBox(height: 8),
              Text(
                predictionResponse.overallRiskLevel.toUpperCase(),
                style: const TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                ),
              ),
              const SizedBox(height: 8),
              Text(
                'Risk Skoru: ${(predictionResponse.overallRiskScore * 100).toInt()}/100',
                style: const TextStyle(
                  fontSize: 16,
                  color: Colors.white,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildPredictionInfoCard() {
    final prediction = predictionResponse.modelPrediction;
    
    return Card(
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(Icons.info_outline, color: Colors.blue.shade700),
                const SizedBox(width: 8),
                const Text(
                  'Tahmin Bilgileri',
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: Colors.blue,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            _buildInfoRow('Güvenilirlik', _formatConfidence(prediction.confidence), Icons.verified),
            const SizedBox(height: 12),
            _buildInfoRow('Tarih', _formatTimestamp(prediction.timestamp), Icons.access_time),
            const SizedBox(height: 12),
            _buildInfoRow('Model Versiyonu', prediction.modelVersion, Icons.settings),
            const SizedBox(height: 12),
            _buildInfoRow('Veri Kalitesi', '${(prediction.dataQualityScore * 100).toInt()}%', Icons.verified_user),
          ],
        ),
      ),
    );
  }

  Widget _buildInfoRow(String label, String value, IconData icon) {
    return Row(
      children: [
        Icon(icon, size: 20, color: Colors.grey.shade600),
        const SizedBox(width: 8),
        Text(
          '$label: ',
          style: TextStyle(
            fontSize: 14,
            color: Colors.grey.shade700,
            fontWeight: FontWeight.w500,
          ),
        ),
        Expanded(
          child: Text(
            value,
            style: const TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.w600,
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildRecommendationsCard() {
    final recommendations = predictionResponse.modelPrediction.recommendations;
    
    return Card(
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(Icons.lightbulb_outline, color: Colors.amber.shade700),
                const SizedBox(width: 8),
                const Text(
                  'Öneriler',
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: Colors.amber,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            ...recommendations.map((recommendation) => Padding(
              padding: const EdgeInsets.only(bottom: 12.0),
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
                      style: const TextStyle(
                        fontSize: 14,
                        height: 1.4,
                      ),
                    ),
                  ),
                ],
              ),
            )).toList(),
          ],
        ),
      ),
    );
  }

  Widget _buildUserGroupCard() {
    final userGroup = predictionResponse.modelPrediction.userGroup;
    
    return Card(
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(Icons.group, color: Colors.green.shade700),
                const SizedBox(width: 8),
                const Text(
                  'Kullanıcı Grubu',
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: Colors.green,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(16.0),
              decoration: BoxDecoration(
                color: Colors.green.shade50,
                borderRadius: BorderRadius.circular(8),
                border: Border.all(color: Colors.green.shade200),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    userGroup.groupName,
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w600,
                      color: Colors.green.shade800,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    userGroup.description,
                    style: TextStyle(
                      fontSize: 14,
                      color: Colors.grey.shade700,
                      height: 1.4,
                    ),
                  ),
                  const SizedBox(height: 12),
                  Row(
                    children: [
                      Icon(Icons.assignment, size: 16, color: Colors.green.shade600),
                      const SizedBox(width: 4),
                      Text(
                        'Gerekçe: ${userGroup.assignmentReason}',
                        style: TextStyle(
                          fontSize: 12,
                          color: Colors.green.shade600,
                          fontStyle: FontStyle.italic,
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
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
              Navigator.popUntil(context, (route) => route.isFirst);
            },
            style: ElevatedButton.styleFrom(
              padding: const EdgeInsets.symmetric(vertical: 16),
              backgroundColor: _getRiskColor(),
              foregroundColor: Colors.white,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
            ),
            icon: const Icon(Icons.home),
            label: const Text(
              'Ana Sayfaya Dön',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
        ),
        const SizedBox(height: 12),
        SizedBox(
          width: double.infinity,
          child: OutlinedButton.icon(
            onPressed: () {
              _showShareDialog(context);
            },
            style: OutlinedButton.styleFrom(
              padding: const EdgeInsets.symmetric(vertical: 16),
              side: BorderSide(color: _getRiskColor()),
              foregroundColor: _getRiskColor(),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
            ),
            icon: const Icon(Icons.share),
            label: const Text(
              'Sonuçları Paylaş',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildPersonalModifiersCard() {
    final modifiers = predictionResponse.modelPrediction.personalModifiers!;
    
    return Card(
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(Icons.person, color: Colors.purple.shade700),
                const SizedBox(width: 8),
                const Text(
                  'Kişisel Faktörler',
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: Colors.purple,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            if (modifiers['base_safe_hours'] != null)
              _buildInfoRow('Temel Güvenli Süre', '${modifiers['base_safe_hours'].toStringAsFixed(1)} saat', Icons.schedule),
            const SizedBox(height: 12),
            if (modifiers['personal_safe_hours'] != null)
              _buildInfoRow('Kişisel Güvenli Süre', '${modifiers['personal_safe_hours'].toStringAsFixed(1)} saat', Icons.person_outline),
            const SizedBox(height: 12),
            if (modifiers['personal_multiplier'] != null)
              _buildInfoRow('Kişisel Çarpan', '${modifiers['personal_multiplier'].toStringAsFixed(2)}x', Icons.trending_up),
          ],
        ),
      ),
    );
  }

  Widget _buildEnvironmentalRisksCard() {
    final risks = predictionResponse.modelPrediction.environmentalRisks!;
    
    return Card(
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(Icons.nature, color: Colors.teal.shade700),
                const SizedBox(width: 8),
                const Text(
                  'Çevresel Riskler',
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: Colors.teal,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            _buildRiskItem('Hava Kalitesi', risks['air_quality_risk'] ?? 'low'),
            const SizedBox(height: 8),
            _buildRiskItem('Polen Riski', risks['pollen_risk'] ?? 'low'),
            const SizedBox(height: 8),
            _buildRiskItem('Hava Durumu', risks['weather_risk'] ?? 'low'),
          ],
        ),
      ),
    );
  }

  Widget _buildPollenRisksCard() {
    final pollenRisks = predictionResponse.modelPrediction.pollenSpecificRisks!;
    
    return Card(
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(Icons.local_florist, color: Colors.orange.shade700),
                const SizedBox(width: 8),
                const Text(
                  'Polen Spesifik Riskler',
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: Colors.orange,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            
            // Yüksek Risk Polenleri
            if (pollenRisks['high_risk_pollens'] != null && (pollenRisks['high_risk_pollens'] as List).isNotEmpty) ...[
              const Text(
                'Yüksek Risk Polenleri:',
                style: TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.w600,
                  color: Colors.red,
                ),
              ),
              const SizedBox(height: 8),
              ...(pollenRisks['high_risk_pollens'] as List).map((pollen) => 
                Padding(
                  padding: const EdgeInsets.only(bottom: 4),
                  child: Row(
                    children: [
                      Icon(Icons.warning, size: 16, color: Colors.red),
                      const SizedBox(width: 8),
                      Text(_translatePollenName(pollen.toString())),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 12),
            ],
            
            // Orta Risk Polenleri
            if (pollenRisks['moderate_risk_pollens'] != null && (pollenRisks['moderate_risk_pollens'] as List).isNotEmpty) ...[
              const Text(
                'Orta Risk Polenleri:',
                style: TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.w600,
                  color: Colors.orange,
                ),
              ),
              const SizedBox(height: 8),
              ...(pollenRisks['moderate_risk_pollens'] as List).map((pollen) => 
                Padding(
                  padding: const EdgeInsets.only(bottom: 4),
                  child: Row(
                    children: [
                      Icon(Icons.info, size: 16, color: Colors.orange),
                      const SizedBox(width: 8),
                      Text(_translatePollenName(pollen.toString())),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 12),
            ],
            
            // Çapraz Reaktif Gıdalar
            if (pollenRisks['cross_reactive_foods'] != null && (pollenRisks['cross_reactive_foods'] as List).isNotEmpty) ...[
              const Text(
                'Dikkat Edilmesi Gereken Gıdalar:',
                style: TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.w600,
                  color: Colors.blue,
                ),
              ),
              const SizedBox(height: 8),
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.blue.shade50,
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: Colors.blue.shade200),
                ),
                child: Wrap(
                  spacing: 8,
                  runSpacing: 4,
                  children: (pollenRisks['cross_reactive_foods'] as List).map((food) => 
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                      decoration: BoxDecoration(
                        color: Colors.blue.shade100,
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Text(
                        _translateFoodName(food.toString()),
                        style: TextStyle(
                          fontSize: 12,
                          color: Colors.blue.shade800,
                        ),
                      ),
                    ),
                  ).toList(),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }

  String _translateRiskLevel(String risk) {
    final translations = {
      'high': 'Yüksek',
      'medium': 'Orta',
      'moderate': 'Orta',
      'low': 'Düşük',
    };
    return translations[risk.toLowerCase()] ?? risk.toUpperCase();
  }

  String _translatePollenName(String pollen) {
    final translations = {
      // Trees - Ağaçlar
      'birch': 'Huş Ağacı',
      'oak': 'Meşe',
      'pine': 'Çam',
      'olive': 'Zeytin',
      'plane': 'Çınar',
      'cypress': 'Servi',
      'hazel': 'Fındık',
      'alder': 'Kızılağaç',
      'poplar': 'Kavak',
      'willow': 'Söğüt',
      'ash': 'Dişbudak',
      'maple': 'Akçaağaç',
      'elm': 'Karaağaç',
      'beech': 'Kayın',
      'chestnut': 'Kestane',
      'linden': 'Ihlamur',
      'walnut': 'Ceviz',
      
      // Grasses - Otlar
      'grass': 'Çimen',
      'timothy': 'Timothy Otu',
      'rye grass': 'Çavdar Otu',
      'bermuda': 'Bermuda Otu',
      'johnson grass': 'Johnson Otu',
      'bahia': 'Bahia Otu',
      'fescue': 'Yumak Otu',
      'kentucky bluegrass': 'Kentucky Çimi',
      'orchard grass': 'Domuz Ayrığı',
      
      // Weeds - Yabani Otlar
      'ragweed': 'Ambrozya',
      'mugwort': 'Pelin',
      'plantain': 'Sinir Otu',
      'nettle': 'Isırgan',
      'sorrel': 'Kuzukulağı',
      'goosefoot': 'Sirken',
      'lamb\'s quarters': 'Kazayağı',
      'english plantain': 'İngiliz Sinir Otu',
      'cocklebur': 'Domuz Pıtrağı',
      'sagebrush': 'Yavşan Otu',
      'amaranth': 'Horozibiği',
      'pigweed': 'Domuz Otu',
      
      // Fungi/Molds - Küfler
      'alternaria': 'Alternaria Küfü',
      'cladosporium': 'Cladosporium Küfü',
      'aspergillus': 'Aspergillus Küfü',
      'penicillium': 'Penicillium Küfü',
      'botrytis': 'Botrytis Küfü',
      'helminthosporium': 'Helminthosporium Küfü',
      'epicoccum': 'Epicoccum Küfü',
      'stemphylium': 'Stemphylium Küfü',
      'drechslera': 'Drechslera Küfü',
      'fusarium': 'Fusarium Küfü',
    };
    
    // Küçük harfe çevir ve tercüme et
    String lowerPollen = pollen.toLowerCase().trim();
    return translations[lowerPollen] ?? pollen;
  }

  String _translateFoodName(String food) {
    final translations = {
      // Fruits - Meyveler
      'apple': 'Elma',
      'pear': 'Armut',
      'cherry': 'Kiraz',
      'peach': 'Şeftali',
      'apricot': 'Kayısı',
      'plum': 'Erik',
      'kiwi': 'Kivi',
      'banana': 'Muz',
      'melon': 'Kavun',
      'watermelon': 'Karpuz',
      'orange': 'Portakal',
      'lemon': 'Limon',
      'grapefruit': 'Greyfurt',
      'strawberry': 'Çilek',
      'raspberry': 'Ahududu',
      'blackberry': 'Böğürtlen',
      'blueberry': 'Yaban Mersini',
      'grape': 'Üzüm',
      'pineapple': 'Ananas',
      'mango': 'Mango',
      'papaya': 'Papaya',
      'avocado': 'Avokado',
      
      // Vegetables - Sebzeler
      'tomato': 'Domates',
      'potato': 'Patates',
      'carrot': 'Havuç',
      'celery': 'Kereviz',
      'onion': 'Soğan',
      'garlic': 'Sarımsak',
      'pepper': 'Biber',
      'cucumber': 'Salatalık',
      'lettuce': 'Marul',
      'spinach': 'Ispanak',
      'cabbage': 'Lahana',
      'broccoli': 'Brokoli',
      'cauliflower': 'Karnabahar',
      'eggplant': 'Patlıcan',
      'zucchini': 'Kabak',
      'radish': 'Turp',
      'beetroot': 'Pancar',
      'turnip': 'Şalgam',
      'leek': 'Pırasa',
      'artichoke': 'Enginar',
      'asparagus': 'Kuşkonmaz',
      
      // Nuts - Kuruyemişler
      'hazelnut': 'Fındık',
      'walnut': 'Ceviz',
      'almond': 'Badem',
      'peanut': 'Yer Fıstığı',
      'pistachio': 'Antep Fıstığı',
      'cashew': 'Kaju',
      'brazil nut': 'Brezilya Fıstığı',
      'pecan': 'Pekan Cevizi',
      'chestnut': 'Kestane',
      'pine nut': 'Çam Fıstığı',
      
      // Herbs and Spices - Baharatlar ve Otlar
      'parsley': 'Maydanoz',
      'dill': 'Dereotu',
      'mint': 'Nane',
      'basil': 'Fesleğen',
      'oregano': 'Kekik',
      'thyme': 'Kekik',
      'rosemary': 'Biberiye',
      'sage': 'Adaçayı',
      'coriander': 'Kişniş',
      'cumin': 'Kimyon',
      'fennel': 'Rezene',
      'anise': 'Anason',
      'cardamom': 'Kakule',
      'cinnamon': 'Tarçın',
      'clove': 'Karanfil',
      'ginger': 'Zencefil',
      'turmeric': 'Zerdeçal',
      'paprika': 'Kırmızı Biber',
      'black pepper': 'Karabiber',
      'white pepper': 'Beyaz Biber',
      
      // Grains and Legumes - Tahıllar ve Baklagiller
      'wheat': 'Buğday',
      'rice': 'Pirinç',
      'oat': 'Yulaf',
      'barley': 'Arpa',
      'rye': 'Çavdar',
      'corn': 'Mısır',
      'soy': 'Soya',
      'lentil': 'Mercimek',
      'chickpea': 'Nohut',
      'bean': 'Fasulye',
      'pea': 'Bezelye',
      'graminales': 'Buğdaylar',
      
      // Seeds - Tohumlar
      'sunflower seed': 'Ayçiçeği Tohumu',
      'pumpkin seed': 'Kabak Çekirdeği',
      'sesame': 'Susam',
      'flax seed': 'Keten Tohumu',
      'chia seed': 'Chia Tohumu',
      'poppy seed': 'Haşhaş Tohumu',
    };
    
    String lowerFood = food.toLowerCase().trim();
    return translations[lowerFood] ?? food;
  }

  Widget _buildRiskItem(String title, String risk) {
    Color color;
    IconData icon;
    
    switch (risk.toLowerCase()) {
      case 'high':
        color = Colors.red;
        icon = Icons.warning;
        break;
      case 'medium':
      case 'moderate':
        color = Colors.orange;
        icon = Icons.info;
        break;
      case 'low':
      default:
        color = Colors.green;
        icon = Icons.check_circle;
        break;
    }
    
    return Row(
      children: [
        Icon(icon, size: 20, color: color),
        const SizedBox(width: 8),
        Text(
          '$title: ',
          style: TextStyle(
            fontSize: 14,
            color: Colors.grey.shade700,
            fontWeight: FontWeight.w500,
          ),
        ),
        Expanded(
          child: Text(
            _translateRiskLevel(risk),
            style: TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.w600,
              color: color,
            ),
          ),
        ),
      ],
    );
  }

  void _showShareDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Sonuçları Paylaş'),
        content: const Text(
          'Bu özellik yakında aktif olacak. Tahmin sonuçlarınızı paylaşabileceksiniz.',
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