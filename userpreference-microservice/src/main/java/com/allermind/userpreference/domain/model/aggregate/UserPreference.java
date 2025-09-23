package com.allermind.userpreference.domain.model.aggregate;

import com.allermind.userpreference.domain.model.enums.*;
import com.allermind.userpreference.domain.model.valueobject.Age;
import com.allermind.userpreference.domain.model.valueobject.Location;
import jakarta.persistence.*;

import java.util.*;

@Entity
@Table(name = "user_preferences")
public class UserPreference {
    
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;
    
    @Embedded
    @AttributeOverrides({
        @AttributeOverride(name = "value", column = @Column(name = "age"))
    })
    private Age age;
    
    @Enumerated(EnumType.STRING)
    private Gender gender;
    
    @Embedded
    @AttributeOverrides({
        @AttributeOverride(name = "latitude", column = @Column(name = "latitude")),
        @AttributeOverride(name = "longitude", column = @Column(name = "longitude"))
    })
    private Location location;
    
    @Enumerated(EnumType.STRING)
    @Column(name = "clinical_diagnosis")
    private ClinicalDiagnosis clinicalDiagnosis;
    
    @Column(name = "family_allergy_history")
    private Boolean familyAllergyHistory;
    
    @ElementCollection(fetch = FetchType.EAGER)
    @CollectionTable(name = "previous_allergic_reactions", joinColumns = @JoinColumn(name = "user_preference_id"))
    @MapKeyEnumerated(EnumType.STRING)
    @Column(name = "has_reaction")
    private Map<AllergyReactionType, Boolean> previousAllergicReactions = new HashMap<>();
    
    @ElementCollection(fetch = FetchType.EAGER)
    @CollectionTable(name = "current_medications", joinColumns = @JoinColumn(name = "user_preference_id"))
    @Column(name = "medication")
    private Set<String> currentMedications = new HashSet<>();
    
    @ElementCollection(fetch = FetchType.EAGER)
    @CollectionTable(name = "tree_pollen_allergies", joinColumns = @JoinColumn(name = "user_preference_id"))
    @MapKeyEnumerated(EnumType.STRING)
    @Column(name = "is_allergic")
    private Map<PollenType, Boolean> treePollenAllergies = new HashMap<>();
    
    @ElementCollection(fetch = FetchType.EAGER)
    @CollectionTable(name = "grass_pollen_allergies", joinColumns = @JoinColumn(name = "user_preference_id"))
    @MapKeyEnumerated(EnumType.STRING)
    @Column(name = "is_allergic")
    private Map<PollenType, Boolean> grassPollenAllergies = new HashMap<>();
    
    @ElementCollection(fetch = FetchType.EAGER)
    @CollectionTable(name = "weed_pollen_allergies", joinColumns = @JoinColumn(name = "user_preference_id"))
    @MapKeyEnumerated(EnumType.STRING)
    @Column(name = "is_allergic")
    private Map<PollenType, Boolean> weedPollenAllergies = new HashMap<>();
    
    @ElementCollection(fetch = FetchType.EAGER)
    @CollectionTable(name = "food_allergies", joinColumns = @JoinColumn(name = "user_preference_id"))
    @MapKeyEnumerated(EnumType.STRING)
    @Column(name = "is_allergic")
    private Map<FoodType, Boolean> foodAllergies = new HashMap<>();
    
    @ElementCollection(fetch = FetchType.EAGER)
    @CollectionTable(name = "environmental_triggers", joinColumns = @JoinColumn(name = "user_preference_id"))
    @MapKeyEnumerated(EnumType.STRING)
    @Column(name = "is_sensitive")
    private Map<EnvironmentalTrigger, Boolean> environmentalTriggers = new HashMap<>();
    
    // Constructors
    protected UserPreference() {}
    
    public UserPreference(Age age, Gender gender, Location location, ClinicalDiagnosis clinicalDiagnosis, 
                          Boolean familyAllergyHistory) {
        this.age = age;
        this.gender = gender;
        this.location = location;
        this.clinicalDiagnosis = clinicalDiagnosis;
        this.familyAllergyHistory = familyAllergyHistory;
    }
    
    // Business methods
    public boolean hasVulnerableAge() {
        return age != null && age.isVulnerable();
    }
    
    public boolean hasFamilyHistory() {
        return Boolean.TRUE.equals(familyAllergyHistory);
    }
    
    public int getEnvironmentalTriggerCount() {
        return (int) environmentalTriggers.values().stream()
                .mapToLong(triggered -> triggered ? 1 : 0)
                .sum();
    }
    
    public boolean hasPreviousReaction(AllergyReactionType reactionType) {
        return Boolean.TRUE.equals(previousAllergicReactions.get(reactionType));
    }
    
    public boolean isOnMedication(String medication) {
        return currentMedications.contains(medication);
    }
    
    public boolean hasPollenAllergy(PollenType pollenType) {
        return switch (pollenType.getCategory()) {
            case TREE -> Boolean.TRUE.equals(treePollenAllergies.get(pollenType));
            case GRASS -> Boolean.TRUE.equals(grassPollenAllergies.get(pollenType));
            case WEED -> Boolean.TRUE.equals(weedPollenAllergies.get(pollenType));
        };
    }
    
    public boolean hasFoodAllergy(FoodType foodType) {
        return Boolean.TRUE.equals(foodAllergies.get(foodType));
    }
    
    public boolean hasEnvironmentalTrigger(EnvironmentalTrigger trigger) {
        return Boolean.TRUE.equals(environmentalTriggers.get(trigger));
    }
    
    // Getters and setters
    public UUID getId() {
        return id;
    }
    
    public Age getAge() {
        return age;
    }
    
    public void setAge(Age age) {
        this.age = age;
    }
    
    public Gender getGender() {
        return gender;
    }
    
    public void setGender(Gender gender) {
        this.gender = gender;
    }
    
    public Location getLocation() {
        return location;
    }
    
    public void setLocation(Location location) {
        this.location = location;
    }
    
    public ClinicalDiagnosis getClinicalDiagnosis() {
        return clinicalDiagnosis;
    }
    
    public void setClinicalDiagnosis(ClinicalDiagnosis clinicalDiagnosis) {
        this.clinicalDiagnosis = clinicalDiagnosis;
    }
    
    public Boolean getFamilyAllergyHistory() {
        return familyAllergyHistory;
    }
    
    public void setFamilyAllergyHistory(Boolean familyAllergyHistory) {
        this.familyAllergyHistory = familyAllergyHistory;
    }
    
    public Map<AllergyReactionType, Boolean> getPreviousAllergicReactions() {
        return previousAllergicReactions;
    }
    
    public void setPreviousAllergicReactions(Map<AllergyReactionType, Boolean> previousAllergicReactions) {
        this.previousAllergicReactions = previousAllergicReactions;
    }
    
    public Set<String> getCurrentMedications() {
        return currentMedications;
    }
    
    public void setCurrentMedications(Set<String> currentMedications) {
        this.currentMedications = currentMedications;
    }
    
    public Map<PollenType, Boolean> getTreePollenAllergies() {
        return treePollenAllergies;
    }
    
    public void setTreePollenAllergies(Map<PollenType, Boolean> treePollenAllergies) {
        this.treePollenAllergies = treePollenAllergies;
    }
    
    public Map<PollenType, Boolean> getGrassPollenAllergies() {
        return grassPollenAllergies;
    }
    
    public void setGrassPollenAllergies(Map<PollenType, Boolean> grassPollenAllergies) {
        this.grassPollenAllergies = grassPollenAllergies;
    }
    
    public Map<PollenType, Boolean> getWeedPollenAllergies() {
        return weedPollenAllergies;
    }
    
    public void setWeedPollenAllergies(Map<PollenType, Boolean> weedPollenAllergies) {
        this.weedPollenAllergies = weedPollenAllergies;
    }
    
    public Map<FoodType, Boolean> getFoodAllergies() {
        return foodAllergies;
    }
    
    public void setFoodAllergies(Map<FoodType, Boolean> foodAllergies) {
        this.foodAllergies = foodAllergies;
    }
    
    public Map<EnvironmentalTrigger, Boolean> getEnvironmentalTriggers() {
        return environmentalTriggers;
    }
    
    public void setEnvironmentalTriggers(Map<EnvironmentalTrigger, Boolean> environmentalTriggers) {
        this.environmentalTriggers = environmentalTriggers;
    }
}