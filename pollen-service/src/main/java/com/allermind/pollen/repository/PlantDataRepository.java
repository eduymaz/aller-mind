package com.allermind.pollen.repository;

import com.allermind.pollen.model.PlantData;
import com.allermind.pollen.model.PollenData;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface PlantDataRepository extends JpaRepository<PlantData, Integer> {
    List<PlantData> findByPollenData(PollenData pollenData);
}
