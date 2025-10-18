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

# Install envsubst for environment variable substitution
RUN apk add --no-cache gettext

# Copy nginx configuration template
COPY nginx.conf /etc/nginx/nginx.conf.template

# Copy built web app from build stage
COPY --from=build /app/build/web /usr/share/nginx/html

# Copy startup script
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Cloud Run will set the PORT environment variable
# Default to 8080 for local testing
ENV PORT=8080
EXPOSE $PORT

# Use custom entrypoint
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
