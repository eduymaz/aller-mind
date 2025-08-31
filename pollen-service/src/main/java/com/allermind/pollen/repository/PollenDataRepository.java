package com.allermind.pollen.repository;

import java.time.LocalDate;
import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.allermind.pollen.model.PollenData;

@Repository
public interface PollenDataRepository extends JpaRepository<PollenData, Integer> {
    List<PollenData> findByLatAndLon(Float lat, Float lon);

    // New method to find data ordered by date
    List<PollenData> findByLatAndLonAndDateOrderByDateDesc(Float lat, Float lon, LocalDate date);
}
