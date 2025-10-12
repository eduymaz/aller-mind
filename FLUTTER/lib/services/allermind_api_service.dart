import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/allermind_response.dart';
import '../models/user_settings.dart';

class AllerMindApiService {
  // Use relative URL - nginx will proxy to model-service
  static const String baseUrl = '';
  static const String predictionEndpoint = '/api/v1/model/prediction';

  /// AllerMind model prediction'ı çağırır
  /// [lat] Enlem koordinatı
  /// [lon] Boylam koordinatı 
  /// [userSettings] Kullanıcı ayarları
  static Future<AllerMindResponse> getPrediction({
    required String lat,
    required String lon,
    required UserSettings userSettings,
  }) async {
    try {
      final url = Uri.parse('$baseUrl$predictionEndpoint?lat=$lat&lon=$lon');
      
      final response = await http.post(
        url,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: jsonEncode(userSettings.toJson()),
      );

      if (response.statusCode == 200) {
        final jsonData = jsonDecode(response.body);
        return AllerMindResponse.fromJson(jsonData);
      } else {
        throw Exception('API çağrısı başarısız: ${response.statusCode} - ${response.body}');
      }
    } catch (e) {
      throw Exception('Network hatası: $e');
    }
  }

  /// Health check endpoint'ini çağırır
  static Future<bool> checkHealth() async {
    try {
      final url = Uri.parse('$baseUrl/api/v1/model/health');
      final response = await http.get(url);
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }
}