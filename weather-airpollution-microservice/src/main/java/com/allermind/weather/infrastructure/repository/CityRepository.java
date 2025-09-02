package com.allermind.weather.infrastructure.repository;

import com.allermind.weather.domain.entity.City;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface CityRepository extends JpaRepository<City, Integer> {
    
    Optional<City> findByIlAdiIgnoreCase(String ilAdi);
}
