import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL bağlantı bilgilerin
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "ALLERMIND"
DB_USER = "postgres"
DB_PASSWORD = "123456"
SCHEMA_NAME = "POLLEN"

# CSV dosyanın yolu
csv_file = "/Users/elifdy/Desktop/allermind/aller-mind/allermind-pollen/city.csv"

# Pandas ile CSV oku
df = pd.read_csv(csv_file)

# SQLAlchemy engine oluştur
engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

df.to_sql(
    name="city",       # PostgreSQL'deki tablo adı
    con=engine,
    schema=SCHEMA_NAME,       # Şemanı belirtiyorsun
    if_exists="append",       # tablo varsa verileri ekler, yoksa oluşturur
    index=False
)

print("CSV başarıyla PostgreSQL'e aktarıldı ✅")
