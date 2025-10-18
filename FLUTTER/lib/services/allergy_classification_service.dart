import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/allergy_profile_request.dart';
import '../models/allergy_classification_response.dart';
import '../models/user_profile_response.dart';
import '../config/app_config.dart';
import 'allermind_api_service.dart';

class AllergyClassificationService {
  static String get _baseUrl => AppConfig().userPreferenceServiceUrl;
  static const String _classificationEndpoint = '/api/v1/allergy-classification/classify';

  /// Classify user's allergy profile and get group assignment
  static Future<AllergyClassificationResponse> classifyAllergyProfile(
      AllergyProfileRequest request) async {
    try {
      final url = Uri.parse('$_baseUrl$_classificationEndpoint');
      
      final response = await http.post(
        url,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: jsonEncode(request.toJson()),
      );

      if (response.statusCode == 200) {
        final Map<String, dynamic> jsonResponse = jsonDecode(response.body);
        return AllergyClassificationResponse.fromJson(jsonResponse);
      } else if (response.statusCode == 400) {
        throw AllergyClassificationException(
          'Geçersiz veri gönderildi: ${response.body}',
          response.statusCode,
        );
      } else if (response.statusCode == 404) {
        throw AllergyClassificationException(
          'Servis bulunamadı. Lütfen sunucu durumunu kontrol edin.',
          response.statusCode,
        );
      } else if (response.statusCode == 500) {
        throw AllergyClassificationException(
          'Sunucu hatası. Lütfen daha sonra tekrar deneyin.',
          response.statusCode,
        );
      } else {
        throw AllergyClassificationException(
          'Beklenmeyen hata: ${response.statusCode}',
          response.statusCode,
        );
      }
    } catch (e) {
      if (e is AllergyClassificationException) {
        rethrow;
      }
      
      // Network or other errors
      throw AllergyClassificationException(
        'Bağlantı hatası: Sunucuya erişilemiyor. İnternet bağlantınızı ve sunucu durumunu kontrol edin.',
        -1,
      );
    }
  }

  /// Test server connection
  static Future<bool> testConnection() async {
    try {
      final url = Uri.parse('$_baseUrl/health');
      final response = await http.get(url).timeout(
        const Duration(seconds: 5),
      );
      
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }

  /// Get user profile by user preference ID
  static Future<UserProfileResponse> getUserProfile(String userPreferenceId) async {
    try {
      final url = Uri.parse('$_baseUrl/api/v1/allergy-classification/user/$userPreferenceId');
      
      final response = await http.get(
        url,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        final Map<String, dynamic> jsonResponse = jsonDecode(response.body);
        return UserProfileResponse.fromJson(jsonResponse);
      } else if (response.statusCode == 404) {
        throw AllergyClassificationException(
          'Kullanıcı profili bulunamadı.',
          response.statusCode,
        );
      } else if (response.statusCode == 500) {
        throw AllergyClassificationException(
          'Sunucu hatası. Lütfen daha sonra tekrar deneyin.',
          response.statusCode,
        );
      } else {
        throw AllergyClassificationException(
          'Beklenmeyen hata: ${response.statusCode}',
          response.statusCode,
        );
      }
    } catch (e) {
      if (e is AllergyClassificationException) {
        rethrow;
      }
      
      // Network or other errors
      throw AllergyClassificationException(
        'Bağlantı hatası: Sunucuya erişilemiyor. İnternet bağlantınızı ve sunucu durumunu kontrol edin.',
        -1,
      );
    }
  }

  /// Get prediction for user based on location and user ID
  static Future<Map<String, dynamic>> getPrediction({
    required double latitude,
    required double longitude,
    required String userId,
  }) async {
    try {
      // Use the full model service base URL (local development uses http://localhost:8484)
      final url = Uri.parse(
        '${AllerMindApiService.baseUrl}/api/v1/model/prediction?lat=$latitude&lon=$longitude&userId=$userId'
      );
      
      final response = await http.get(
        url,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        final Map<String, dynamic> jsonResponse = jsonDecode(response.body);
        return jsonResponse;
      } else if (response.statusCode == 400) {
        throw AllergyClassificationException(
          'Geçersiz parametreler: ${response.body}',
          response.statusCode,
        );
      } else if (response.statusCode == 404) {
        throw AllergyClassificationException(
          'Kullanıcı bulunamadı veya servis bulunamadı.',
          response.statusCode,
        );
      } else if (response.statusCode == 500) {
        throw AllergyClassificationException(
          'Sunucu hatası. Lütfen daha sonra tekrar deneyin.',
          response.statusCode,
        );
      } else {
        throw AllergyClassificationException(
          'Beklenmeyen hata: ${response.statusCode}',
          response.statusCode,
        );
      }
    } catch (e) {
      if (e is AllergyClassificationException) {
        rethrow;
      }
      throw AllergyClassificationException(
        'Ağ hatası: $e',
        0,
      );
    }
  }

  /// Validate request data before sending
  static bool validateRequest(AllergyProfileRequest request) {
    // Basic validation
    if (request.age <= 0 || request.age > 150) {
      return false;
    }
    
    if (request.gender.isEmpty) {
      return false;
    }
    
    if (request.clinicalDiagnosis.isEmpty) {
      return false;
    }
    
    if (request.latitude < -90 || request.latitude > 90) {
      return false;
    }
    
    if (request.longitude < -180 || request.longitude > 180) {
      return false;
    }
    
    return true;
  }
}

class AllergyClassificationException implements Exception {
  final String message;
  final int statusCode;

  const AllergyClassificationException(this.message, this.statusCode);

  @override
  String toString() => 'AllergyClassificationException: $message (Status: $statusCode)';
}

/// Helper class for available options in the form
class AllergyFormOptions {
  static const List<String> genders = ['male', 'female', 'other'];
  
  static const Map<String, String> genderLabels = {
    'male': 'Erkek',
    'female': 'Kadın', 
    'other': 'Bilinmiyor',
  };

  static const List<String> clinicalDiagnoses = [
    'none',
    'mild_moderate_allergy',
    'severe_allergy',
    'asthma',
  ];

  static const Map<String, String> clinicalDiagnosisLabels = {
    'none': 'Alerji Tanısı Olmayan',
    'mild_moderate_allergy': 'Hafif/Orta Derece Alerjik Durum',
    'severe_allergy': 'Şiddetli Alerjik Durum',
    'asthma': 'Çocuk/Kronik Rahatsız',
  };

  static const List<String> availableMedications = [
    'antihistamine',
    'nasal_spray',
    'bronchodilator',
    'corticosteroid',
    'epinephrine',
    'leukotriene_modifier',
  ];

  static const Map<String, String> medicationLabels = {
    'antihistamine': 'Antihistaminik',
    'nasal_spray': 'Burun spreyi',
    'bronchodilator': 'Bronkodilatör',
    'corticosteroid': 'Kortikosteroid',
    'epinephrine': 'Epinefrin',
    'leukotriene_modifier': 'Lökotriin modifikatörü',
  };

  static const Map<String, String> environmentalTriggerLabels = {
    'air_pollution': 'Hava kirliliği',
    'dust_mites': 'Ev tozu akarı',
    'pet_dander': 'Hayvan tüyü',
    'smoke': 'Duman',
    'mold': 'Küf',
  };

  static const Map<String, String> foodAllergyLabels = {
    'apple': 'Elma',
    'shellfish': 'Kabuklu deniz ürünleri',
    'nuts': 'Fındık/Fıstık',
  };

  static const Map<String, String> treePollenLabels = {
    'pine': 'Çam',
    'olive': 'Zeytin',
    'birch': 'Huş ağacı',
  };

  static const Map<String, String> grassPollenLabels = {
    'graminales': 'Çim poleni',
  };

  static const Map<String, String> weedPollenLabels = {
    'mugwort': 'Pelin',
    'ragweed': 'Karaot',
  };

  static const Map<String, String> allergicReactionLabels = {
    'severe_asthma': 'Akut Şiddetli Astım Atak',
    'hospitalization': 'Hastanede Tedavi/İzlem Gerekliliği',
    'anaphylaxis': 'Anafilaksi Durumu',
  };

  /// Get prediction for user based on location and user ID
  static Future<Map<String, dynamic>> getPrediction({
    required double latitude,
    required double longitude,
    required String userId,
  }) async {
    try {
      final url = Uri.parse(
        '/api/v1/model/prediction?lat=$latitude&lon=$longitude&userId=$userId'
      );
      
      final response = await http.get(
        url,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        final Map<String, dynamic> jsonResponse = jsonDecode(response.body);
        return jsonResponse;
      } else if (response.statusCode == 400) {
        throw AllergyClassificationException(
          'Geçersiz parametreler: ${response.body}',
          response.statusCode,
        );
      } else if (response.statusCode == 404) {
        throw AllergyClassificationException(
          'Kullanıcı bulunamadı veya servis bulunamadı.',
          response.statusCode,
        );
      } else if (response.statusCode == 500) {
        throw AllergyClassificationException(
          'Sunucu hatası. Lütfen daha sonra tekrar deneyin.',
          response.statusCode,
        );
      } else {
        throw AllergyClassificationException(
          'Beklenmeyen hata: ${response.statusCode}',
          response.statusCode,
        );
      }
    } catch (e) {
      if (e is AllergyClassificationException) {
        rethrow;
      }
      throw AllergyClassificationException(
        'Ağ hatası: $e',
        0,
      );
    }
  }
}