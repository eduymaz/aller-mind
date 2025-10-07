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
      overallRiskLevel: json['overallRiskLevel'] ?? '',
      overallRiskEmoji: json['overallRiskEmoji'] ?? '',
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
  });

  factory ModelPrediction.fromJson(Map<String, dynamic> json) {
    return ModelPrediction(
      success: json['success'] ?? false,
      message: json['message'],
      error: json['error'],
      timestamp: json['timestamp'] ?? '',
      confidence: (json['confidence'] ?? 0.0).toDouble(),
      recommendations: List<String>.from(json['recommendations'] ?? []),
      riskScore: (json['riskScore'] ?? 0.0).toDouble(),
      riskLevel: json['riskLevel'] ?? '',
      userGroup: UserGroup.fromJson(json['userGroup'] ?? {}),
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
      groupId: json['groupId'] ?? '',
      groupName: json['groupName'] ?? '',
      description: json['description'] ?? '',
      assignmentReason: json['assignmentReason'] ?? '',
      modelWeight: (json['modelWeight'] ?? 0.0).toDouble(),
    );
  }
}