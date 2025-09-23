package com.allermind.userpreference.infrastructure.adapter.in.web;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.allermind.userpreference.application.dto.AllergyClassificationRequest;
import com.allermind.userpreference.application.dto.AllergyClassificationResponse;
import com.allermind.userpreference.application.port.in.AllergyGroupClassificationUseCase;

@RestController
@RequestMapping("/api/v1/allergy-classification")
public class AllergyClassificationController {
    
    private final AllergyGroupClassificationUseCase classificationUseCase;
    
    public AllergyClassificationController(AllergyGroupClassificationUseCase classificationUseCase) {
        this.classificationUseCase = classificationUseCase;
    }
    
    @PostMapping("/classify")
    public ResponseEntity<AllergyClassificationResponse> classifyAllergy(
            @RequestBody AllergyClassificationRequest request) {
        AllergyClassificationResponse response = classificationUseCase.classifyAllergy(request);
        return ResponseEntity.ok(response);
    }
    
    @ExceptionHandler(IllegalArgumentException.class)
    public ResponseEntity<ErrorResponse> handleValidationException(IllegalArgumentException ex) {
        ErrorResponse error = new ErrorResponse("VALIDATION_ERROR", ex.getMessage());
        return ResponseEntity.badRequest().body(error);
    }
    
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGenericException(Exception ex) {
        ErrorResponse error = new ErrorResponse("INTERNAL_ERROR", "An internal error occurred");
        return ResponseEntity.internalServerError().body(error);
    }
    
    public static class ErrorResponse {
        private final String code;
        private final String message;
        
        public ErrorResponse(String code, String message) {
            this.code = code;
            this.message = message;
        }
        
        public String getCode() {
            return code;
        }
        
        public String getMessage() {
            return message;
        }
    }
}