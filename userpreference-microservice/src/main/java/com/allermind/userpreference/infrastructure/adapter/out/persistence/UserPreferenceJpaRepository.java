package com.allermind.userpreference.infrastructure.adapter.out.persistence;

import java.util.UUID;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.allermind.userpreference.application.port.out.UserPreferenceRepository;
import com.allermind.userpreference.domain.model.aggregate.UserPreference;

@Repository
public interface UserPreferenceJpaRepository extends JpaRepository<UserPreference, UUID>, UserPreferenceRepository {
}