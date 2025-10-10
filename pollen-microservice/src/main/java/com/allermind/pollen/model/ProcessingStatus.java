package com.allermind.pollen.model;

import java.time.LocalDate;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "processing_status")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class ProcessingStatus {
    
    @Id
    private LocalDate date;
    
    @Column(nullable = false)
    private Boolean isprocessed;
}
