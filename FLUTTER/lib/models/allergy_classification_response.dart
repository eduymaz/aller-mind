class AllergyClassificationResponse {
  final String assignmentReason;
  final EnvironmentalSensitivityFactors environmentalSensitivityFactors;
  final String groupDescription;
  final int groupId;
  final String groupName;
  final ImmunologicProfile immunologicProfile;
  final double modelWeight;
  final PersonalRiskModifiers personalRiskModifiers;
  final PollenSpecificRisks pollenSpecificRisks;
  final RecommendationAdjustments recommendationAdjustments;
  final String userPreferenceId;

  AllergyClassificationResponse({
    required this.assignmentReason,
    required this.environmentalSensitivityFactors,
    required this.groupDescription,
    required this.groupId,
    required this.groupName,
    required this.immunologicProfile,
    required this.modelWeight,
    required this.personalRiskModifiers,
    required this.pollenSpecificRisks,
    required this.recommendationAdjustments,
    required this.userPreferenceId,
  });

  factory AllergyClassificationResponse.fromJson(Map<String, dynamic> json) {
    return AllergyClassificationResponse(
      assignmentReason: json['assignmentReason'] ?? '',
      environmentalSensitivityFactors: EnvironmentalSensitivityFactors.fromJson(json['environmentalSensitivityFactors'] ?? {}),
      groupDescription: json['groupDescription'] ?? '',
      groupId: json['groupId'] ?? 0,
      groupName: json['groupName'] ?? '',
      immunologicProfile: ImmunologicProfile.fromJson(json['immunologicProfile'] ?? {}),
      modelWeight: (json['modelWeight'] ?? 0.0).toDouble(),
      personalRiskModifiers: PersonalRiskModifiers.fromJson(json['personalRiskModifiers'] ?? {}),
      pollenSpecificRisks: PollenSpecificRisks.fromJson(json['pollenSpecificRisks'] ?? {}),
      recommendationAdjustments: RecommendationAdjustments.fromJson(json['recommendationAdjustments'] ?? {}),
      userPreferenceId: json['userPreferenceId'] ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'assignmentReason': assignmentReason,
      'environmentalSensitivityFactors': environmentalSensitivityFactors.toJson(),
      'groupDescription': groupDescription,
      'groupId': groupId,
      'groupName': groupName,
      'immunologicProfile': immunologicProfile.toJson(),
      'modelWeight': modelWeight,
      'personalRiskModifiers': personalRiskModifiers.toJson(),
      'pollenSpecificRisks': pollenSpecificRisks.toJson(),
      'recommendationAdjustments': recommendationAdjustments.toJson(),
      'userPreferenceId': userPreferenceId,
    };
  }
}

class EnvironmentalSensitivityFactors {
  final bool petDanderSensitivity;
  final bool moldSensitivity;
  final bool airPollutionSensitivity;
  final bool dustMiteSensitivity;
  final bool smokeSensitivity;

  EnvironmentalSensitivityFactors({
    required this.petDanderSensitivity,
    required this.moldSensitivity,
    required this.airPollutionSensitivity,
    required this.dustMiteSensitivity,
    required this.smokeSensitivity,
  });

  factory EnvironmentalSensitivityFactors.fromJson(Map<String, dynamic> json) {
    return EnvironmentalSensitivityFactors(
      petDanderSensitivity: json['pet_dander_sensitivity'] ?? false,
      moldSensitivity: json['mold_sensitivity'] ?? false,
      airPollutionSensitivity: json['air_pollution_sensitivity'] ?? false,
      dustMiteSensitivity: json['dust_mite_sensitivity'] ?? false,
      smokeSensitivity: json['smoke_sensitivity'] ?? false,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'pet_dander_sensitivity': petDanderSensitivity,
      'mold_sensitivity': moldSensitivity,
      'air_pollution_sensitivity': airPollutionSensitivity,
      'dust_mite_sensitivity': dustMiteSensitivity,
      'smoke_sensitivity': smokeSensitivity,
    };
  }
}

class ImmunologicProfile {
  // Ana 4 alan (mevcut)
  final String inflammatoryResponse;
  final String igeLevel;
  final String antihistamineResponse;
  final String seasonalPattern;
  
  // SEVERE_ALLERGIC grubu için ek alanlar
  final String? th2Activation;
  final String? mastCellDegranulation;
  final List<String>? cytokineProfile;
  
  // GENETIC_PREDISPOSITION grubu için ek alanlar
  final bool? atopicStructure;
  final bool? familyLoading;
  final String? igeProductionCapacity;
  final bool? th1Th2Imbalance;
  final String? sensitizationRisk;
  
  // UNDIAGNOSED grubu için ek alanlar
  final String? sensitization;
  final bool? environmentalTriggers;
  
  // VULNERABLE_POPULATION grubu için ek alanlar
  final String? immuneSystem;
  final String? immuneTolerance;
  final String? multisystemRisk;

  ImmunologicProfile({
    required this.inflammatoryResponse,
    required this.igeLevel,
    required this.antihistamineResponse,
    required this.seasonalPattern,
    this.th2Activation,
    this.mastCellDegranulation,
    this.cytokineProfile,
    this.atopicStructure,
    this.familyLoading,
    this.igeProductionCapacity,
    this.th1Th2Imbalance,
    this.sensitizationRisk,
    this.sensitization,
    this.environmentalTriggers,
    this.immuneSystem,
    this.immuneTolerance,
    this.multisystemRisk,
  });

  factory ImmunologicProfile.fromJson(Map<String, dynamic> json) {
    return ImmunologicProfile(
      inflammatoryResponse: json['inflammatory_response'] ?? '',
      igeLevel: json['ige_level'] ?? '',
      antihistamineResponse: json['antihistamine_response'] ?? '',
      seasonalPattern: json['seasonal_pattern'] ?? '',
      th2Activation: json['th2_activation'],
      mastCellDegranulation: json['mast_cell_degranulation'],
      cytokineProfile: json['cytokine_profile'] != null 
          ? List<String>.from(json['cytokine_profile']) 
          : null,
      atopicStructure: json['atopic_structure'],
      familyLoading: json['family_loading'],
      igeProductionCapacity: json['ige_production_capacity'],
      th1Th2Imbalance: json['th1_th2_imbalance'],
      sensitizationRisk: json['sensitization_risk'],
      sensitization: json['sensitization'],
      environmentalTriggers: json['environmental_triggers'],
      immuneSystem: json['immune_system'],
      immuneTolerance: json['immune_tolerance'],
      multisystemRisk: json['multisystem_risk'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'inflammatory_response': inflammatoryResponse,
      'ige_level': igeLevel,
      'antihistamine_response': antihistamineResponse,
      'seasonal_pattern': seasonalPattern,
      if (th2Activation != null) 'th2_activation': th2Activation,
      if (mastCellDegranulation != null) 'mast_cell_degranulation': mastCellDegranulation,
      if (cytokineProfile != null) 'cytokine_profile': cytokineProfile,
      if (atopicStructure != null) 'atopic_structure': atopicStructure,
      if (familyLoading != null) 'family_loading': familyLoading,
      if (igeProductionCapacity != null) 'ige_production_capacity': igeProductionCapacity,
      if (th1Th2Imbalance != null) 'th1_th2_imbalance': th1Th2Imbalance,
      if (sensitizationRisk != null) 'sensitization_risk': sensitizationRisk,
      if (sensitization != null) 'sensitization': sensitization,
      if (environmentalTriggers != null) 'environmental_triggers': environmentalTriggers,
      if (immuneSystem != null) 'immune_system': immuneSystem,
      if (immuneTolerance != null) 'immune_tolerance': immuneTolerance,
      if (multisystemRisk != null) 'multisystem_risk': multisystemRisk,
    };
  }
}

class PersonalRiskModifiers {
  final double seasonalModifier;
  final double environmentalAmplifier;
  final double comorbidityFactor;
  final double baseSensitivity;

  PersonalRiskModifiers({
    required this.seasonalModifier,
    required this.environmentalAmplifier,
    required this.comorbidityFactor,
    required this.baseSensitivity,
  });

  factory PersonalRiskModifiers.fromJson(Map<String, dynamic> json) {
    return PersonalRiskModifiers(
      seasonalModifier: (json['seasonal_modifier'] ?? 0.0).toDouble(),
      environmentalAmplifier: (json['environmental_amplifier'] ?? 0.0).toDouble(),
      comorbidityFactor: (json['comorbidity_factor'] ?? 0.0).toDouble(),
      baseSensitivity: (json['base_sensitivity'] ?? 0.0).toDouble(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'seasonal_modifier': seasonalModifier,
      'environmental_amplifier': environmentalAmplifier,
      'comorbidity_factor': comorbidityFactor,
      'base_sensitivity': baseSensitivity,
    };
  }
}

class PollenSpecificRisks {
  final List<String> highRiskPollens;
  final List<String> crossReactiveFoods;
  final List<String> moderateRiskPollens;

  PollenSpecificRisks({
    required this.highRiskPollens,
    required this.crossReactiveFoods,
    required this.moderateRiskPollens,
  });

  factory PollenSpecificRisks.fromJson(Map<String, dynamic> json) {
    return PollenSpecificRisks(
      highRiskPollens: List<String>.from(json['high_risk_pollens'] ?? []),
      crossReactiveFoods: List<String>.from(json['cross_reactive_foods'] ?? []),
      moderateRiskPollens: List<String>.from(json['moderate_risk_pollens'] ?? []),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'high_risk_pollens': highRiskPollens,
      'cross_reactive_foods': crossReactiveFoods,
      'moderate_risk_pollens': moderateRiskPollens,
    };
  }
}

class RecommendationAdjustments {
  final String environmentalControlLevel;
  final String medicationPriority;
  final String monitoringFrequency;
  final bool emergencyPreparedness;

  RecommendationAdjustments({
    required this.environmentalControlLevel,
    required this.medicationPriority,
    required this.monitoringFrequency,
    required this.emergencyPreparedness,
  });

  factory RecommendationAdjustments.fromJson(Map<String, dynamic> json) {
    return RecommendationAdjustments(
      environmentalControlLevel: json['environmental_control_level'] ?? '',
      medicationPriority: json['medication_priority'] ?? '',
      monitoringFrequency: json['monitoring_frequency'] ?? '',
      emergencyPreparedness: json['emergency_preparedness'] ?? false,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'environmental_control_level': environmentalControlLevel,
      'medication_priority': medicationPriority,
      'monitoring_frequency': monitoringFrequency,
      'emergency_preparedness': emergencyPreparedness,
    };
  }
}