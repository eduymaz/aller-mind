-- AllerMind Database Initialization Script
-- Bu script PostgreSQL container ilk kez başlatıldığında çalışır
-- Veritabanı: allermind

\echo '🚀 AllerMind veritabanı başlatılıyor...'

-- Create schemas for microservices
\echo '📦 Şemalar oluşturuluyor...'
CREATE SCHEMA IF NOT EXISTS "WEATHER";
CREATE SCHEMA IF NOT EXISTS "POLLEN";
CREATE SCHEMA IF NOT EXISTS "USER";

\echo '🔑 İzinler veriliyor...'
-- Grant permissions on schemas
GRANT ALL PRIVILEGES ON SCHEMA "WEATHER" TO postgres;
GRANT ALL PRIVILEGES ON SCHEMA "POLLEN" TO postgres;
GRANT ALL PRIVILEGES ON SCHEMA "USER" TO postgres;

-- Grant permissions on future tables in schemas
GRANT ALL ON ALL TABLES IN SCHEMA "WEATHER" TO postgres;
GRANT ALL ON ALL TABLES IN SCHEMA "POLLEN" TO postgres;
GRANT ALL ON ALL TABLES IN SCHEMA "USER" TO postgres;
GRANT ALL ON ALL SEQUENCES IN SCHEMA "WEATHER" TO postgres;
GRANT ALL ON ALL SEQUENCES IN SCHEMA "POLLEN" TO postgres;
GRANT ALL ON ALL SEQUENCES IN SCHEMA "USER" TO postgres;

-- Grant default privileges for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA "WEATHER" GRANT ALL ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA "WEATHER" GRANT ALL ON SEQUENCES TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA "POLLEN" GRANT ALL ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA "POLLEN" GRANT ALL ON SEQUENCES TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA "USER" GRANT ALL ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA "USER" GRANT ALL ON SEQUENCES TO postgres;

-- Set search path
ALTER DATABASE allermind SET search_path TO public, "WEATHER", "POLLEN", "USER";

\echo '🏙️ City tablosu oluşturuluyor...'
-- Create city table in both schemas
CREATE TABLE IF NOT EXISTS "WEATHER".city (
    plaka integer NOT NULL,
    il_adi varchar(255) NOT NULL,
    lat varchar(255) NOT NULL,
    lon varchar(255) NOT NULL,
    northeast_lat float4,
    northeast_lon float4,
    southwest_lat float4,
    southwest_lon float4,
    PRIMARY KEY (plaka)
);

CREATE TABLE IF NOT EXISTS "POLLEN".city (
    plaka integer NOT NULL,
    il_adi varchar(255) NOT NULL,
    lat varchar(255) NOT NULL,
    lon varchar(255) NOT NULL,
    northeast_lat float4,
    northeast_lon float4,
    southwest_lat float4,
    southwest_lon float4,
    PRIMARY KEY (plaka)
);

\echo '📊 City verileri yükleniyor...'
-- Import city data from CSV into both schemas
COPY "WEATHER".city (plaka, il_adi, lat, lon, northeast_lat, northeast_lon, southwest_lat, southwest_lon)
FROM '/docker-entrypoint-initdb.d/city.csv'
WITH CSV HEADER DELIMITER ',';

COPY "POLLEN".city (plaka, il_adi, lat, lon, northeast_lat, northeast_lon, southwest_lat, southwest_lon)
FROM '/docker-entrypoint-initdb.d/city.csv'
WITH CSV HEADER DELIMITER ',';

\echo '✅ AllerMind veritabanı başarıyla hazırlandı!'
\echo '📊 Mevcut şemalar:'
\dn+