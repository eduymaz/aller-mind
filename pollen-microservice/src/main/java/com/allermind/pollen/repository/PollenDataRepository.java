package com.allermind.pollen.repository;

import java.time.LocalDate;
import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.allermind.pollen.model.PollenData;

@Repository
public interface PollenDataRepository extends JpaRepository<PollenData, Integer> {
    List<PollenData> findByLatAndLon(String lat, String lon);

    // Method to find data by coordinates and specific date
    List<PollenData> findByLatAndLonAndDate(String lat, String lon, LocalDate date);
    
    // Method to find data ordered by date
    List<PollenData> findByLatAndLonAndDateOrderByDateDesc(String lat, String lon, LocalDate date);
}
