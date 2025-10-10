package com.allermind.pollen.dto.external;

import java.util.List;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Root response from Google Pollen API
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class GooglePollenApiResponse {
    
    private String regionCode;
    private List<DailyInfo> dailyInfo;
    
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class DailyInfo {
        private DateInfo date;
        private List<PollenTypeInfo> pollenTypeInfo;
        private List<PlantInfo> plantInfo;
        
        @Data
        @NoArgsConstructor
        @AllArgsConstructor
        public static class DateInfo {
            private Integer year;
            private Integer month;
            private Integer day;
        }
        
        @Data
        @NoArgsConstructor
        @AllArgsConstructor
        public static class PollenTypeInfo {
            private String code;
            private String displayName;
            private Boolean inSeason;
            private IndexInfo indexInfo;
            private List<String> healthRecommendations;
            
            @Data
            @NoArgsConstructor
            @AllArgsConstructor
            public static class IndexInfo {
                private String code;
                private String displayName;
                private Double value;
                private String category;
                private String indexDescription;
            }
        }
        
        @Data
        @NoArgsConstructor
        @AllArgsConstructor
        public static class PlantInfo {
            private String code;
            private String displayName;
            private Boolean inSeason;
            private IndexInfo indexInfo;
            private PlantDescription plantDescription;
            
            @Data
            @NoArgsConstructor
            @AllArgsConstructor
            public static class IndexInfo {
                private String code;
                private String displayName;
                private Double value;
                private String category;
                private String indexDescription;
            }
            
            @Data
            @NoArgsConstructor
            @AllArgsConstructor
            public static class PlantDescription {
                private String type;
                private String family;
                private String season;
                private String specialColors;
                private String specialShapes;
                private String crossReaction;
                private String picture;
                private String pictureCloseup;
                
        
            }
        }
    }
}
