# Stage 1: Build Flutter Web App
FROM ghcr.io/cirruslabs/flutter:stable AS build

# Set working directory
WORKDIR /app

# Copy pubspec files first (as root)
COPY pubspec.yaml pubspec.lock* ./

# Get dependencies (as root - Flutter SDK needs root for first run)
RUN flutter pub get

# Copy the rest of the application
COPY . .

# Build for web with release mode
RUN flutter build web --release

# Stage 2: Serve with Nginx
FROM nginx:alpine

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy built web app from build stage
COPY --from=build /app/build/web /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
