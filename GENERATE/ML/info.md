# Allergy Group Classification and Environmental Factors

## Allergy Groups

Based on clinical immunology principles, we've revised our allergy group classification from the previous type-based approach to a severity and diagnosis-based categorization:

1. **Severe Allergic Asthma (Group 1)**: Individuals with diagnosed severe allergic asthma
2. **Mild to Moderate Allergic (Group 2)**: Individuals with diagnosed mild to moderate allergies
3. **Possible Allergic/High Risk (Group 3)**: Individuals with high risk for allergies but not yet fully symptomatic
4. **Not Yet Diagnosed (Group 4)**: General population without specific allergy diagnosis
5. **Vulnerable Population (Group 5)**: Babies, children, elderly, and chronic patients

## Priority Environmental Factors by Group

### Group 1: Severe Allergic Asthma
- **Highest Priority Factors**:
  - All pollens (tree, grass, weed)
  - Mold spores
  - Fine particulate matter (PM2.5)
  - Ozone (O3)
  - Nitrogen dioxide (NO2)
  - Sulfur dioxide (SO2)
  - Volatile organic compounds (VOCs)
  - Animal dander (indoor environments)

### Group 2: Mild to Moderate Allergic
- **Primary Factors**:
  - Pollens (seasonal triggers)
  - Mold spores
  - Particulate matter (PM2.5, PM10)
  - Ozone (O3)
  - Nitrogen dioxide (NO2)
  - Carbon monoxide (CO)

### Group 3: Possible Allergic/High Risk
- **Key Monitoring Factors**:
  - Particulate matter (PM2.5, PM10)
  - Pollens and mold spores
  - Nitrogen dioxide (NO2) and sulfur dioxide (SO2)
  - Ozone (O3)
  - Volatile organic compounds (VOCs)

### Group 4: Not Yet Diagnosed
- **General Air Quality Indicators**:
  - Particulate matter (PM2.5, PM10)
  - Ozone (O3)
  - Nitrogen dioxide (NO2)
  - Sulfur dioxide (SO2) and carbon monoxide (CO)
  - General pollen and mold spore levels

### Group 5: Vulnerable Population
- **Critical Factors**:
  - All allergens (pollens, mold spores, animal dander)
  - All particulate matter types (PM2.5, PM10, ultrafine particles)
  - Gaseous pollutants (O3, NO2, SO2, CO, VOCs)
  - Temperature and humidity extremes

### Universal Factors Important for All Groups
- Air Quality Index (AQI)
- Temperature and humidity
- Wind direction and speed
- Precipitation

## Feature Importance Analysis Results

Our machine learning analysis has determined the following feature importance ranking for each group:

### Group 1: Severe Allergic Asthma
1. PM2.5 (fine particulate matter)
2. Tree pollen
3. Grass pollen
4. Weed pollen
5. Ozone
6. Nitrogen dioxide
7. Relative humidity
8. Temperature
9. Sulfur dioxide
10. Mold spore proxies (soil moisture + precipitation)

### Group 2: Mild to Moderate Allergic
1. PM10 (particulate matter)
2. PM2.5 (fine particulate matter)
3. Tree pollen
4. Grass pollen
5. Ozone
6. Relative humidity
7. Temperature
8. Nitrogen dioxide
9. Wind speed
10. Precipitation

### Group 3: Possible Allergic/High Risk
1. PM2.5 (fine particulate matter)
2. PM10 (particulate matter)
3. Ozone
4. Tree pollen
5. Nitrogen dioxide
6. Temperature
7. Humidity
8. Sulfur dioxide
9. Grass pollen
10. Weed pollen

### Group 4: Not Yet Diagnosed
1. Air Quality Index (composite)
2. PM10 (particulate matter)
3. Ozone
4. Nitrogen dioxide
5. Temperature
6. Humidity
7. PM2.5 (fine particulate matter)
8. Carbon monoxide
9. Sulfur dioxide
10. General pollen levels

### Group 5: Vulnerable Population
1. PM2.5 (fine particulate matter)
2. Temperature extremes
3. Humidity extremes
4. Ozone
5. All pollen types
6. Nitrogen dioxide
7. PM10 (particulate matter)
8. Sulfur dioxide
9. Carbon monoxide
10. Precipitation (mold growth indicator)

## Clinical Immunology Insights

From an immunological perspective, our model's feature importance rankings align with clinical understanding of allergy mechanisms:

### Group 1 (Severe Allergic Asthma)
These patients have heightened IgE-mediated responses and often experience bronchial hyperreactivity. Fine particulates (PM2.5) can penetrate deep into the airways, carrying allergens and acting as adjuvants that enhance allergenic potential. The synergistic effect between pollutants like ozone and nitrogen dioxide with biological allergens (pollens) creates a particularly hazardous environment for these individuals.

### Group 2 (Mild to Moderate Allergic)
While still experiencing IgE-mediated hypersensitivity, these individuals typically have better compensatory mechanisms. However, the combination of multiple environmental triggers can overwhelm these defenses, leading to symptom exacerbation. PM10 particles primarily affect upper airways, corresponding to the common symptoms in this group.

### Group 3 (Possible Allergic/High Risk)
These individuals often show subclinical immune dysregulation or genetic predisposition without full-blown allergic disease. Long-term exposure to particulate matter and pollutants may contribute to airway inflammation and eventual sensitization to allergens, potentially leading to progression to Groups 1 or 2.

### Group 4 (Not Yet Diagnosed)
General air quality impacts overall respiratory health even in those without specific allergic tendencies. Poor air quality may contribute to non-specific respiratory symptoms that could be confused with allergies or increase susceptibility to respiratory infections.

### Group 5 (Vulnerable Population)
The developing immune system in children and the senescent immune system in the elderly are particularly susceptible to environmental insults. PM2.5 and temperature/humidity extremes are particularly impactful due to underdeveloped/compromised thermoregulatory and respiratory defenses in these populations.
