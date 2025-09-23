package com.allermind.userpreference.infrastructure.configuration;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

import com.allermind.userpreference.domain.service.AllergyGroupClassifierDomainService;
import com.allermind.userpreference.domain.service.CrossReactivityService;
import com.allermind.userpreference.domain.service.RiskCalculationService;

@Configuration
@EnableJpaRepositories(basePackages = "com.allermind.userpreference.infrastructure.adapter.out.persistence")
public class BeanConfiguration {
    
    @Bean
    public CrossReactivityService crossReactivityService() {
        return new CrossReactivityService();
    }
    
    @Bean
    public RiskCalculationService riskCalculationService(CrossReactivityService crossReactivityService) {
        return new RiskCalculationService(crossReactivityService);
    }
    
    @Bean
    public AllergyGroupClassifierDomainService allergyGroupClassifierDomainService(
            RiskCalculationService riskCalculationService,
            CrossReactivityService crossReactivityService) {
        return new AllergyGroupClassifierDomainService(riskCalculationService, crossReactivityService);
    }
}