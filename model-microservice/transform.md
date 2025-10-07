# AllerMind User Preference System - Python to Java Transformation Guide

## 📋 Overview
Bu doküman, `user_preference_system.py` dosyasının Java 21 ve Spring Framework kullanılarak modern, maintainable ve SOLID prensiplere uygun bir şekilde dönüştürülmesi için kapsamlı bir rehber sağlar.

## 🏗️ Architecture Overview

### Domain-Driven Design (DDD) Approach
- **Bounded Context**: Allergy Management Domain
- **Ubiquitous Language**: Alerji terminolojisi ve medikal kavramlar
- **Hexagonal Architecture**: Clean Architecture prensiplerine uygun katmanlı yapı

### Core Principles
- **SOLID Principles**: Tüm sınıflar ve interfaceler SOLID prensiplere uygun
- **Design Patterns**: Strategy, Factory, Builder, Observer patterns
- **Clean Code**: Readable, maintainable, testable kod
- **DDD**: Domain Model, Value Objects, Aggregates, Domain Services

## 📊 Current Python Code Analysis

### Main Components Identified:

1. **ALLERGY_GROUPS (Dictionary)**: 5 farklı alerji grubu tanımı
2. **UserPreferences (Dataclass)**: Kullanıcı tercihleri ve sağlık bilgileri
3. **AllergyGroupClassifier (Class)**: Ana sınıflandırma algoritması

### Key Functionalities:
- İmmünolojik profil değerlendirmesi
- Risk skoru hesaplama
- Çapraz reaksiyon analizi
- Yaş bazlı vulnerabilite değerlendirmesi
- Kişisel risk modifikasyonları

## 🎯 Java Transformation Strategy

### 1. Project Structure (Hexagonal Architecture)

```
com.allermind.userpreference/
├── application/
│   ├── service/
│   │   └── UserPreferenceApplicationService.java
│   ├── port/
│   │   ├── in/
│   │   │   └── AllergyGroupClassificationUseCase.java
│   │   └── out/
│   │       ├── AllergyGroupRepository.java
│   │       └── UserPreferenceRepository.java
│   └── dto/
│       ├── AllergyClassificationRequest.java
│       └── AllergyClassificationResponse.java
├── domain/
│   ├── model/
│   │   ├── aggregate/
│   │   │   └── UserPreference.java
│   │   ├── entity/
│   │   │   ├── AllergyGroup.java
│   │   │   └── User.java
│   │   ├── valueobject/
│   │   │   ├── Age.java
│   │   │   ├── Location.java
│   │   │   ├── RiskScore.java
│   │   │   ├── ImmunologicProfile.java
│   │   │   └── PollenSensitivity.java
│   │   └── enums/
│   │       ├── ClinicalDiagnosis.java
│   │       ├── Gender.java
│   │       ├── PollenType.java
│   │       └── AllergyGroupType.java
│   ├── service/
│   │   ├── AllergyGroupClassifierDomainService.java
│   │   ├── RiskCalculationService.java
│   │   └── CrossReactivityService.java
│   └── exception/
│       └── AllergyClassificationException.java
├── infrastructure/
│   ├── adapter/
│   │   ├── in/
│   │   │   └── web/
│   │   │       └── AllergyClassificationController.java
│   │   └── out/
│   │       ├── persistence/
│   │       │   ├── AllergyGroupJpaRepository.java
│   │       │   └── UserPreferenceJpaRepository.java
│   │       └── external/
│   └── configuration/
│       ├── BeanConfiguration.java
│       └── JpaConfiguration.java
└── shared/
    ├── constant/
    │   └── AllergyConstants.java
    └── util/
        └── ValidationUtils.java
```

### 2. Maven Dependencies (pom.xml)

```xml
<!-- Spring Boot Starters -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-validation</artifactId>
</dependency>

<!-- Database -->
<dependency>
    <groupId>com.h2database</groupId>
    <artifactId>h2</artifactId>
    <scope>runtime</scope>
</dependency>

<!-- Utilities -->
<dependency>
    <groupId>org.mapstruct</groupId>
    <artifactId>mapstruct</artifactId>
    <version>1.5.5.Final</version>
</dependency>
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
</dependency>

<!-- Testing -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
</dependency>
```

### 3. Domain Model Design

#### 3.1 Value Objects

**Age.java** (Value Object)
```java
public record Age(int value) {
    public Age {
        if (value < 0 || value > 150) {
            throw new IllegalArgumentException("Invalid age: " + value);
        }
    }
    
    public boolean isVulnerable() {
        return value <= 12 || value >= 65;
    }
    
    public boolean isChild() {
        return value <= 12;
    }
    
    public boolean isElderly() {
        return value >= 65;
    }
}
```

**Location.java** (Value Object)
```java
public record Location(
    @NotNull @DecimalMax("90") @DecimalMin("-90") BigDecimal latitude,
    @NotNull @DecimalMax("180") @DecimalMin("-180") BigDecimal longitude
) {
    public Location {
        Objects.requireNonNull(latitude, "Latitude cannot be null");
        Objects.requireNonNull(longitude, "Longitude cannot be null");
    }
}
```

**RiskScore.java** (Value Object)
```java
public record RiskScore(BigDecimal value) {
    private static final BigDecimal MIN_SCORE = BigDecimal.ZERO;
    private static final BigDecimal MAX_SCORE = BigDecimal.ONE;
    
    public RiskScore {
        if (value.compareTo(MIN_SCORE) < 0 || value.compareTo(MAX_SCORE) > 0) {
            throw new IllegalArgumentException("Risk score must be between 0 and 1");
        }
    }
    
    public boolean isHigh() {
        return value.compareTo(new BigDecimal("0.7")) >= 0;
    }
    
    public boolean isModerate() {
        return value.compareTo(new BigDecimal("0.4")) >= 0 && 
               value.compareTo(new BigDecimal("0.7")) < 0;
    }
}
```

#### 3.2 Enums

**ClinicalDiagnosis.java**
```java
public enum ClinicalDiagnosis {
    NONE("none"),
    MILD_MODERATE_ALLERGY("mild_moderate_allergy"),
    SEVERE_ALLERGY("severe_allergy"),
    ASTHMA("asthma");
    
    private final String value;
    
    ClinicalDiagnosis(String value) {
        this.value = value;
    }
    
    public AllergyGroupType toAllergyGroupType() {
        return switch (this) {
            case SEVERE_ALLERGY -> AllergyGroupType.SEVERE_ALLERGIC;
            case MILD_MODERATE_ALLERGY -> AllergyGroupType.MILD_MODERATE_ALLERGIC;
            default -> null;
        };
    }
}
```

**AllergyGroupType.java**
```java
public enum AllergyGroupType {
    SEVERE_ALLERGIC(1, "Şiddetli Alerjik Grup", 0.28),
    MILD_MODERATE_ALLERGIC(2, "Hafif-Orta Alerjik Grup", 0.22),
    GENETIC_PREDISPOSITION(3, "Genetik Yatkınlık Grubu", 0.24),
    UNDIAGNOSED(4, "Teşhis Almamış Grup", 0.24),
    VULNERABLE_POPULATION(5, "Hassas Çocuk/Yaşlı Grubu", 0.12);
    
    private final int id;
    private final String name;
    private final double weight;
    
    AllergyGroupType(int id, String name, double weight) {
        this.id = id;
        this.name = name;
        this.weight = weight;
    }
    
    // Getters...
}
```

#### 3.3 Entities and Aggregates

**AllergyGroup.java** (Entity)
```java
@Entity
@Table(name = "allergy_groups")
public class AllergyGroup {
    @Id
    private AllergyGroupType type;
    
    @Column(nullable = false)
    private String description;
    
    @Embedded
    private ImmunologicProfile immunologicProfile;
    
    @Column(nullable = false)
    private BigDecimal weight;
    
    // Constructors, getters, setters...
}
```

**UserPreference.java** (Aggregate Root)
```java
@Entity
@Table(name = "user_preferences")
public class UserPreference {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;
    
    @Embedded
    @AttributeOverrides({
        @AttributeOverride(name = "value", column = @Column(name = "age"))
    })
    private Age age;
    
    @Enumerated(EnumType.STRING)
    private Gender gender;
    
    @Embedded
    private Location location;
    
    @Enumerated(EnumType.STRING)
    private ClinicalDiagnosis clinicalDiagnosis;
    
    @Column(name = "family_allergy_history")
    private Boolean familyAllergyHistory;
    
    @ElementCollection
    @CollectionTable(name = "previous_allergic_reactions")
    @MapKeyEnumerated(EnumType.STRING)
    private Map<AllergyReactionType, Boolean> previousAllergicReactions = new HashMap<>();
    
    @ElementCollection
    @CollectionTable(name = "current_medications")
    private Set<String> currentMedications = new HashSet<>();
    
    @Embedded
    private PollenSensitivityProfile pollenSensitivityProfile;
    
    @ElementCollection
    @CollectionTable(name = "food_allergies")
    @MapKeyEnumerated(EnumType.STRING)
    private Map<FoodType, Boolean> foodAllergies = new HashMap<>();
    
    @ElementCollection
    @CollectionTable(name = "environmental_triggers")
    @MapKeyEnumerated(EnumType.STRING)
    private Map<EnvironmentalTrigger, Boolean> environmentalTriggers = new HashMap<>();
    
    // Constructors, getters, business methods...
    
    public boolean hasVulnerableAge() {
        return age.isVulnerable();
    }
    
    public boolean hasFamilyHistory() {
        return Boolean.TRUE.equals(familyAllergyHistory);
    }
    
    public int getEnvironmentalTriggerCount() {
        return (int) environmentalTriggers.values().stream()
            .mapToLong(trigger -> trigger ? 1 : 0)
            .sum();
    }
}
```

### 4. Domain Services

**AllergyGroupClassifierDomainService.java**
```java
@DomainService
public class AllergyGroupClassifierDomainService {
    
    private final RiskCalculationService riskCalculationService;
    private final CrossReactivityService crossReactivityService;
    private final AllergyGroupRepository allergyGroupRepository;
    
    public AllergyGroupClassifierDomainService(
            RiskCalculationService riskCalculationService,
            CrossReactivityService crossReactivityService,
            AllergyGroupRepository allergyGroupRepository) {
        this.riskCalculationService = riskCalculationService;
        this.crossReactivityService = crossReactivityService;
        this.allergyGroupRepository = allergyGroupRepository;
    }
    
    public AllergyClassificationResult classifyAllergyGroup(UserPreference userPreference) {
        // 1. Age vulnerability assessment
        if (userPreference.hasVulnerableAge()) {
            return createClassificationResult(
                AllergyGroupType.VULNERABLE_POPULATION,
                userPreference,
                "Age-based vulnerability: " + userPreference.getAge().value()
            );
        }
        
        // 2. Clinical diagnosis assessment
        AllergyGroupType clinicalGroup = assessClinicalStatus(userPreference.getClinicalDiagnosis());
        if (clinicalGroup != null) {
            return createClassificationResult(
                clinicalGroup,
                userPreference,
                "Clinical diagnosis based"
            );
        }
        
        // 3. Pollen sensitivity and genetic predisposition
        RiskScore pollenRiskScore = riskCalculationService.calculatePollenRiskScore(userPreference);
        
        if (userPreference.hasFamilyHistory() && pollenRiskScore.isHigh()) {
            return createClassificationResult(
                AllergyGroupType.GENETIC_PREDISPOSITION,
                userPreference,
                String.format("Genetic predisposition + high pollen risk (%.2f)", pollenRiskScore.value())
            );
        }
        
        // Default: Undiagnosed group
        return createClassificationResult(
            AllergyGroupType.UNDIAGNOSED,
            userPreference,
            String.format("Undiagnosed, pollen risk: %.2f", pollenRiskScore.value())
        );
    }
    
    private AllergyGroupType assessClinicalStatus(ClinicalDiagnosis diagnosis) {
        return diagnosis.toAllergyGroupType();
    }
    
    private AllergyClassificationResult createClassificationResult(
            AllergyGroupType groupType,
            UserPreference userPreference,
            String reason) {
        
        AllergyGroup group = allergyGroupRepository.findByType(groupType)
            .orElseThrow(() -> new AllergyClassificationException("Group not found: " + groupType));
        
        PersonalRiskModifiers modifiers = calculatePersonalModifiers(userPreference, groupType);
        EnvironmentalSensitivityFactors envFactors = extractEnvironmentalFactors(userPreference);
        PollenSpecificRisks pollenRisks = crossReactivityService.calculatePollenSpecificRisks(userPreference);
        RecommendationAdjustments recommendations = calculateRecommendationAdjustments(userPreference, groupType);
        
        return AllergyClassificationResult.builder()
            .groupType(groupType)
            .groupName(group.getName())
            .groupDescription(group.getDescription())
            .assignmentReason(reason)
            .modelWeight(group.getWeight())
            .personalRiskModifiers(modifiers)
            .immunologicProfile(group.getImmunologicProfile())
            .environmentalSensitivityFactors(envFactors)
            .pollenSpecificRisks(pollenRisks)
            .recommendationAdjustments(recommendations)
            .build();
    }
    
    // Additional helper methods...
}
```

**RiskCalculationService.java**
```java
@DomainService
public class RiskCalculationService {
    
    private final Map<PollenType, BigDecimal> pollenRiskWeights;
    private final CrossReactivityService crossReactivityService;
    
    public RiskCalculationService(CrossReactivityService crossReactivityService) {
        this.crossReactivityService = crossReactivityService;
        this.pollenRiskWeights = initializePollenRiskWeights();
    }
    
    public RiskScore calculatePollenRiskScore(UserPreference userPreference) {
        BigDecimal riskScore = BigDecimal.ZERO;
        
        // Tree pollen sensitivity calculation
        riskScore = riskScore.add(
            calculateCategoryRisk(
                userPreference.getPollenSensitivityProfile().getTreePollenAllergies(),
                new BigDecimal("0.3")
            )
        );
        
        // Grass pollen sensitivity calculation
        riskScore = riskScore.add(
            calculateCategoryRisk(
                userPreference.getPollenSensitivityProfile().getGrassPollenAllergies(),
                new BigDecimal("0.4")
            )
        );
        
        // Weed pollen sensitivity calculation
        riskScore = riskScore.add(
            calculateCategoryRisk(
                userPreference.getPollenSensitivityProfile().getWeedPollenAllergies(),
                new BigDecimal("0.4")
            )
        );
        
        // Add cross-reactivity bonus
        BigDecimal crossReactivityBonus = crossReactivityService
            .calculateCrossReactivityRisk(userPreference);
        riskScore = riskScore.add(crossReactivityBonus);
        
        // Normalize to 0-1 range
        BigDecimal normalizedScore = riskScore.min(BigDecimal.ONE);
        
        return new RiskScore(normalizedScore);
    }
    
    private BigDecimal calculateCategoryRisk(
            Map<PollenType, Boolean> sensitivities,
            BigDecimal categoryWeight) {
        
        return sensitivities.entrySet().stream()
            .filter(Map.Entry::getValue)
            .map(entry -> pollenRiskWeights.getOrDefault(entry.getKey(), BigDecimal.ZERO))
            .reduce(BigDecimal.ZERO, BigDecimal::add)
            .multiply(categoryWeight);
    }
    
    private Map<PollenType, BigDecimal> initializePollenRiskWeights() {
        Map<PollenType, BigDecimal> weights = new EnumMap<>(PollenType.class);
        
        // Tree pollens
        weights.put(PollenType.BIRCH, new BigDecimal("0.9"));
        weights.put(PollenType.OLIVE, new BigDecimal("0.5"));
        weights.put(PollenType.PINE, new BigDecimal("0.6"));
        weights.put(PollenType.OAK, new BigDecimal("0.8"));
        weights.put(PollenType.CEDAR, new BigDecimal("0.7"));
        
        // Grass pollens
        weights.put(PollenType.GRAMINALES, new BigDecimal("1.0"));
        
        // Weed pollens
        weights.put(PollenType.RAGWEED, new BigDecimal("1.3"));
        weights.put(PollenType.MUGWORT, new BigDecimal("1.1"));
        weights.put(PollenType.PLANTAIN, new BigDecimal("1.0"));
        weights.put(PollenType.NETTLE, new BigDecimal("0.9"));
        
        return Collections.unmodifiableMap(weights);
    }
}
```

### 5. Application Services

**UserPreferenceApplicationService.java**
```java
@Service
@Transactional
public class UserPreferenceApplicationService implements AllergyGroupClassificationUseCase {
    
    private final AllergyGroupClassifierDomainService classifierDomainService;
    private final UserPreferenceRepository userPreferenceRepository;
    private final AllergyClassificationMapper mapper;
    
    public UserPreferenceApplicationService(
            AllergyGroupClassifierDomainService classifierDomainService,
            UserPreferenceRepository userPreferenceRepository,
            AllergyClassificationMapper mapper) {
        this.classifierDomainService = classifierDomainService;
        this.userPreferenceRepository = userPreferenceRepository;
        this.mapper = mapper;
    }
    
    @Override
    public AllergyClassificationResponse classifyAllergy(AllergyClassificationRequest request) {
        // Convert request to domain object
        UserPreference userPreference = mapper.toDomain(request);
        
        // Validate domain object
        validateUserPreference(userPreference);
        
        // Classify allergy group
        AllergyClassificationResult result = classifierDomainService
            .classifyAllergyGroup(userPreference);
        
        // Save user preference
        UserPreference savedPreference = userPreferenceRepository.save(userPreference);
        
        // Convert to response
        return mapper.toResponse(result, savedPreference);
    }
    
    private void validateUserPreference(UserPreference userPreference) {
        if (userPreference.getAge() == null) {
            throw new ValidationException("Age is required");
        }
        
        if (userPreference.getLocation() == null) {
            throw new ValidationException("Location is required");
        }
        
        // Additional validations...
    }
}
```

### 6. Infrastructure Layer

**AllergyClassificationController.java**
```java
@RestController
@RequestMapping("/api/v1/allergy-classification")
@Validated
public class AllergyClassificationController {
    
    private final AllergyGroupClassificationUseCase classificationUseCase;
    
    public AllergyClassificationController(AllergyGroupClassificationUseCase classificationUseCase) {
        this.classificationUseCase = classificationUseCase;
    }
    
    @PostMapping("/classify")
    public ResponseEntity<AllergyClassificationResponse> classifyAllergy(
            @Valid @RequestBody AllergyClassificationRequest request) {
        
        AllergyClassificationResponse response = classificationUseCase.classifyAllergy(request);
        return ResponseEntity.ok(response);
    }
    
    @ExceptionHandler(ValidationException.class)
    public ResponseEntity<ErrorResponse> handleValidationException(ValidationException ex) {
        ErrorResponse error = ErrorResponse.builder()
            .message(ex.getMessage())
            .timestamp(Instant.now())
            .build();
        return ResponseEntity.badRequest().body(error);
    }
}
```

### 7. Configuration

**BeanConfiguration.java**
```java
@Configuration
@EnableJpaRepositories(basePackages = "com.allermind.userpreference.infrastructure.adapter.out.persistence")
public class BeanConfiguration {
    
    @Bean
    public AllergyGroupClassifierDomainService allergyGroupClassifierDomainService(
            RiskCalculationService riskCalculationService,
            CrossReactivityService crossReactivityService,
            AllergyGroupRepository allergyGroupRepository) {
        return new AllergyGroupClassifierDomainService(
            riskCalculationService, 
            crossReactivityService, 
            allergyGroupRepository
        );
    }
    
    @Bean
    public RiskCalculationService riskCalculationService(
            CrossReactivityService crossReactivityService) {
        return new RiskCalculationService(crossReactivityService);
    }
    
    @Bean
    public CrossReactivityService crossReactivityService() {
        return new CrossReactivityService();
    }
}
```

### 8. Testing Strategy

**Unit Tests Example:**
```java
@ExtendWith(MockitoExtension.class)
class AllergyGroupClassifierDomainServiceTest {
    
    @Mock
    private RiskCalculationService riskCalculationService;
    
    @Mock
    private CrossReactivityService crossReactivityService;
    
    @Mock
    private AllergyGroupRepository allergyGroupRepository;
    
    @InjectMocks
    private AllergyGroupClassifierDomainService classifierService;
    
    @Test
    void shouldClassifyAsVulnerablePopulationForChild() {
        // Given
        UserPreference childPreference = UserPreferenceTestDataBuilder.aChild()
            .withAge(8)
            .build();
        
        AllergyGroup vulnerableGroup = AllergyGroupTestDataBuilder.vulnerablePopulationGroup()
            .build();
        
        when(allergyGroupRepository.findByType(AllergyGroupType.VULNERABLE_POPULATION))
            .thenReturn(Optional.of(vulnerableGroup));
        
        // When
        AllergyClassificationResult result = classifierService.classifyAllergyGroup(childPreference);
        
        // Then
        assertThat(result.getGroupType()).isEqualTo(AllergyGroupType.VULNERABLE_POPULATION);
        assertThat(result.getAssignmentReason()).contains("Age-based vulnerability: 8");
    }
    
    // More test methods...
}
```

### 9. Key Design Patterns Applied

#### 9.1 Strategy Pattern
- **RiskCalculationStrategy**: Farklı risk hesaplama algoritmaları
- **ClassificationStrategy**: Grup sınıflandırma stratejileri

#### 9.2 Factory Pattern
- **AllergyGroupFactory**: AllergyGroup nesnelerini oluşturmak için
- **UserPreferenceFactory**: Test ve varsayılan nesneler için

#### 9.3 Builder Pattern
- **AllergyClassificationResult.Builder**: Karmaşık sonuç nesnelerini oluşturmak için
- **UserPreference.Builder**: Fluent API ile kullanıcı tercihleri oluşturmak için

#### 9.4 Repository Pattern
- **AllergyGroupRepository**: Domain ile infrastructure arasında soyutlama
- **UserPreferenceRepository**: CRUD operations için clean interface

### 10. Migration Checklist

#### Phase 1: Domain Model Setup
- [ ] Value Objects implementasyonu (Age, Location, RiskScore)
- [ ] Enum sınıfları (ClinicalDiagnosis, AllergyGroupType, etc.)
- [ ] Entity sınıfları (AllergyGroup, UserPreference)
- [ ] Domain Exception sınıfları

#### Phase 2: Domain Services
- [ ] AllergyGroupClassifierDomainService
- [ ] RiskCalculationService
- [ ] CrossReactivityService
- [ ] Unit testleri

#### Phase 3: Application Layer
- [ ] Use Case interfaces
- [ ] Application Services
- [ ] DTO sınıfları
- [ ] Mapper sınıfları (MapStruct)

#### Phase 4: Infrastructure Layer
- [ ] JPA Repository implementasyonları
- [ ] REST Controller
- [ ] Configuration sınıfları
- [ ] Integration testler

#### Phase 5: Testing & Documentation
- [ ] Comprehensive unit tests
- [ ] Integration tests
- [ ] API documentation (Swagger/OpenAPI)
- [ ] Performance tests

### 11. Performance Considerations

#### 11.1 Caching Strategy
```java
@Cacheable(value = "allergyGroups", key = "#groupType")
public Optional<AllergyGroup> findByType(AllergyGroupType groupType) {
    // Implementation
}
```

#### 11.2 Database Optimization
- Proper indexing on frequently queried fields
- Connection pooling configuration
- Query optimization with JPA criteria API

#### 11.3 Monitoring & Observability
```java
@Component
public class AllergyClassificationMetrics {
    
    private final MeterRegistry meterRegistry;
    private final Counter classificationCounter;
    
    public AllergyClassificationMetrics(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
        this.classificationCounter = Counter.builder("allergy.classification.total")
            .description("Total number of allergy classifications")
            .tag("application", "allermind")
            .register(meterRegistry);
    }
    
    public void recordClassification(AllergyGroupType groupType) {
        classificationCounter.increment(Tags.of("group.type", groupType.name()));
    }
}
```

### 12. Security Considerations

#### 12.1 Data Protection
- Personal health information encryption
- GDPR compliance for user data
- Audit logging for sensitive operations

#### 12.2 API Security
```java
@PreAuthorize("hasRole('USER') or hasRole('ADMIN')")
@PostMapping("/classify")
public ResponseEntity<AllergyClassificationResponse> classifyAllergy(
        @Valid @RequestBody AllergyClassificationRequest request) {
    // Implementation
}
```

### 13. Deployment & DevOps

#### 13.1 Docker Configuration
```dockerfile
FROM openjdk:21-jdk-slim

WORKDIR /app
COPY target/allermind-user-preference-service.jar app.jar

EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

#### 13.2 Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: allermind-user-preference-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: allermind-user-preference-service
  template:
    metadata:
      labels:
        app: allermind-user-preference-service
    spec:
      containers:
      - name: app
        image: allermind/user-preference-service:latest
        ports:
        - containerPort: 8080
        env:
        - name: SPRING_PROFILES_ACTIVE
          value: "production"
```

## 🚀 Next Steps

1. **Setup Development Environment**: Java 21, Maven, IDE configuration
2. **Create Base Project Structure**: Maven module, package organization
3. **Implement Domain Layer First**: Value objects, entities, domain services
4. **Add Application Layer**: Use cases, application services
5. **Build Infrastructure Layer**: Repositories, controllers, configurations
6. **Comprehensive Testing**: Unit, integration, performance tests
7. **Documentation**: API docs, architectural decisions
8. **Production Deployment**: CI/CD pipeline, monitoring, logging

## 📚 References

- **Domain-Driven Design**: Eric Evans - "Domain-Driven Design: Tackling Complexity in the Heart of Software"
- **Clean Architecture**: Robert C. Martin - "Clean Architecture: A Craftsman's Guide to Software Structure and Design"
- **Spring Boot Reference**: https://docs.spring.io/spring-boot/docs/current/reference/html/
- **Java 21 Features**: https://openjdk.org/projects/jdk/21/

---

**Document Version**: 1.0  
**Last Updated**: 2025-09-20  
**Author**: AllerMind Development Team