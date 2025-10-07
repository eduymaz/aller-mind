package com.allermind.userpreference.application.mapper;

import java.util.HashSet;
import java.util.Map;
import java.util.stream.Collectors;

import org.springframework.stereotype.Component;

import com.allermind.userpreference.application.dto.AllergyClassificationRequest;
import com.allermind.userpreference.application.dto.AllergyClassificationResponse;
import com.allermind.userpreference.domain.model.aggregate.UserPreference;
import com.allermind.userpreference.domain.model.enums.AllergyReactionType;
import com.allermind.userpreference.domain.model.enums.ClinicalDiagnosis;
import com.allermind.userpreference.domain.model.enums.EnvironmentalTrigger;
import com.allermind.userpreference.domain.model.enums.FoodType;
import com.allermind.userpreference.domain.model.enums.Gender;
import com.allermind.userpreference.domain.model.enums.PollenType;
import com.allermind.userpreference.domain.model.valueobject.Age;
import com.allermind.userpreference.domain.model.valueobject.AllergyClassificationResult;
import com.allermind.userpreference.domain.model.valueobject.Location;

@Component
public class AllergyClassificationMapper {
    
    public UserPreference toUserPreference(AllergyClassificationRequest request) {
        UserPreference userPreference = new UserPreference(
                new Age(request.getAge()),
                parseGender(request.getGender()),
                new Location(request.getLatitude(), request.getLongitude()),
                parseClinicalDiagnosis(request.getClinicalDiagnosis()),
                request.getFamilyAllergyHistory()
        );
        
        // Map allergic reactions
        if (request.getPreviousAllergicReactions() != null) {
            Map<AllergyReactionType, Boolean> reactions = request.getPreviousAllergicReactions().entrySet().stream()
                    .collect(Collectors.toMap(
                            entry -> parseAllergyReactionType(entry.getKey()),
                            Map.Entry::getValue
                    ));
            userPreference.setPreviousAllergicReactions(reactions);
        }
        
        // Map medications
        if (request.getCurrentMedications() != null) {
            userPreference.setCurrentMedications(new HashSet<>(request.getCurrentMedications()));
        }
        
        // Map pollen allergies
        if (request.getTreePollenAllergies() != null) {
            Map<PollenType, Boolean> treeAllergies = request.getTreePollenAllergies().entrySet().stream()
                    .collect(Collectors.toMap(
                            entry -> parsePollenType(entry.getKey()),
                            Map.Entry::getValue,
                            (existing, replacement) -> replacement
                    ));
            userPreference.setTreePollenAllergies(treeAllergies);
        }
        
        if (request.getGrassPollenAllergies() != null) {
            Map<PollenType, Boolean> grassAllergies = request.getGrassPollenAllergies().entrySet().stream()
                    .collect(Collectors.toMap(
                            entry -> parsePollenType(entry.getKey()),
                            Map.Entry::getValue,
                            (existing, replacement) -> replacement
                    ));
            userPreference.setGrassPollenAllergies(grassAllergies);
        }
        
        if (request.getWeedPollenAllergies() != null) {
            Map<PollenType, Boolean> weedAllergies = request.getWeedPollenAllergies().entrySet().stream()
                    .collect(Collectors.toMap(
                            entry -> parsePollenType(entry.getKey()),
                            Map.Entry::getValue,
                            (existing, replacement) -> replacement
                    ));
            userPreference.setWeedPollenAllergies(weedAllergies);
        }
        
        // Map food allergies
        if (request.getFoodAllergies() != null) {
            Map<FoodType, Boolean> foodAllergies = request.getFoodAllergies().entrySet().stream()
                    .collect(Collectors.toMap(
                            entry -> parseFoodType(entry.getKey()),
                            Map.Entry::getValue,
                            (existing, replacement) -> replacement
                    ));
            userPreference.setFoodAllergies(foodAllergies);
        }
        
        // Map environmental triggers
        if (request.getEnvironmentalTriggers() != null) {
            Map<EnvironmentalTrigger, Boolean> triggers = request.getEnvironmentalTriggers().entrySet().stream()
                    .collect(Collectors.toMap(
                            entry -> parseEnvironmentalTrigger(entry.getKey()),
                            Map.Entry::getValue,
                            (existing, replacement) -> replacement
                    ));
            userPreference.setEnvironmentalTriggers(triggers);
        }
        
        return userPreference;
    }
    
    public AllergyClassificationResponse toResponse(AllergyClassificationResult result, UserPreference userPreference) {
        AllergyClassificationResponse response = new AllergyClassificationResponse();
        
        // Classification result mapping
        response.setUserPreferenceId(userPreference.getId());
        response.setGroupId(result.getGroupType().getId());
        response.setGroupName(result.getGroupType().getName());
        response.setGroupDescription(result.getGroupType().getDescription());
        response.setAssignmentReason(result.getAssignmentReason());
        response.setModelWeight(result.getModelWeight());
        response.setPersonalRiskModifiers(result.getPersonalRiskModifiers());
        response.setImmunologicProfile(result.getImmunologicProfile());
        response.setEnvironmentalSensitivityFactors(result.getEnvironmentalSensitivityFactors());
        response.setPollenSpecificRisks(result.getPollenSpecificRisks());
        response.setRecommendationAdjustments(result.getRecommendationAdjustments());
        
        // User preference details mapping
        if (userPreference.getAge() != null) {
            response.setAge(userPreference.getAge().value());
        }
        if (userPreference.getGender() != null) {
            response.setGender(userPreference.getGender().getValue());
        }
        if (userPreference.getLocation() != null) {
            response.setLatitude(userPreference.getLocation().latitude());
            response.setLongitude(userPreference.getLocation().longitude());
        }
        if (userPreference.getClinicalDiagnosis() != null) {
            response.setClinicalDiagnosis(userPreference.getClinicalDiagnosis().getValue());
        }
        response.setFamilyAllergyHistory(userPreference.getFamilyAllergyHistory());
        
        // Map previous allergic reactions to String keys
        if (userPreference.getPreviousAllergicReactions() != null && !userPreference.getPreviousAllergicReactions().isEmpty()) {
            Map<String, Boolean> reactions = userPreference.getPreviousAllergicReactions().entrySet().stream()
                    .collect(Collectors.toMap(
                            entry -> entry.getKey().getName(),
                            Map.Entry::getValue
                    ));
            response.setPreviousAllergicReactions(reactions);
        }
        
        response.setCurrentMedications(userPreference.getCurrentMedications());
        
        // Map pollen allergies to String keys
        if (userPreference.getTreePollenAllergies() != null && !userPreference.getTreePollenAllergies().isEmpty()) {
            Map<String, Boolean> treeAllergies = userPreference.getTreePollenAllergies().entrySet().stream()
                    .collect(Collectors.toMap(
                            entry -> entry.getKey().getName(),
                            Map.Entry::getValue
                    ));
            response.setTreePollenAllergies(treeAllergies);
        }
        
        if (userPreference.getGrassPollenAllergies() != null && !userPreference.getGrassPollenAllergies().isEmpty()) {
            Map<String, Boolean> grassAllergies = userPreference.getGrassPollenAllergies().entrySet().stream()
                    .collect(Collectors.toMap(
                            entry -> entry.getKey().getName(),
                            Map.Entry::getValue
                    ));
            response.setGrassPollenAllergies(grassAllergies);
        }
        
        if (userPreference.getWeedPollenAllergies() != null && !userPreference.getWeedPollenAllergies().isEmpty()) {
            Map<String, Boolean> weedAllergies = userPreference.getWeedPollenAllergies().entrySet().stream()
                    .collect(Collectors.toMap(
                            entry -> entry.getKey().getName(),
                            Map.Entry::getValue
                    ));
            response.setWeedPollenAllergies(weedAllergies);
        }
        
        // Map food allergies to String keys
        if (userPreference.getFoodAllergies() != null && !userPreference.getFoodAllergies().isEmpty()) {
            Map<String, Boolean> foodAllergies = userPreference.getFoodAllergies().entrySet().stream()
                    .collect(Collectors.toMap(
                            entry -> entry.getKey().getName(),
                            Map.Entry::getValue
                    ));
            response.setFoodAllergies(foodAllergies);
        }
        
        // Map environmental triggers to String keys
        if (userPreference.getEnvironmentalTriggers() != null && !userPreference.getEnvironmentalTriggers().isEmpty()) {
            Map<String, Boolean> triggers = userPreference.getEnvironmentalTriggers().entrySet().stream()
                    .collect(Collectors.toMap(
                            entry -> entry.getKey().getName(),
                            Map.Entry::getValue
                    ));
            response.setEnvironmentalTriggers(triggers);
        }
        
        return response;
    }
    
    private Gender parseGender(String gender) {
        if (gender == null) return null;
        return switch (gender.toLowerCase()) {
            case "male" -> Gender.MALE;
            case "female" -> Gender.FEMALE;
            case "other" -> Gender.OTHER;
            default -> throw new IllegalArgumentException("Invalid gender: " + gender);
        };
    }
    
    private ClinicalDiagnosis parseClinicalDiagnosis(String diagnosis) {
        if (diagnosis == null) return ClinicalDiagnosis.NONE;
        return switch (diagnosis.toLowerCase()) {
            case "none" -> ClinicalDiagnosis.NONE;
            case "mild_moderate_allergy" -> ClinicalDiagnosis.MILD_MODERATE_ALLERGY;
            case "severe_allergy" -> ClinicalDiagnosis.SEVERE_ALLERGY;
            case "asthma" -> ClinicalDiagnosis.ASTHMA;
            default -> throw new IllegalArgumentException("Invalid clinical diagnosis: " + diagnosis);
        };
    }
    
    private AllergyReactionType parseAllergyReactionType(String type) {
        if (type == null) return null;
        return switch (type.toLowerCase()) {
            case "anaphylaxis" -> AllergyReactionType.ANAPHYLAXIS;
            case "severe_asthma" -> AllergyReactionType.SEVERE_ASTHMA;
            case "hospitalization" -> AllergyReactionType.HOSPITALIZATION;
            case "skin_reactions" -> AllergyReactionType.SKIN_REACTIONS;
            case "respiratory_symptoms" -> AllergyReactionType.RESPIRATORY_SYMPTOMS;
            default -> throw new IllegalArgumentException("Invalid allergy reaction type: " + type);
        };
    }
    
    private PollenType parsePollenType(String type) {
        if (type == null) return null;
        return switch (type.toLowerCase()) {
            case "birch" -> PollenType.BIRCH;
            case "olive" -> PollenType.OLIVE;
            case "pine" -> PollenType.PINE;
            case "oak" -> PollenType.OAK;
            case "cedar" -> PollenType.CEDAR;
            case "graminales" -> PollenType.GRAMINALES;
            case "ragweed" -> PollenType.RAGWEED;
            case "mugwort" -> PollenType.MUGWORT;
            case "plantain" -> PollenType.PLANTAIN;
            case "nettle" -> PollenType.NETTLE;
            default -> throw new IllegalArgumentException("Invalid pollen type: " + type);
        };
    }
    
    private FoodType parseFoodType(String type) {
        if (type == null) return null;
        return switch (type.toLowerCase()) {
            case "apple" -> FoodType.APPLE;
            case "cherry" -> FoodType.CHERRY;
            case "pear" -> FoodType.PEAR;
            case "almond" -> FoodType.ALMOND;
            case "melon" -> FoodType.MELON;
            case "banana" -> FoodType.BANANA;
            case "cucumber" -> FoodType.CUCUMBER;
            case "celery" -> FoodType.CELERY;
            case "spices" -> FoodType.SPICES;
            case "herbs" -> FoodType.HERBS;
            case "nuts" -> FoodType.NUTS;
            case "shellfish" -> FoodType.SHELLFISH;
            case "milk" -> FoodType.MILK;
            case "eggs" -> FoodType.EGGS;
            case "soy" -> FoodType.SOY;
            case "wheat" -> FoodType.WHEAT;
            case "fish" -> FoodType.FISH;
            default -> throw new IllegalArgumentException("Invalid food type: " + type);
        };
    }
    
    private EnvironmentalTrigger parseEnvironmentalTrigger(String trigger) {
        if (trigger == null) return null;
        return switch (trigger.toLowerCase()) {
            case "dust_mites" -> EnvironmentalTrigger.DUST_MITES;
            case "pet_dander" -> EnvironmentalTrigger.PET_DANDER;
            case "mold" -> EnvironmentalTrigger.MOLD;
            case "air_pollution" -> EnvironmentalTrigger.AIR_POLLUTION;
            case "smoke" -> EnvironmentalTrigger.SMOKE;
            default -> throw new IllegalArgumentException("Invalid environmental trigger: " + trigger);
        };
    }
}