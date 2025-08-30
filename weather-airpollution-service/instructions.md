Postgresql 16'da çalışıyorsun. Python kullanıyorsun. Database tabloları üreteceksin; airquality-response.json  ve weather-response.json dosyalarını incele. Ve aşağıdaki gibi tablolar oluşturacaksın. .json dosyası bir http rest response'udur. Bu json'ı tabloya kaydetmek için gerekli alanları extract etmen gerekir. 

Json bilgilerinde, hourly objesi dictionary tutuyor. buradaki dictionary objelerindeki key ler liste tutuyor. bunlar arasındaki ilişki şu şekildedir: 
her key için valueların i. indexleri birbiri ile ilişkilidir. Tablolara kayıt atarken bu ilişkilere dikkat edilerek kayıt atılmalıdır.

DB bilgileri şöyle : 

DB_HOST = "localhost"  # Replace with your PostgreSQL host
DB_PORT = "5432"       # Default PostgreSQL port
DB_NAME = "ALLERMIND"  # Replace with your database name
DB_USER = "postgres"       # Replace with your username
DB_PASSWORD = "123456"   # Replace with your password
SCHEMA_NAME = "WEATHER"

DB'de city tablosu var. Bu tablonun pythondaki karşılığı entities.py altında data class olarak tanımlanmıştır.
DB'deki her city için weather ve airquality bilgileri sorgulanacak, city tablosundan lat ve lon bilgileri rest servislerindeki gerekli parametrelere beslenecek. Servislerin çağırılması için hazır yazılmış bir sınıs var (service.py), bunu kullan. servislerde gerekli olan date bilgisini, bulunduğumuz gün olarak ver. YANİ başlangıç ve bitiş tarihleri "today" için bilgi içersin. 

Yeni üretecek olduğun tablolar için yeni tablo isimlerini sen düzenle ama kolon isimlendirmeleri şu şekilde olacak : 

Tablo1 : 
lat,lon,time,temperature_2m,relative_humidity_2m,precipitation,snowfall,rain,cloud_cover,surface_pressure,wind_speed_10m,wind_direction_10m,soil_temperature_0_to_7cm,soil_moisture_0_to_7cm,sunshine_duration

Tablo2 :
lat,lon,time,pm10,pm2_5,carbon_dioxide,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone,aerosol_optical_depth,methane,uv_index,uv_index_clear_sky,dust

Tablo3 : -- bu tablo servisin sadece günde bir kere çalıştığını kontrol edecek kontrol tablosu olacaktır. İçereceği kolonlar: 
date, isprocessed

Bu tablolar sadece bir kez yaratılacak ve her uygulama çalıştırıldığında yeniden yaratılmasın. 
Her iki tablo için de lat lon ve time kolonları unique'lik sağlayacak.

Python ile kodlama tasarımları, design pattern, clean code, solıd prensipleri ve DDD yaklaşımına göre  okunabilir ve maintainable olan kod yazıyorsun. 

DB işlemlerinde entity, dao ve servis katmanları kullanılarak oluştur. 

Genel olarak yapacakların özeti : 
1. Tabloları oluşturmak 
2. DB'den city leri okuyarak her city için sorgu atıp, DB'ye uygun şekilde kaydetmek
3. Sorgu atmadan önce Tablo3'teki date bilgisini sorgulayıp "today" bilgisi ile karşılaştırıp, aynı gün içerisinde 1'den fazla çalışmasını engelleyecek kontrol mekanizması ekle.

