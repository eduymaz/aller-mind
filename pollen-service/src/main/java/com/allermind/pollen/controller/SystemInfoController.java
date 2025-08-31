package com.allermind.pollen.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/system")
public class SystemInfoController {

    @GetMapping("/info")
    public Map<String, String> getSystemInfo() {
        Map<String, String> info = new HashMap<>();
        info.put("java.version", System.getProperty("java.version"));
        info.put("java.home", System.getProperty("java.home"));
        info.put("java.vendor", System.getProperty("java.vendor"));
        info.put("os.name", System.getProperty("os.name"));
        info.put("user.dir", System.getProperty("user.dir"));
        
        // Add environment JAVA_HOME if available
        String javaHome = System.getenv("JAVA_HOME");
        if (javaHome != null) {
            info.put("env.JAVA_HOME", javaHome);
        } else {
            info.put("env.JAVA_HOME", "Not set");
        }
        
        return info;
    }
}
