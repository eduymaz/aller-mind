package com.allermind.userpreference.application.port.in;

import java.util.UUID;

import com.allermind.userpreference.application.dto.AllergyClassificationResponse;

public interface GetUserPreferenceUseCase {
    AllergyClassificationResponse getUserPreference(UUID userId);
}