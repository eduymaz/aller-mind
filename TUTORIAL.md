# Allermind: Data Acquisition Tutorial

Welcome to the Allermind data acquisition tutorial. This guide provides a comprehensive overview of the Allermind application's data pipeline, including its directory structure, module responsibilities, and the rationale behind each component. The documentation is designed to be clear, precise, and maintainable, following best practices in software engineering and scientific computing.

---

## Directory Structure

```
aller-mind/
│
├── allermind-weather/
│   ├── main.py
│   ├── service.py
│   ├── domain.py
│   ├── repository.py
│   ├── merge.py
│   ├── exporter.py
│   ├── city.csv
│   ├── country.csv
│   ├── output.csv
│   └── sample.csv
│
├── allermind-pollen/
│   ├── pollen_main.py
│   ├── pollen_service.py
│   ├── pollen_exporter.py
│   ├── city.csv
│   ├── pollen_output.csv
│   └── google-pollen-response.json
│
├── dataset/
│   ├── analysis.ipynb
│   ├── analysis.py
│   ├── city_output.csv
│   ├── aug14_pollen_output.csv
│   ├── merge_data.csv
│   └── 14aug_city_output.csv
│
└── TUTORIAL.md
```

---

## Module Overview

### allermind-weather

**Purpose:**  
Automates the retrieval, enrichment, and storage of weather and air quality data for all Turkish cities and districts using the Open-Meteo API.

**Key Components:**

- `main.py`  
  Orchestrates the data pipeline. Iterates over all cities/districts, triggers API requests, and manages output generation.

- `service.py`  
  Encapsulates API communication logic. Handles HTTP requests and parses JSON responses into Python domain objects.

- `domain.py`  
  Defines core data models (e.g., `City`, `Country`, `WeatherData`, `AirQualityData`, `CombinedData`) using Python dataclasses for type safety and clarity.

- `repository.py`  
  Abstracts data access from CSV sources. Provides robust, reusable methods for reading city and district metadata.

- `merge.py`  
  Implements logic for merging weather and air quality datasets on a per-hour basis, ensuring data consistency and enrichment.

- `exporter.py`  
  Responsible for writing processed data to CSV files. Handles column selection, header management, and incremental writing for memory efficiency.

- `city.csv` / `country.csv`  
  Contain geospatial metadata for cities and districts, including latitude and longitude coordinates.

- `output.csv` / `sample.csv`  
  Store the final, processed datasets ready for downstream analysis.

**Design Principles:**  
- Single Responsibility: Each module addresses a distinct concern.
- Domain-Driven Design: Data models reflect real-world entities.
- Maintainability: Modular, extensible, and testable codebase.

---

### allermind-pollen

**Purpose:**  
Fetches and structures pollen forecast data for all Turkish cities using the Google Pollen API, enabling allergy risk analysis and environmental reporting.

**Key Components:**

- `pollen_main.py`  
  Coordinates the pollen data acquisition workflow. Reads city metadata, invokes API requests, and manages CSV output.

- `pollen_service.py`  
  Handles API interactions and transforms JSON responses into structured Python objects (`PollenTypeInfo`, `PollenResponse`).

- `pollen_exporter.py`  
  Serializes pollen data into CSV format, ensuring correct column mapping and encoding.

- `city.csv`  
  Provides city names and coordinates for API queries.

- `pollen_output.csv`  
  Contains the consolidated pollen forecast data for all cities.

- `google-pollen-response.json`  
  Example API response for reference and testing.

**Design Principles:**  
- Separation of Concerns: API logic, data modeling, and export routines are isolated.
- Extensibility: Easily adaptable to new pollen types or API changes.

---

### dataset

**Purpose:**  
Facilitates exploratory data analysis, merging, and reporting using Python and Jupyter Notebook. Enables users to manipulate, visualize, and combine weather and pollen datasets.

**Key Components:**

- `analysis.ipynb`  
  Interactive notebook for data cleaning, transformation, and visualization. Demonstrates best practices in pandas usage and scientific reporting.

- `analysis.py`  
  Script-based alternative for batch data processing and merging.

- `city_output.csv`, `aug14_pollen_output.csv`, `merge_data.csv`, `14aug_city_output.csv`  
  Intermediate and final datasets produced during analysis and merging steps.

**Design Principles:**  
- Reproducibility: All analysis steps are documented and executable.
- Clarity: Code and markdown cells are annotated for transparency.

---

## Data Acquisition Workflow

1. **Metadata Loading:**  
   - Read city and district information from CSV files.

2. **API Querying:**  
   - For each location, construct and send requests to Open-Meteo and Google Pollen APIs.
   - Parse responses into domain objects.

3. **Data Enrichment:**  
   - Merge weather and air quality data on a per-hour basis.
   - Enrich with city/district metadata.
   - Integrate pollen indices for each city.

4. **Export:**  
   - Write enriched datasets to CSV files, ensuring correct column structure and encoding.

5. **Analysis:**  
   - Use Jupyter Notebook or Python scripts to further process, merge, and visualize data.

---

## Best Practices & Rationale

- **Modularity:**  
  Each module is designed for a single purpose, facilitating maintenance and future extension.

- **Type Safety:**  
  Domain models use dataclasses for explicit typing, reducing runtime errors.

- **Efficiency:**  
  Data is written incrementally to CSV to minimize memory usage during large-scale processing.

- **Extensibility:**  
  The pipeline can be easily adapted to new data sources, additional cities, or new environmental indices.

- **Documentation:**  
  Inline comments and markdown cells provide context and usage examples, supporting onboarding and reproducibility.

---

## Getting Started

1. **Install Dependencies:**  
   - Ensure Python 3.8+ and required libraries (e.g., `requests`, `pandas`) are installed.

2. **Configure Metadata:**  
   - Update `city.csv` and `country.csv` as needed for your analysis.

3. **Run Data Acquisition:**  
   - Execute `main.py` in `allermind-weather` and `pollen_main.py` in `allermind-pollen` to generate datasets.

4. **Analyze Data:**  
   - Open `analysis.ipynb` in Jupyter Notebook for interactive exploration.

---

## Support & Contribution

For bug reports, feature requests, or contributions, please refer to the project repository and follow the contribution guidelines.

---

This tutorial aims to provide a robust, maintainable, and extensible foundation for environmental data acquisition and analysis in the Allermind project.
