package com.allermind.userpreference.application.service;

import java.util.UUID;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.allermind.userpreference.application.dto.AllergyClassificationRequest;
import com.allermind.userpreference.application.dto.AllergyClassificationResponse;
import com.allermind.userpreference.application.mapper.AllergyClassificationMapper;
import com.allermind.userpreference.application.port.in.AllergyGroupClassificationUseCase;
import com.allermind.userpreference.application.port.in.GetUserPreferenceUseCase;
import com.allermind.userpreference.application.port.out.UserPreferenceRepository;
import com.allermind.userpreference.domain.model.aggregate.UserPreference;
import com.allermind.userpreference.domain.model.valueobject.AllergyClassificationResult;
import com.allermind.userpreference.domain.service.AllergyGroupClassifierDomainService;

@Service
@Transactional
public class UserPreferenceApplicationService implements AllergyGroupClassificationUseCase, GetUserPreferenceUseCase {
    
    private final AllergyGroupClassifierDomainService classifierDomainService;
    private final UserPreferenceRepository userPreferenceRepository;
    private final AllergyClassificationMapper mapper;
    
    public UserPreferenceApplicationService(
            AllergyGroupClassifierDomainService classifierDomainService,
            UserPreferenceRepository userPreferenceRepository,
            AllergyClassificationMapper mapper) {
        this.classifierDomainService = classifierDomainService;
        this.userPreferenceRepository = userPreferenceRepository;
        this.mapper = mapper;
    }
    
    @Override
    public AllergyClassificationResponse classifyAllergy(AllergyClassificationRequest request) {
        // Validate request
        validateRequest(request);
        
        // Convert request to domain object
        UserPreference userPreference = mapper.toUserPreference(request);
        
        // Validate domain object
        validateUserPreference(userPreference);
        
        // Classify allergy group
        AllergyClassificationResult result = classifierDomainService.classifyAllergyGroup(userPreference);
        
        // Save user preference
        UserPreference savedPreference = userPreferenceRepository.save(userPreference);
        
        // Convert to response
        return mapper.toResponse(result, savedPreference);
    }
    
    @Override
    public AllergyClassificationResponse getUserPreference(UUID userId) {
        // Find user preference by ID
        UserPreference userPreference = userPreferenceRepository.findById(userId)
                .orElseThrow(() -> new IllegalArgumentException("User preference not found with ID: " + userId));
        
        // Re-classify allergy group based on stored user preference
        AllergyClassificationResult result = classifierDomainService.classifyAllergyGroup(userPreference);
        
        // Convert to response
        return mapper.toResponse(result, userPreference);
    }
    
    private void validateRequest(AllergyClassificationRequest request) {
        if (request == null) {
            throw new IllegalArgumentException("Request cannot be null");
        }
        
        if (request.getAge() == null || request.getAge() < 0 || request.getAge() > 150) {
            throw new IllegalArgumentException("Age must be between 0 and 150");
        }
        
        if (request.getGender() == null || request.getGender().isBlank()) {
            throw new IllegalArgumentException("Gender is required");
        }
        
        if (request.getLatitude() == null || request.getLongitude() == null) {
            throw new IllegalArgumentException("Location (latitude and longitude) is required");
        }
    }
    
    private void validateUserPreference(UserPreference userPreference) {
        if (userPreference.getAge() == null) {
            throw new IllegalArgumentException("Age is required");
        }
        
        if (userPreference.getGender() == null) {
            throw new IllegalArgumentException("Gender is required");
        }
        
        if (userPreference.getLocation() == null) {
            throw new IllegalArgumentException("Location is required");
        }
    }
}