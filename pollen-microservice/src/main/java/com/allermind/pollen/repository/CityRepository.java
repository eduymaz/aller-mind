package com.allermind.pollen.repository;

import java.util.List;
import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import com.allermind.pollen.model.City;

@Repository
public interface CityRepository extends JpaRepository<City, Integer> {
    // Custom query to find cities by name (case insensitive)
    List<City> findByIlAdiIgnoreCase(String ilAdi);
    
    // Find city by exact lat/lon coordinates
    Optional<City> findByLatAndLon(String lat, String lon);
    
    // Find nearest city using SQL formula for distance calculation
    @Query(value = "SELECT * FROM \"POLLEN\".city c " +
           "ORDER BY " +
           "SQRT(POWER(CAST(c.lat AS DECIMAL(10,6)) - CAST(:lat AS DECIMAL(10,6)), 2) + " +
           "     POWER(CAST(c.lon AS DECIMAL(10,6)) - CAST(:lon AS DECIMAL(10,6)), 2)) " +
           "LIMIT 1", nativeQuery = true)
    Optional<City> findNearestCity(@Param("lat") String lat, @Param("lon") String lon);
}
