class PredictionResponse {
  final String predictionId;
  final String userId;
  final bool success;
  final String? message;
  final double overallRiskScore;
  final String overallRiskLevel;
  final String overallRiskEmoji;
  final ModelPrediction modelPrediction;

  PredictionResponse({
    required this.predictionId,
    required this.userId,
    required this.success,
    this.message,
    required this.overallRiskScore,
    required this.overallRiskLevel,
    required this.overallRiskEmoji,
    required this.modelPrediction,
  });

  factory PredictionResponse.fromJson(Map<String, dynamic> json) {
    return PredictionResponse(
      predictionId: json['predictionId'] ?? '',
      userId: json['userId'] ?? '',
      success: json['success'] ?? false,
      message: json['message'],
      overallRiskScore: (json['overallRiskScore'] ?? 0.0).toDouble(),
      overallRiskLevel: json['overallRiskLevel'] ?? 'Orta',
      overallRiskEmoji: json['overallRiskEmoji'] ?? '🟡',
      modelPrediction: ModelPrediction.fromJson(json['modelPrediction'] ?? {}),
    );
  }
}

class ModelPrediction {
  final bool success;
  final String? message;
  final String? error;
  final String timestamp;
  final double confidence;
  final List<String> recommendations;
  final double riskScore;
  final String riskLevel;
  final UserGroup userGroup;
  final Map<String, dynamic>? contributingFactors;
  final Map<String, dynamic>? environmentalRisks;
  final Map<String, dynamic>? personalModifiers;
  final Map<String, dynamic>? immunologicProfile;
  final Map<String, dynamic>? environmentalSensitivityFactors;
  final Map<String, dynamic>? pollenSpecificRisks;
  final double dataQualityScore;
  final String modelVersion;

  ModelPrediction({
    required this.success,
    this.message,
    this.error,
    required this.timestamp,
    required this.confidence,
    required this.recommendations,
    required this.riskScore,
    required this.riskLevel,
    required this.userGroup,
    this.contributingFactors,
    this.environmentalRisks,
    this.personalModifiers,
    this.immunologicProfile,
    this.environmentalSensitivityFactors,
    this.pollenSpecificRisks,
    required this.dataQualityScore,
    required this.modelVersion,
  });

  factory ModelPrediction.fromJson(Map<String, dynamic> json) {
    return ModelPrediction(
      success: json['success'] ?? false,
      message: json['message'],
      error: json['error'],
      timestamp: json['timestamp'] ?? json['predictionTimestamp'] ?? '',
      confidence: (json['confidence'] ?? 0.0).toDouble(),
      recommendations: List<String>.from(json['recommendations'] ?? []),
      riskScore: (json['riskScore'] ?? 0.0).toDouble(),
      riskLevel: json['riskLevel'] ?? 'Orta',
      userGroup: UserGroup.fromJson(json['userGroup'] ?? {}),
      contributingFactors: json['contributingFactors'],
      environmentalRisks: json['environmentalRisks'],
      personalModifiers: json['personalModifiers'],
      immunologicProfile: json['immunologicProfile'],
      environmentalSensitivityFactors: json['environmentalSensitivityFactors'],
      pollenSpecificRisks: json['pollenSpecificRisks'],
      dataQualityScore: (json['dataQualityScore'] ?? 1.0).toDouble(),
      modelVersion: json['modelVersion'] ?? 'Expert-v2.0',
    );
  }
}

class UserGroup {
  final String groupId;
  final String groupName;
  final String description;
  final String assignmentReason;
  final double modelWeight;

  UserGroup({
    required this.groupId,
    required this.groupName,
    required this.description,
    required this.assignmentReason,
    required this.modelWeight,
  });

  factory UserGroup.fromJson(Map<String, dynamic> json) {
    return UserGroup(
      groupId: json['groupId']?.toString() ?? '',
      groupName: json['groupName'] ?? 'Model Grubu',
      description: json['description'] ?? json['groupDescription'] ?? '',
      assignmentReason: json['assignmentReason'] ?? 'Otomatik sınıflandırma',
      modelWeight: (json['modelWeight'] ?? json['riskScore'] ?? 0.0).toDouble(),
    );
  }
}