# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-21 AS builder

WORKDIR /build

# Copy pom.xml and download dependencies (for better caching)
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code and build
COPY src ./src
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime
FROM eclipse-temurin:21-jre-jammy

LABEL maintainer="AllerMind Team"
LABEL description="AllerMind Pollen Microservice"

WORKDIR /app

# Copy the built jar from builder stage
COPY --from=builder /build/target/*.jar app.jar

# Expose the port
EXPOSE 8282

# Environment variables (hassas veriler Render'da tanımlanacak)
ENV JAVA_OPTS="-Xmx512m -Xms256m"
ENV SPRING_PROFILES_ACTIVE="docker"

# Run the application
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar /app/app.jar"]