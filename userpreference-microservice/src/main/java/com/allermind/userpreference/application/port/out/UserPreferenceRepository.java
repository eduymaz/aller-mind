package com.allermind.userpreference.application.port.out;

import com.allermind.userpreference.domain.model.aggregate.UserPreference;
import java.util.UUID;
import java.util.Optional;

public interface UserPreferenceRepository {
    UserPreference save(UserPreference userPreference);
    Optional<UserPreference> findById(UUID id);
    void deleteById(UUID id);
}