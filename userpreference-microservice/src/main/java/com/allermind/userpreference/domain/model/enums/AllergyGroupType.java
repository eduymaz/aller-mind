package com.allermind.userpreference.domain.model.enums;

public enum AllergyGroupType {
    SEVERE_ALLERGIC(1, "Şiddetli Alerjik Grup", 0.18, "IgE > 1000 IU/mL, Anaphylaxis riski yüksek"),
    MILD_MODERATE_ALLERGIC(2, "Hafif-Orta Alerjik Grup", 0.22, "IgE 200-1000 IU/mL, Kontrol edilebilir belirtiler"),
    GENETIC_PREDISPOSITION(3, "Genetik Yatkınlık Grubu", 0.24, "Atopik yapı, ailesel yüklenme"),
    UNDIAGNOSED(4, "Teşhis Almamış Grup", 0.24, "Normal/sınırda IgE, belirsiz sensibilizasyon"),
    VULNERABLE_POPULATION(5, "Hassas Çocuk/Yaşlı Grubu", 0.12, "İmmün sistem immatüritesi/yaşlanması");
    
    private final int id;
    private final String name;
    private final double weight;
    private final String description;
    
    AllergyGroupType(int id, String name, double weight, String description) {
        this.id = id;
        this.name = name;
        this.weight = weight;
        this.description = description;
    }
    
    public int getId() {
        return id;
    }
    
    public String getName() {
        return name;
    }
    
    public double getWeight() {
        return weight;
    }
    
    public String getDescription() {
        return description;
    }
}