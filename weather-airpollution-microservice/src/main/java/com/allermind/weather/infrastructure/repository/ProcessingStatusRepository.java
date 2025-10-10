package com.allermind.weather.infrastructure.repository;

import java.time.LocalDate;
import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.allermind.weather.domain.entity.ProcessingStatus;

@Repository
public interface ProcessingStatusRepository extends JpaRepository<ProcessingStatus, LocalDate> {
    
    Optional<ProcessingStatus> findByDate(LocalDate date);
}
