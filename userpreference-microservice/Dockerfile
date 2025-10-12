FROM openjdk:21-jdk-slim

LABEL maintainer="AllerMind Team"
LABEL description="AllerMind User Preference Microservice"

WORKDIR /app

# Install curl for health checks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy the jar file
COPY target/*.jar app.jar

# Create data directory for H2 database
RUN mkdir -p /app/data

# Expose the port
EXPOSE 9191

# Environment variables
ENV JAVA_OPTS="-Xmx512m -Xms256m"
ENV SPRING_PROFILES_ACTIVE="docker"

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:9191/actuator/health || exit 1

# Run the application
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar /app/app.jar"]