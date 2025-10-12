FROM openjdk:21-jdk-slim

LABEL maintainer="AllerMind Team"
LABEL description="AllerMind Weather Air Pollution Microservice"

WORKDIR /app

# Install curl for health check
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy the jar file
COPY target/*.jar app.jar

# Expose the port
EXPOSE 8383

# Environment variables
ENV JAVA_OPTS="-Xmx512m -Xms256m"
ENV SPRING_PROFILES_ACTIVE="docker"
ENV SPRING_DATASOURCE_URL="jdbc:postgresql://postgres:5432/allermind?currentSchema=WEATHER"
ENV SPRING_DATASOURCE_USERNAME="postgres"
ENV SPRING_DATASOURCE_PASSWORD="123456"

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8383/actuator/health || exit 1

# Run the application
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar /app/app.jar"]