package com.allermind.model.dto;

import java.util.List;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserSettings {
    private String userId;
    private List<String> allergies;
    private String sensitivityLevel; // LOW, MEDIUM, HIGH
    private Integer age;
    private String location;
    private List<String> preferences;
    // Daha fazla field gelecekte eklenebilir

    // yas 
    // şehir 
    // Alerji bilgisi 
    
}
