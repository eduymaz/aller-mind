import 'user_settings.dart';

class AllerMindResponse {
  final String? predictionId;
  final String? userId;
  final String? lat;
  final String? lon;
  final bool? success;
  final String? message;
  final double? overallRiskScore;
  final String? overallRiskLevel;
  final String? overallRiskEmoji;
  final int? overallRiskCode;
  final ModelPredictionResponse? modelPrediction;
  final UserGroup? userGroup;
  final String? recommendation;

  AllerMindResponse({
    this.predictionId,
    this.userId,
    this.lat,
    this.lon,
    this.success,
    this.message,
    this.overallRiskScore,
    this.overallRiskLevel,
    this.overallRiskEmoji,
    this.overallRiskCode,
    this.modelPrediction,
    this.userGroup,
    this.recommendation,
  });

  factory AllerMindResponse.fromJson(Map<String, dynamic> json) {
    return AllerMindResponse(
      predictionId: json['predictionId'],
      userId: json['userId'],
      lat: json['lat'],
      lon: json['lon'],
      success: json['success'],
      message: json['message'],
      overallRiskScore: json['overallRiskScore']?.toDouble(),
      overallRiskLevel: json['overallRiskLevel'],
      overallRiskEmoji: json['overallRiskEmoji'],
      overallRiskCode: json['overallRiskCode'],
      modelPrediction: json['modelPrediction'] != null 
          ? ModelPredictionResponse.fromJson(json['modelPrediction'])
          : null,
      userGroup: json['userGroup'] != null 
          ? UserGroup.fromApiJson(json['userGroup'])
          : null,
      recommendation: json['recommendation'],
    );
  }

  /// Tavsiye mesajını döndürür
  String getRecommendation() {
    // Önce API'den gelen recommendation'ı kontrol et
    if (recommendation != null && recommendation!.isNotEmpty) {
      return recommendation!;
    }
    
    // Eğer yoksa, risk seviyesine göre generate et
    if (modelPrediction?.predictions != null && modelPrediction!.predictions!.isNotEmpty) {
      final highestRisk = modelPrediction!.predictions!.reduce((a, b) => 
          a.predictionValue! > b.predictionValue! ? a : b);
      return _generateRecommendation(highestRisk.riskLevel, highestRisk.predictionValue);
    }
    return "Veri yetersiz";
  }

  String _generateRecommendation(String? riskLevel, double? value) {
    switch (riskLevel) {
      case "DÜŞÜK":
        return "Dışarı çıkabilirsiniz, genel önlemler yeterli";
      case "ORTA":
        return "Dikkatli olun, maske kullanımı önerilir";
      case "ORTA-YÜKSEK":
        return "Mümkünse evde kalın, çıkarken mutlaka maske takın";
      case "YÜKSEK":
        return "Dışarı çıkmayın, ilaçlarınızı hazır bulundurun";
      case "ÇOK YÜKSEK":
        return "Kesinlikle dışarı çıkmayın, acil durumda doktora başvurun";
      default:
        return "Risk değerlendirmesi yapılamadı";
    }
  }

  /// Risk seviyesine göre uygun görsel dosya adını döndürür
  String getImageAsset() {
    if (overallRiskLevel == null) return 'IMAGE/first.png';
    
    switch (overallRiskLevel!.toUpperCase()) {
      case 'DÜŞÜK':
        return 'IMAGE/iyi.png';
      case 'ORTA':
        return 'IMAGE/orta.png';
      case 'ORTA-YÜKSEK':
      case 'YÜKSEK':
      case 'ÇOK YÜKSEK':
        return 'IMAGE/risk.png';
      default:
        return 'IMAGE/first.png';
    }
  }
}

class ModelPredictionResponse {
  final bool? success;
  final String? message;
  final String? error;
  final LocationInfo? location;
  final UserGroup? userGroup;
  final List<GroupResult>? predictions;
  final PredictionSummary? summary;
  final Map<String, dynamic>? environmentalData;
  final String? timestamp;

  ModelPredictionResponse({
    this.success,
    this.message,
    this.error,
    this.location,
    this.userGroup,
    this.predictions,
    this.summary,
    this.environmentalData,
    this.timestamp,
  });

  factory ModelPredictionResponse.fromJson(Map<String, dynamic> json) {
    return ModelPredictionResponse(
      success: json['success'],
      message: json['message'],
      error: json['error'],
      location: json['location'] != null 
          ? LocationInfo.fromJson(json['location'])
          : null,
      userGroup: json['user_group'] != null 
          ? UserGroup.fromApiJson(json['user_group'])
          : null,
      predictions: json['predictions'] != null
          ? (json['predictions'] as List).map((e) => GroupResult.fromJson(e)).toList()
          : null,
      summary: json['summary'] != null 
          ? PredictionSummary.fromJson(json['summary'])
          : null,
      environmentalData: json['environmental_data'],
      timestamp: json['timestamp'],
    );
  }
}

class LocationInfo {
  final double? latitude;
  final double? longitude;
  final String? cityName;

  LocationInfo({
    this.latitude,
    this.longitude,
    this.cityName,
  });

  factory LocationInfo.fromJson(Map<String, dynamic> json) {
    return LocationInfo(
      latitude: json['latitude']?.toDouble(),
      longitude: json['longitude']?.toDouble(),
      cityName: json['city_name'], // API'de city_name kullanılıyor
    );
  }
}

class GroupResult {
  final int? groupId;
  final String? groupName;
  final double? predictionValue;
  final String? riskLevel;
  final String? riskEmoji;
  final int? riskCode;

  GroupResult({
    this.groupId,
    this.groupName,
    this.predictionValue,
    this.riskLevel,
    this.riskEmoji,
    this.riskCode,
  });

  factory GroupResult.fromJson(Map<String, dynamic> json) {
    return GroupResult(
      groupId: json['group_id'],
      groupName: json['group_name'],
      predictionValue: json['prediction_value']?.toDouble(),
      riskLevel: json['risk_level'],
      riskEmoji: json['risk_emoji'],
      riskCode: json['risk_code'],
    );
  }
}

class PredictionSummary {
  final RiskGroup? lowestRisk;
  final RiskGroup? highestRisk;
  final double? averageRisk;

  PredictionSummary({
    this.lowestRisk,
    this.highestRisk,
    this.averageRisk,
  });

  factory PredictionSummary.fromJson(Map<String, dynamic> json) {
    return PredictionSummary(
      lowestRisk: json['lowest_risk'] != null 
          ? RiskGroup.fromJson(json['lowest_risk'])
          : null,
      highestRisk: json['highest_risk'] != null 
          ? RiskGroup.fromJson(json['highest_risk'])
          : null,
      averageRisk: json['average_risk']?.toDouble(),
    );
  }
}

class RiskGroup {
  final int? groupId;
  final String? groupName;
  final double? value;

  RiskGroup({
    this.groupId,
    this.groupName,
    this.value,
  });

  factory RiskGroup.fromJson(Map<String, dynamic> json) {
    return RiskGroup(
      groupId: json['group_id'],
      groupName: json['group_name'],
      value: json['value']?.toDouble(),
    );
  }
}