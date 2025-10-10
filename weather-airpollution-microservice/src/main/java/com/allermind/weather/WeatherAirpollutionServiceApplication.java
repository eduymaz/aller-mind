package com.allermind.weather;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class WeatherAirpollutionServiceApplication {

	public static void main(String[] args) {
		SpringApplication.run(WeatherAirpollutionServiceApplication.class, args);
	}

}
