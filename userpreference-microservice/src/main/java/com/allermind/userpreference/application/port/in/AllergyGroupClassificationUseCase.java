package com.allermind.userpreference.application.port.in;

import com.allermind.userpreference.application.dto.AllergyClassificationRequest;
import com.allermind.userpreference.application.dto.AllergyClassificationResponse;

public interface AllergyGroupClassificationUseCase {
    AllergyClassificationResponse classifyAllergy(AllergyClassificationRequest request);
}