import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/allermind_provider.dart';
import '../models/allermind_response.dart';

class ResultScreen extends StatelessWidget {
  const ResultScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Allerji Risk Sonucu'),
        backgroundColor: Colors.teal,
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () {
              // Yeniden tahmin al
              Navigator.of(context).popUntil((route) => route.isFirst);
            },
          ),
        ],
      ),
      body: Consumer<AllerMindProvider>(
        builder: (context, provider, child) {
          final response = provider.currentResponse;
          
          if (response == null) {
            return const Center(
              child: Text('Sonuç bulunamadı'),
            );
          }

          return SingleChildScrollView(
            child: Column(
              children: [
                // Ana Risk Göstergesi
                _buildMainRiskIndicator(response),
                
                // Detaylı Bilgiler
                _buildDetailedInfo(response),
                
                // Çevresel Veriler
                _buildEnvironmentalData(response),
                
                // Grup Sonuçları
                _buildGroupResults(response),
                
                // Tavsiyeler
                _buildRecommendations(response),
                
                const SizedBox(height: 24),
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _buildMainRiskIndicator(AllerMindResponse response) {
    return Container(
      margin: const EdgeInsets.all(16),
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        gradient: _getGradientForRiskLevel(response.overallRiskLevel),
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1),
            blurRadius: 10,
            offset: const Offset(0, 5),
          ),
        ],
      ),
      child: Column(
        children: [
          // Risk emoji ve görsel
          Container(
            width: 150,
            height: 150,
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(15),
              color: Colors.white.withOpacity(0.2),
            ),
            child: ClipRRect(
              borderRadius: BorderRadius.circular(15),
              child: Image.asset(
                response.getImageAsset(),
                fit: BoxFit.cover,
                errorBuilder: (context, error, stackTrace) {
                  return Container(
                    color: Colors.white.withOpacity(0.3),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text(
                          response.overallRiskEmoji ?? '📊',
                          style: const TextStyle(fontSize: 60),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          response.overallRiskLevel ?? 'Bilinmeyen',
                          style: const TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ],
                    ),
                  );
                },
              ),
            ),
          ),
          
          const SizedBox(height: 20),
          
          // Risk seviyesi
          Text(
            response.overallRiskLevel ?? 'Bilinmeyen Risk',
            style: const TextStyle(
              fontSize: 28,
              fontWeight: FontWeight.bold,
              color: Colors.white,
            ),
          ),
          
          const SizedBox(height: 8),
          
          // Risk skoru
          if (response.overallRiskScore != null)
            Text(
              'Risk Skoru: ${response.overallRiskScore!.toStringAsFixed(1)}',
              style: const TextStyle(
                fontSize: 16,
                color: Colors.white70,
              ),
            ),
        ],
      ),
    );
  }

  Widget _buildDetailedInfo(AllerMindResponse response) {
    final location = response.modelPrediction?.location;
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Konum Bilgileri',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: Colors.teal,
              ),
            ),
            const SizedBox(height: 12),
            if (location != null) ...[
              _buildInfoRow('Şehir', location.cityName ?? 'Bilinmeyen'),
              _buildInfoRow('Enlem', location.latitude?.toStringAsFixed(4) ?? '-'),
              _buildInfoRow('Boylam', location.longitude?.toStringAsFixed(4) ?? '-'),
            ],
            if (response.userGroup != null) ...[
              const Divider(height: 24),
              _buildInfoRow('Kullanıcı Grubu', response.userGroup!.groupName),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildEnvironmentalData(AllerMindResponse response) {
    final envData = response.modelPrediction?.environmentalData;
    if (envData == null || envData.isEmpty) return const SizedBox.shrink();

    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Çevresel Veriler',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: Colors.teal,
              ),
            ),
            const SizedBox(height: 12),
            _buildInfoRow('Sıcaklık', '${envData['temperature'] ?? '-'} °C'),
            _buildInfoRow('Nem', '${envData['humidity'] ?? '-'}%'),
            _buildInfoRow('Polen İndeksi', '${envData['pollen_index'] ?? '-'}'),
            _buildInfoRow('PM10', '${envData['pm10'] ?? '-'} μg/m³'),
            _buildInfoRow('PM2.5', '${envData['pm2_5'] ?? '-'} μg/m³'),
            _buildInfoRow('Rüzgar Hızı', '${envData['wind_speed'] ?? '-'} km/h'),
            _buildInfoRow('Yağış', '${envData['precipitation'] ?? '-'} mm'),
            _buildInfoRow('Bulut Örtüsü', '${envData['cloud_cover'] ?? '-'}%'),
          ],
        ),
      ),
    );
  }

  Widget _buildGroupResults(AllerMindResponse response) {
    final predictions = response.modelPrediction?.predictions;
    if (predictions == null || predictions.isEmpty) return const SizedBox.shrink();

    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Grup Bazlı Risk Analizi',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: Colors.teal,
              ),
            ),
            const SizedBox(height: 16),
            ...predictions.map((group) => Container(
              margin: const EdgeInsets.only(bottom: 12),
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: _getRiskColor(group.riskLevel).withOpacity(0.1),
                borderRadius: BorderRadius.circular(8),
                border: Border.all(
                  color: _getRiskColor(group.riskLevel).withOpacity(0.3),
                ),
              ),
              child: Row(
                children: [
                  Text(
                    group.riskEmoji ?? '📊',
                    style: const TextStyle(fontSize: 24),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          group.groupName ?? 'Bilinmeyen Grup',
                          style: const TextStyle(
                            fontWeight: FontWeight.bold,
                            fontSize: 14,
                          ),
                        ),
                        Text(
                          '${group.riskLevel ?? 'Bilinmeyen'} - ${group.predictionValue?.toStringAsFixed(2) ?? '-'}',
                          style: TextStyle(
                            color: _getRiskColor(group.riskLevel),
                            fontWeight: FontWeight.w500,
                          ),
                        ),
                      ],
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

  Widget _buildRecommendations(AllerMindResponse response) {
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Row(
              children: [
                Icon(Icons.lightbulb_outline, color: Colors.orange),
                SizedBox(width: 8),
                Text(
                  'Öneriler',
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: Colors.teal,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.blue.shade50,
                borderRadius: BorderRadius.circular(8),
                border: Border.all(color: Colors.blue.shade200),
              ),
              child: Text(
                response.getRecommendation(),
                style: const TextStyle(
                  fontSize: 15,
                  height: 1.4,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildInfoRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        children: [
          SizedBox(
            width: 120,
            child: Text(
              label,
              style: const TextStyle(
                fontWeight: FontWeight.w500,
                color: Colors.grey,
              ),
            ),
          ),
          Expanded(
            child: Text(
              value,
              style: const TextStyle(fontWeight: FontWeight.w500),
            ),
          ),
        ],
      ),
    );
  }

  LinearGradient _getGradientForRiskLevel(String? riskLevel) {
    switch (riskLevel?.toUpperCase()) {
      case 'DÜŞÜK':
        return const LinearGradient(
          colors: [Color(0xFF4CAF50), Color(0xFF2E7D32)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        );
      case 'ORTA':
        return const LinearGradient(
          colors: [Color(0xFFFF9800), Color(0xFFE65100)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        );
      case 'ORTA-YÜKSEK':
        return const LinearGradient(
          colors: [Color(0xFFFF5722), Color(0xFFBF360C)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        );
      case 'YÜKSEK':
        return const LinearGradient(
          colors: [Color(0xFFF44336), Color(0xFFC62828)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        );
      case 'ÇOK YÜKSEK':
        return const LinearGradient(
          colors: [Color(0xFF9C27B0), Color(0xFF4A148C)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        );
      default:
        return const LinearGradient(
          colors: [Color(0xFF607D8B), Color(0xFF37474F)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        );
    }
  }

  Color _getRiskColor(String? riskLevel) {
    switch (riskLevel?.toUpperCase()) {
      case 'DÜŞÜK':
        return Colors.green;
      case 'ORTA':
        return Colors.orange;
      case 'ORTA-YÜKSEK':
        return Colors.deepOrange;
      case 'YÜKSEK':
        return Colors.red;
      case 'ÇOK YÜKSEK':
        return Colors.purple;
      default:
        return Colors.grey;
    }
  }
}