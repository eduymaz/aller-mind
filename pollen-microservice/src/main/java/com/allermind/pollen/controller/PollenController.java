package com.allermind.pollen.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.allermind.pollen.dto.PollenResponse;
import com.allermind.pollen.service.PollenService;

@RestController
@RequestMapping("/api/pollen")
public class PollenController {

    @Autowired
    private PollenService pollenService;

    @GetMapping
    public ResponseEntity<List<PollenResponse>> getPollenData(
            @RequestParam String lat,
            @RequestParam String lon) {
        List<PollenResponse> responses = pollenService.getPollenDataByLatLon(lat, lon);
        return ResponseEntity.ok(responses);
    }
}
