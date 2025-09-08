package com.allermind.weather.infrastructure.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import com.allermind.weather.domain.entity.City;

@Repository
public interface CityRepository extends JpaRepository<City, Integer> {
    
    Optional<City> findByIlAdiIgnoreCase(String ilAdi);
    
    Optional<City> findByLatAndLon(String lat, String lon);
    
    @Query(value = """
        SELECT *, 
        (6371 * acos(cos(radians(:lat)) * cos(radians(CAST(lat AS DECIMAL(10,8)))) * 
        cos(radians(CAST(lon AS DECIMAL(11,8))) - radians(:lon)) + 
        sin(radians(:lat)) * sin(radians(CAST(lat AS DECIMAL(10,8)))))) AS distance 
        FROM "WEATHER".city 
        ORDER BY distance 
        LIMIT 1
        """, nativeQuery = true)
    Optional<City> findNearestCity(@Param("lat") double lat, @Param("lon") double lon);
}
