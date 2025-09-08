package com.allermind.weather.infrastructure.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import com.allermind.weather.domain.entity.WeatherRecord;

@Repository
public interface WeatherRecordRepository extends JpaRepository<WeatherRecord, Long> {
    
    @Query("SELECT w FROM WeatherRecord w WHERE w.lat = :lat AND w.lon = :lon ORDER BY w.time DESC")
    List<WeatherRecord> findByLatAndLonOrderByTimeDesc(@Param("lat") String lat, @Param("lon") String lon);
    
    @Query("SELECT w FROM WeatherRecord w WHERE w.lat = :lat AND w.lon = :lon ORDER BY w.time DESC LIMIT 1")
    WeatherRecord findLatestByLatAndLon(@Param("lat") String lat, @Param("lon") String lon);
}
