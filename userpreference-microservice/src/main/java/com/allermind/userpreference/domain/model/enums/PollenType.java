package com.allermind.userpreference.domain.model.enums;

public enum PollenType {
    // Tree pollens
    BIRCH("birch", PollenCategory.TREE),
    OLIVE("olive", PollenCategory.TREE),
    PINE("pine", PollenCategory.TREE),
    OAK("oak", PollenCategory.TREE),
    CEDAR("cedar", PollenCategory.TREE),
    
    // Grass pollens
    GRAMINALES("graminales", PollenCategory.GRASS),
    
    // Weed pollens
    RAGWEED("ragweed", PollenCategory.WEED),
    MUGWORT("mugwort", PollenCategory.WEED),
    PLANTAIN("plantain", PollenCategory.WEED),
    NETTLE("nettle", PollenCategory.WEED);
    
    private final String name;
    private final PollenCategory category;
    
    PollenType(String name, PollenCategory category) {
        this.name = name;
        this.category = category;
    }
    
    public String getName() {
        return name;
    }
    
    public PollenCategory getCategory() {
        return category;
    }
    
    public enum PollenCategory {
        TREE, GRASS, WEED
    }
}