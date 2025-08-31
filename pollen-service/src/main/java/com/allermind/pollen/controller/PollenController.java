package com.allermind.pollen.controller;

import com.allermind.pollen.dto.PollenResponse;
import com.allermind.pollen.service.PollenService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/pollen")
public class PollenController {

    @Autowired
    private PollenService pollenService;

    @GetMapping
    public ResponseEntity<List<PollenResponse>> getPollenData(
            @RequestParam(required = false) String city) {
        List<PollenResponse> responses = pollenService.getPollenDataByCityName(city);
        return ResponseEntity.ok(responses);
    }
}
