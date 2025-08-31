package com.allermind.pollen.repository;

import com.allermind.pollen.model.City;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface CityRepository extends JpaRepository<City, Integer> {
    // Custom query to find cities by name (case insensitive)
    List<City> findByIlAdiIgnoreCase(String ilAdi);
}
