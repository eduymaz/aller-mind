package com.allermind.weather.infrastructure.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import com.allermind.weather.domain.entity.AirQualityRecord;

@Repository
public interface AirQualityRecordRepository extends JpaRepository<AirQualityRecord, Long> {
    
    @Query("SELECT a FROM AirQualityRecord a WHERE a.lat = :lat AND a.lon = :lon ORDER BY a.time DESC")
    List<AirQualityRecord> findByLatAndLonOrderByTimeDesc(@Param("lat") String lat, @Param("lon") String lon);
    
    @Query("SELECT a FROM AirQualityRecord a WHERE a.lat = :lat AND a.lon = :lon ORDER BY a.time DESC LIMIT 1")
    AirQualityRecord findLatestByLatAndLon(@Param("lat") String lat, @Param("lon") String lon);
}
