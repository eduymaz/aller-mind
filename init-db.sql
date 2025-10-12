-- AllerMind Database Initialization Script
-- Bu script PostgreSQL container ilk kez başlatıldığında çalışır
-- Veritabanı: allermind

\echo '🚀 AllerMind veritabanı başlatılıyor...'

-- Create schemas for microservices
\echo '📦 Şemalar oluşturuluyor...'
CREATE SCHEMA IF NOT EXISTS WEATHER;
CREATE SCHEMA IF NOT EXISTS POLLEN;

\echo '🔑 İzinler veriliyor...'
-- Grant permissions on schemas
GRANT ALL PRIVILEGES ON SCHEMA WEATHER TO postgres;
GRANT ALL PRIVILEGES ON SCHEMA POLLEN TO postgres;

-- Grant permissions on future tables in schemas
GRANT ALL ON ALL TABLES IN SCHEMA WEATHER TO postgres;
GRANT ALL ON ALL TABLES IN SCHEMA POLLEN TO postgres;
GRANT ALL ON ALL SEQUENCES IN SCHEMA WEATHER TO postgres;
GRANT ALL ON ALL SEQUENCES IN SCHEMA POLLEN TO postgres;

-- Grant default privileges for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA WEATHER GRANT ALL ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA WEATHER GRANT ALL ON SEQUENCES TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA POLLEN GRANT ALL ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA POLLEN GRANT ALL ON SEQUENCES TO postgres;

-- Set search path
ALTER DATABASE allermind SET search_path TO public, weather, pollen;

\echo '✅ AllerMind veritabanı başarıyla hazırlandı!'
\echo '📊 Mevcut şemalar:'
\dn+