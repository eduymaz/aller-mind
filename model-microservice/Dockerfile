FROM openjdk:21-jdk-slim

LABEL maintainer="AllerMind Team"
LABEL description="AllerMind Model Microservice"

WORKDIR /app

# Install curl for health check
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy the jar file
COPY target/*.jar app.jar

# Expose the port
EXPOSE 8484

# Environment variables
ENV JAVA_OPTS="-Xmx512m -Xms256m"
ENV SPRING_PROFILES_ACTIVE="docker"
ENV POLLEN_SERVICE_BASE_URL="http://pollen-service:8282"
ENV WEATHER_SERVICE_BASE_URL="http://weather-service:8383"
ENV ML_MODEL_SERVICE_BASE_URL="http://ml-model-service:8000"
ENV USER_PREFERENCE_SERVICE_BASE_URL="http://userpreference-service:9191"

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8484/actuator/health || exit 1

# Run the application
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar /app/app.jar"]
