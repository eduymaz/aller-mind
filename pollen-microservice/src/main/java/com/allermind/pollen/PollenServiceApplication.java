package com.allermind.pollen;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class PollenServiceApplication {

	public static void main(String[] args) {
		SpringApplication.run(PollenServiceApplication.class, args);
	}

}
