class AllergyProfileRequest {
  final int age;
  final String clinicalDiagnosis;
  final List<String> currentMedications;
  final EnvironmentalTriggers environmentalTriggers;
  final bool familyAllergyHistory;
  final FoodAllergies foodAllergies;
  final String gender;
  final GrassPollenAllergies grassPollenAllergies;
  final double latitude;
  final double longitude;
  final PreviousAllergicReactions previousAllergicReactions;
  final TreePollenAllergies treePollenAllergies;
  final WeedPollenAllergies weedPollenAllergies;

  AllergyProfileRequest({
    required this.age,
    required this.clinicalDiagnosis,
    required this.currentMedications,
    required this.environmentalTriggers,
    required this.familyAllergyHistory,
    required this.foodAllergies,
    required this.gender,
    required this.grassPollenAllergies,
    required this.latitude,
    required this.longitude,
    required this.previousAllergicReactions,
    required this.treePollenAllergies,
    required this.weedPollenAllergies,
  });

  Map<String, dynamic> toJson() {
    return {
      'age': age,
      'clinicalDiagnosis': clinicalDiagnosis,
      'currentMedications': currentMedications,
      'environmentalTriggers': environmentalTriggers.toJson(),
      'familyAllergyHistory': familyAllergyHistory,
      'foodAllergies': foodAllergies.toJson(),
      'gender': gender,
      'grassPollenAllergies': grassPollenAllergies.toJson(),
      'latitude': latitude,
      'longitude': longitude,
      'previousAllergicReactions': previousAllergicReactions.toJson(),
      'treePollenAllergies': treePollenAllergies.toJson(),
      'weedPollenAllergies': weedPollenAllergies.toJson(),
    };
  }

  factory AllergyProfileRequest.fromJson(Map<String, dynamic> json) {
    return AllergyProfileRequest(
      age: json['age'] ?? 0,
      clinicalDiagnosis: json['clinicalDiagnosis'] ?? '',
      currentMedications: List<String>.from(json['currentMedications'] ?? []),
      environmentalTriggers: EnvironmentalTriggers.fromJson(json['environmentalTriggers'] ?? {}),
      familyAllergyHistory: json['familyAllergyHistory'] ?? false,
      foodAllergies: FoodAllergies.fromJson(json['foodAllergies'] ?? {}),
      gender: json['gender'] ?? '',
      grassPollenAllergies: GrassPollenAllergies.fromJson(json['grassPollenAllergies'] ?? {}),
      latitude: (json['latitude'] ?? 0.0).toDouble(),
      longitude: (json['longitude'] ?? 0.0).toDouble(),
      previousAllergicReactions: PreviousAllergicReactions.fromJson(json['previousAllergicReactions'] ?? {}),
      treePollenAllergies: TreePollenAllergies.fromJson(json['treePollenAllergies'] ?? {}),
      weedPollenAllergies: WeedPollenAllergies.fromJson(json['weedPollenAllergies'] ?? {}),
    );
  }
}

class EnvironmentalTriggers {
  final bool airPollution;
  final bool dustMites;
  final bool petDander;
  final bool smoke;
  final bool mold;

  EnvironmentalTriggers({
    required this.airPollution,
    required this.dustMites,
    required this.petDander,
    required this.smoke,
    required this.mold,
  });

  Map<String, dynamic> toJson() {
    return {
      'air_pollution': airPollution,
      'dust_mites': dustMites,
      'pet_dander': petDander,
      'smoke': smoke,
      'mold': mold,
    };
  }

  factory EnvironmentalTriggers.fromJson(Map<String, dynamic> json) {
    return EnvironmentalTriggers(
      airPollution: json['air_pollution'] ?? false,
      dustMites: json['dust_mites'] ?? false,
      petDander: json['pet_dander'] ?? false,
      smoke: json['smoke'] ?? false,
      mold: json['mold'] ?? false,
    );
  }
}

class FoodAllergies {
  final bool apple;
  final bool shellfish;
  final bool nuts;

  FoodAllergies({
    required this.apple,
    required this.shellfish,
    required this.nuts,
  });

  Map<String, dynamic> toJson() {
    return {
      'apple': apple,
      'shellfish': shellfish,
      'nuts': nuts,
    };
  }

  factory FoodAllergies.fromJson(Map<String, dynamic> json) {
    return FoodAllergies(
      apple: json['apple'] ?? false,
      shellfish: json['shellfish'] ?? false,
      nuts: json['nuts'] ?? false,
    );
  }
}

class GrassPollenAllergies {
  final bool graminales;

  GrassPollenAllergies({
    required this.graminales,
  });

  Map<String, dynamic> toJson() {
    return {
      'graminales': graminales,
    };
  }

  factory GrassPollenAllergies.fromJson(Map<String, dynamic> json) {
    return GrassPollenAllergies(
      graminales: json['graminales'] ?? false,
    );
  }
}

class PreviousAllergicReactions {
  final bool severeAsthma;
  final bool hospitalization;
  final bool anaphylaxis;

  PreviousAllergicReactions({
    required this.severeAsthma,
    required this.hospitalization,
    required this.anaphylaxis,
  });

  Map<String, dynamic> toJson() {
    return {
      'severe_asthma': severeAsthma,
      'hospitalization': hospitalization,
      'anaphylaxis': anaphylaxis,
    };
  }

  factory PreviousAllergicReactions.fromJson(Map<String, dynamic> json) {
    return PreviousAllergicReactions(
      severeAsthma: json['severe_asthma'] ?? false,
      hospitalization: json['hospitalization'] ?? false,
      anaphylaxis: json['anaphylaxis'] ?? false,
    );
  }
}

class TreePollenAllergies {
  final bool pine;
  final bool olive;
  final bool birch;

  TreePollenAllergies({
    required this.pine,
    required this.olive,
    required this.birch,
  });

  Map<String, dynamic> toJson() {
    return {
      'pine': pine,
      'olive': olive,
      'birch': birch,
    };
  }

  factory TreePollenAllergies.fromJson(Map<String, dynamic> json) {
    return TreePollenAllergies(
      pine: json['pine'] ?? false,
      olive: json['olive'] ?? false,
      birch: json['birch'] ?? false,
    );
  }
}

class WeedPollenAllergies {
  final bool mugwort;
  final bool ragweed;

  WeedPollenAllergies({
    required this.mugwort,
    required this.ragweed,
  });

  Map<String, dynamic> toJson() {
    return {
      'mugwort': mugwort,
      'ragweed': ragweed,
    };
  }

  factory WeedPollenAllergies.fromJson(Map<String, dynamic> json) {
    return WeedPollenAllergies(
      mugwort: json['mugwort'] ?? false,
      ragweed: json['ragweed'] ?? false,
    );
  }
}