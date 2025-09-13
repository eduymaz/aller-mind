FROM openjdk:21-jdk-slim

LABEL maintainer="AllerMind Team"
LABEL description="AllerMind Model Microservice"

WORKDIR /app

COPY target/*.jar app.jar

EXPOSE 8484

ENV JAVA_OPTS="-Xmx512m -Xms256m"
ENV POLLEN_SERVICE_BASE_URL="http://pollen-service:8282"
ENV WEATHER_SERVICE_BASE_URL="http://weather-service:8383"
ENV ML_MODEL_SERVICE_BASE_URL="http://ml-model-service:8000"

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8484/api/v1/model/health || exit 1

ENTRYPOINT ["java", "-jar", "/app/app.jar"]
