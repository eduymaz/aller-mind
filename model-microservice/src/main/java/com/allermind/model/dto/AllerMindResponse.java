package com.allermind.model.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AllerMindResponse {
    private String predictionId;
    private String userId;
    private String lat;
    private String lon;
    private Boolean success;
    private String message;
    private Double overallRiskScore;
    private String overallRiskLevel;
    private String overallRiskEmoji;
    private Integer overallRiskCode;
    private ModelPredictionResponse modelPrediction;
    private UserGroup userGroup;
    
    // Kısayol metodları - en yüksek risk grubunun bilgilerini getirir
    public String getRecommendation() {
        if (modelPrediction != null && modelPrediction.getPredictions() != null && !modelPrediction.getPredictions().isEmpty()) {
            // En yüksek risk skoruna sahip grubu bul
            return modelPrediction.getPredictions().stream()
                .max((g1, g2) -> Double.compare(g1.getPredictionValue(), g2.getPredictionValue()))
                .map(group -> generateRecommendation(group.getRiskLevel(), group.getPredictionValue()))
                .orElse("Genel önlemler alınması önerilir");
        }
        return "Veri yetersiz";
    }
    
    private String generateRecommendation(String riskLevel, Double value) {
        return switch (riskLevel) {
            case "DÜŞÜK" -> "Dışarı çıkabilirsiniz, genel önlemler yeterli";
            case "ORTA" -> "Dikkatli olun, maske kullanımı önerilir";
            case "ORTA-YÜKSEK" -> "Mümkünse evde kalın, çıkarken mutlaka maske takın";
            case "YÜKSEK" -> "Dışarı çıkmayın, ilaçlarınızı hazır bulundurun";
            case "ÇOK YÜKSEK" -> "Kesinlikle dışarı çıkmayın, acil durumda doktora başvurun";
            default -> "Risk değerlendirmesi yapılamadı";
        };
    }
}
