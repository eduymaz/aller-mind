package com.allermind.pollen_service;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

@SpringBootApplication(scanBasePackages = {"com.allermind.pollen_service", "com.allermind.pollen"})
@EnableJpaRepositories(basePackages = "com.allermind.pollen.repository")
@EntityScan(basePackages = "com.allermind.pollen.model")
public class PollenServiceApplication {

	public static void main(String[] args) {
		SpringApplication.run(PollenServiceApplication.class, args);
	}

}
