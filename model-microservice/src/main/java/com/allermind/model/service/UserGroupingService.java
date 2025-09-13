package com.allermind.model.service;

import java.util.List;

import org.springframework.stereotype.Service;

import com.allermind.model.dto.UserGroup;
import com.allermind.model.dto.UserSettings;

import lombok.extern.slf4j.Slf4j;

@Service
@Slf4j
public class UserGroupingService {

    /**
     * User settings bilgisini algoritma ile grup bilgisine dönüştürür.
     * Şu anda basit bir algoritma kullanılmaktadır, gelecekte ML modeli ile geliştirilebilir.
     */
    public UserGroup determineUserGroup(UserSettings userSettings) {
        log.info("Determining user group for user: {}", userSettings.getUserId());

        return UserGroup.builder()
                .groupId("1")
                .riskLevel("HIGH")
                .riskScore(10.0)
                .groupDescription("Yüksek risk")
                .build();
        
        // Basit bir algoritma - gelecekte daha karmaşık hale getirilebilir
        /*String riskLevel = calculateRiskLevel(userSettings);
        Double riskScore = calculateRiskScore(userSettings);
        
        return UserGroup.builder()
                .groupId(generateGroupId(riskLevel))
                .riskLevel(riskLevel)
                .riskScore(riskScore)
                .groupDescription(generateGroupDescription(riskLevel))
                .build();*/
    }

    private String calculateRiskLevel(UserSettings userSettings) {
        int riskPoints = 0;

        // Allerji sayısına göre puan
        List<String> allergies = userSettings.getAllergies();
        if (allergies != null) {
            riskPoints += allergies.size() * 10;
        }

        // Hassasiyet seviyesine göre puan
        String sensitivityLevel = userSettings.getSensitivityLevel();
        if ("HIGH".equals(sensitivityLevel)) {
            riskPoints += 30;
        } else if ("MEDIUM".equals(sensitivityLevel)) {
            riskPoints += 20;
        } else if ("LOW".equals(sensitivityLevel)) {
            riskPoints += 10;
        }

        // Yaşa göre puan (yaşlılar ve çocuklar daha riskli)
        Integer age = userSettings.getAge();
        if (age != null) {
            if (age < 12 || age > 65) {
                riskPoints += 15;
            }
        }

        // Risk seviyesini belirle
        if (riskPoints >= 60) {
            return "CRITICAL";
        } else if (riskPoints >= 40) {
            return "HIGH";
        } else if (riskPoints >= 20) {
            return "MEDIUM";
        } else {
            return "LOW";
        }
    }

    private Double calculateRiskScore(UserSettings userSettings) {
        // 0.0 - 1.0 arasında risk skoru hesapla
        int totalPoints = 100; // Maksimum puan
        int userPoints = 0;

        List<String> allergies = userSettings.getAllergies();
        if (allergies != null) {
            userPoints += Math.min(allergies.size() * 10, 50); // Max 50 puan allerji için
        }

        String sensitivityLevel = userSettings.getSensitivityLevel();
        if ("HIGH".equals(sensitivityLevel)) {
            userPoints += 30;
        } else if ("MEDIUM".equals(sensitivityLevel)) {
            userPoints += 20;
        } else if ("LOW".equals(sensitivityLevel)) {
            userPoints += 10;
        }

        Integer age = userSettings.getAge();
        if (age != null) {
            if (age < 12 || age > 65) {
                userPoints += 20;
            }
        }

        return Math.min(userPoints / (double) totalPoints, 1.0);
    }

    private String generateGroupId(String riskLevel) {
        // Python servisinin beklediği grup ID formatı (1-5 arası sayısal)
        return switch (riskLevel) {
            case "LOW" -> "1";      // Grup 1: Şiddetli Alerjik Grup (düşük risk)
            case "MEDIUM" -> "2";   // Grup 2: Hafif-Orta Grup
            case "HIGH" -> "3";     // Grup 3: Olası Alerjik/Genetik
            case "CRITICAL" -> "5"; // Grup 5: Hassas Grup (Çocuk/Yaşlı/Kronik)
            default -> "2";         // Default olarak grup 2
        };
    }

    private String generateGroupDescription(String riskLevel) {
        return switch (riskLevel) {
            case "LOW" -> "Düşük risk grubu - Minimal alerji reaksiyonu beklenir";
            case "MEDIUM" -> "Orta risk grubu - Orta düzey alerji reaksiyonu beklenir";
            case "HIGH" -> "Yüksek risk grubu - Yüksek alerji reaksiyonu beklenir";
            case "CRITICAL" -> "Kritik risk grubu - Ciddi alerji reaksiyonu beklenir";
            default -> "Bilinmeyen risk grubu";
        };
    }
}
