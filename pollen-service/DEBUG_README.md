# Pollen Service Debug Kılavuzu

Bu Spring Boot projesini VS Code'da debug modunda çalıştırmak için aşağıdaki adımları izleyin:

## Gereksinimler
- Java 21
- VS Code Extension Pack for Java (zaten yüklü)
- PostgreSQL veritabanı (localhost:5432)

## Debug Yapılandırmaları

Projenizde 3 farklı debug yapılandırması tanımlanmıştır:

### 1. Spring Boot Debug
- Otomatik compile ile debug modu
- Proje başlamadan önce Maven compile çalışır

### 2. Spring Boot Debug (No Compile)
- Hızlı debug başlatma
- Compile işlemi atlanır (önceden derlenmiş olmalı)

### 3. Current File
- Açık olan Java dosyasını direkt çalıştırır
- Test sınıfları için kullanışlı

## Kullanım Adımları

1. VS Code'da projeyi açın
2. `Ctrl+Shift+D` (veya `Cmd+Shift+D` Mac'te) ile Debug panelini açın
3. Yukarıdaki yapılandırmalardan birini seçin
4. F5 tuşuna basın veya "Start Debugging" butonuna tıklayın

## Breakpoint Ekleme

1. Kod satırının sol tarafındaki gri alana tıklayın
2. Kırmızı nokta görünecek (breakpoint)
3. Debug modunda çalıştırın
4. Kod bu satıra geldiğinde duraksayacak

## Önemli Notlar

- PostgreSQL veritabanının çalışır durumda olduğundan emin olun
- İlk debug başlatma biraz zaman alabilir
- Hot swap özelliği küçük değişiklikler için çalışır, büyük yapısal değişikliklerde yeniden başlatın

## Maven Komutları (Terminal)

Alternatif olarak terminal üzerinden de çalışabilirsiniz:

```bash
# Compile
./mvnw compile

# Clean compile
./mvnw clean compile

# Run
./mvnw spring-boot:run

# Test
./mvnw test

# Package
./mvnw package
```

## Hata Giderme

Eğer debug çalışmazsa:

1. Java Extension Pack'in güncel olduğundan emin olun
2. VS Code'u yeniden başlatın
3. `Ctrl+Shift+P` > "Java: Rebuild Projects" komutunu çalıştırın
4. Terminal'de `./mvnw clean compile` komutunu çalıştırın
