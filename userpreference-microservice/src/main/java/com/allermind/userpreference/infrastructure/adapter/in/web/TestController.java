package com.allermind.userpreference.infrastructure.adapter.in.web;

import java.math.BigDecimal;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.allermind.userpreference.application.dto.AllergyClassificationRequest;

@RestController
@RequestMapping("/api/v1/test")
public class TestController {
    
    @GetMapping("/sample-request")
    public ResponseEntity<AllergyClassificationRequest> getSampleRequest() {
        AllergyClassificationRequest request = new AllergyClassificationRequest();
        
        // Basic information
        request.setAge(28);
        request.setGender("female");
        request.setLatitude(new BigDecimal("41.0082"));
        request.setLongitude(new BigDecimal("28.9784"));
        
        // Clinical history
        request.setClinicalDiagnosis("mild_moderate_allergy");
        request.setFamilyAllergyHistory(true);
        
        // Previous allergic reactions
        Map<String, Boolean> reactions = new HashMap<>();
        reactions.put("anaphylaxis", false);
        reactions.put("severe_asthma", false);
        reactions.put("hospitalization", false);
        request.setPreviousAllergicReactions(reactions);
        
        // Current medications
        request.setCurrentMedications(Set.of("antihistamine", "nasal_spray"));
        
        // Pollen allergies
        Map<String, Boolean> treeAllergies = new HashMap<>();
        treeAllergies.put("birch", true);
        treeAllergies.put("olive", false);
        treeAllergies.put("pine", false);
        request.setTreePollenAllergies(treeAllergies);
        
        Map<String, Boolean> grassAllergies = new HashMap<>();
        grassAllergies.put("graminales", true);
        request.setGrassPollenAllergies(grassAllergies);
        
        Map<String, Boolean> weedAllergies = new HashMap<>();
        weedAllergies.put("ragweed", true);
        weedAllergies.put("mugwort", false);
        request.setWeedPollenAllergies(weedAllergies);
        
        // Food allergies
        Map<String, Boolean> foodAllergies = new HashMap<>();
        foodAllergies.put("apple", true);
        foodAllergies.put("nuts", false);
        foodAllergies.put("shellfish", false);
        request.setFoodAllergies(foodAllergies);
        
        // Environmental triggers
        Map<String, Boolean> triggers = new HashMap<>();
        triggers.put("dust_mites", true);
        triggers.put("pet_dander", false);
        triggers.put("mold", true);
        triggers.put("air_pollution", true);
        triggers.put("smoke", true);
        request.setEnvironmentalTriggers(triggers);
        
        return ResponseEntity.ok(request);
    }
}