package com.allermind.weather.infrastructure.repository;

import com.allermind.weather.domain.entity.AirQualityRecord;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface AirQualityRecordRepository extends JpaRepository<AirQualityRecord, Long> {
    
    @Query("SELECT a FROM AirQualityRecord a WHERE a.lat = :lat AND a.lon = :lon ORDER BY a.time DESC")
    List<AirQualityRecord> findByLatAndLonOrderByTimeDesc(@Param("lat") Double lat, @Param("lon") Double lon);
    
    @Query("SELECT a FROM AirQualityRecord a WHERE a.lat = :lat AND a.lon = :lon ORDER BY a.time DESC LIMIT 1")
    AirQualityRecord findLatestByLatAndLon(@Param("lat") Double lat, @Param("lon") Double lon);
}
