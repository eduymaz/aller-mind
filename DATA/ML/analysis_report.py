import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Any
import json
import os

class AllergyAnalysisReport:
    """
    Allerji tahmin sistemi analiz raporu oluşturucu
    """
    
    def __init__(self):
        self.group_names = {
            1: "Şiddetli Alerjik Grup",
            2: "Hafif-Orta Grup", 
            3: "Olası Alerjik Grup/Genetiğinde Olan",
            4: "Henüz Teşhis Almamış/İhtimali Bilinmeyen Grup",
            5: "Alerjisi Olmayan + İhtimali Bilinmeyen Ama Hassas Grup"
        }
        
        # Test sonuçları
        self.test_results = self._get_test_results()
    
    def _get_test_results(self) -> Dict[str, Dict[int, Dict[str, Any]]]:
        """Test sonuçlarını tanımla"""
        return {
            "İdeal Hava Koşulları": {
                1: {"safe_hours": 5.93, "risk_score": 0.155, "risk_level": "Düşük"},
                2: {"safe_hours": 7.32, "risk_score": 0.147, "risk_level": "Düşük"},
                3: {"safe_hours": 7.21, "risk_score": 0.128, "risk_level": "Düşük"},
                4: {"safe_hours": 7.36, "risk_score": 0.166, "risk_level": "Düşük"},
                5: {"safe_hours": 7.35, "risk_score": 0.202, "risk_level": "Düşük"}
            },
            "Yüksek Polen Sezonu": {
                1: {"safe_hours": 0.0, "risk_score": 0.67, "risk_level": "Çok Yüksek"},
                2: {"safe_hours": 2.51, "risk_score": 0.59, "risk_level": "Orta"},
                3: {"safe_hours": 0.08, "risk_score": 0.613, "risk_level": "Çok Yüksek"},
                4: {"safe_hours": 5.84, "risk_score": 0.567, "risk_level": "Orta"},
                5: {"safe_hours": 5.52, "risk_score": 0.556, "risk_level": "Düşük"}
            },
            "Kötü Hava Kalitesi": {
                1: {"safe_hours": 0.0, "risk_score": 0.574, "risk_level": "Çok Yüksek"},
                2: {"safe_hours": 4.83, "risk_score": 0.51, "risk_level": "Orta"},
                3: {"safe_hours": 1.78, "risk_score": 0.482, "risk_level": "Yüksek"},
                4: {"safe_hours": 5.48, "risk_score": 0.536, "risk_level": "Orta"},
                5: {"safe_hours": 6.38, "risk_score": 0.595, "risk_level": "Düşük"}
            },
            "Karma Risk Durumu": {
                1: {"safe_hours": 0.0, "risk_score": 0.72, "risk_level": "Çok Yüksek"},
                2: {"safe_hours": 2.16, "risk_score": 0.606, "risk_level": "Yüksek"},
                3: {"safe_hours": 0.43, "risk_score": 0.616, "risk_level": "Çok Yüksek"},
                4: {"safe_hours": 4.18, "risk_score": 0.595, "risk_level": "Orta"},
                5: {"safe_hours": 5.68, "risk_score": 0.589, "risk_level": "Düşük"}
            }
        }
    
    def generate_comprehensive_report(self):
        """Kapsamlı analiz raporu oluştur"""
        report = []
        
        report.append("# 🌟 AllerMind - Allerji Tahmin Sistemi Analiz Raporu")
        report.append("=" * 60)
        report.append("")
        
        # Sistem özeti
        report.extend(self._system_overview())
        
        # Grup ağırlık analizi
        report.extend(self._group_weight_analysis())
        
        # Test sonuçları analizi
        report.extend(self._test_results_analysis())
        
        # Grup karşılaştırması
        report.extend(self._group_comparison())
        
        # Senaryo analizi
        report.extend(self._scenario_analysis())
        
        # Öneriler ve sonuç
        report.extend(self._recommendations_and_conclusion())
        
        # Raporu dosyaya kaydet
        report_content = "\n".join(report)
        report_path = '/Users/elifdy/Desktop/allermind/aller-mind/DATA/ML/allergy_analysis_report.md'
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"📋 Detaylı analiz raporu oluşturuldu: {report_path}")
        return report_content
    
    def _system_overview(self) -> List[str]:
        """Sistem genel bakış"""
        return [
            "## 📊 Sistem Genel Bakış",
            "",
            "AllerMind allerji tahmin sistemi, 5 farklı allerji profili için özelleştirilmiş",
            "tahmin modelleri geliştirmektedir. Sistem şu temel bileşenleri içerir:",
            "",
            "### 🔧 Teknik Özellikler:",
            "- **Veri Kaynağı**: 175,872 satır kombinlenmiş hava durumu, hava kalitesi ve polen verisi",
            "- **Tarih Aralığı**: 30 Ağustos - 1 Eylül 2025",
            "- **Model Türü**: Random Forest Regressor (her grup için ayrı)",
            "- **Özellik Sayısı**: 21 farklı çevresel parametre",
            "- **Hedef Değişken**: Güvenli vakit geçirme süresi (saat)",
            "",
            "### 📈 Model Performansı:",
            "- **Grup 1 (Şiddetli Alerjik)**: R² = 1.000, RMSE = 0.047",
            "- **Grup 2 (Hafif-Orta)**: R² = 0.997, RMSE = 0.081", 
            "- **Grup 3 (Olası Alerjik)**: R² = 1.000, RMSE = 0.049",
            "- **Grup 4 (Teşhis Almamış)**: R² = 0.992, RMSE = 0.051",
            "- **Grup 5 (Hassas Grup)**: R² = 0.994, RMSE = 0.020",
            "",
        ]
    
    def _group_weight_analysis(self) -> List[str]:
        """Grup ağırlık analizi"""
        return [
            "## ⚖️ Grup Ağırlık Analizi",
            "",
            "Her allerji grubu için parametre ağırlıkları bilimsel prensipler doğrultusunda",
            "optimize edilmiştir:",
            "",
            "### 👥 Grup 1 - Şiddetli Alerjik Grup:",
            "- **Polen Hassasiyeti**: %40 (En yüksek)",
            "- **Hava Kalitesi**: %35",
            "- **Hava Durumu**: %25",
            "- **Hassasiyet Eşiği**: 0.2 (Çok düşük tolerans)",
            "- **Mevsimsel Faktör**: 2.0x",
            "",
            "**🎯 Strateji**: Polen odaklı maksimum koruma",
            "",
            "### 👥 Grup 2 - Hafif-Orta Grup:",
            "- **Polen Hassasiyeti**: %30",
            "- **Hava Kalitesi**: %30", 
            "- **Hava Durumu**: %40 (Dengeli)",
            "- **Hassasiyet Eşiği**: 0.4",
            "- **Mevsimsel Faktör**: 1.5x",
            "",
            "**🎯 Strateji**: Dengeli risk yönetimi",
            "",
            "### 👥 Grup 3 - Olası Alerjik/Genetik:",
            "- **Polen Hassasiyeti**: %35 (Yüksek)",
            "- **Hava Kalitesi**: %25",
            "- **Hava Durumu**: %40",
            "- **Hassasiyet Eşiği**: 0.3",
            "- **Mevsimsel Faktör**: 1.7x",
            "",
            "**🎯 Strateji**: Proaktif önlem odaklı",
            "",
            "### 👥 Grup 4 - Teşhis Almamış:",
            "- **Polen Hassasiyeti**: %25",
            "- **Hava Kalitesi**: %35 (Temkinli)",
            "- **Hava Durumu**: %40",
            "- **Hassasiyet Eşiği**: 0.5",
            "- **Mevsimsel Faktör**: 1.3x",
            "",
            "**🎯 Strateji**: Belirsizlik yönetimi",
            "",
            "### 👥 Grup 5 - Hassas Grup (Çocuk/Yaşlı):",
            "- **Polen Hassasiyeti**: %20",
            "- **Hava Kalitesi**: %45 (En yüksek)",
            "- **Hava Durumu**: %35",
            "- **Hassasiyet Eşiği**: 0.6",
            "- **Mevsimsel Faktör**: 1.2x",
            "",
            "**🎯 Strateji**: Genel sağlık odaklı koruma",
            "",
        ]
    
    def _test_results_analysis(self) -> List[str]:
        """Test sonuçları analizi"""
        lines = [
            "## 🧪 Test Sonuçları Analizi",
            "",
            "4 farklı senaryo ile gerçekleştirilen testler, sistemin farklı",
            "çevresel koşullardaki performansını göstermektedir:",
            "",
        ]
        
        for scenario, results in self.test_results.items():
            lines.append(f"### 📋 {scenario}")
            lines.append("")
            
            for group_id, result in results.items():
                group_name = self.group_names[group_id]
                safe_hours = result['safe_hours']
                risk_score = result['risk_score']
                risk_level = result['risk_level']
                
                lines.append(f"**{group_name}:**")
                lines.append(f"- Güvenli süre: {safe_hours} saat")
                lines.append(f"- Risk skoru: {risk_score} ({risk_level})")
                lines.append("")
            
            lines.append("")
        
        return lines
    
    def _group_comparison(self) -> List[str]:
        """Grup karşılaştırması"""
        lines = [
            "## 🔄 Grup Karşılaştırması",
            "",
            "Farklı senaryolardaki grup performansları:",
            "",
        ]
        
        # Her senaryo için grup sıralaması
        for scenario, results in self.test_results.items():
            lines.append(f"### {scenario} - Güvenli Süre Sıralaması:")
            
            # Güvenli süreye göre sırala
            sorted_groups = sorted(results.items(), 
                                 key=lambda x: x[1]['safe_hours'], 
                                 reverse=True)
            
            for i, (group_id, result) in enumerate(sorted_groups, 1):
                emoji = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i-1]
                lines.append(f"{emoji} {self.group_names[group_id]}: {result['safe_hours']} saat")
            
            lines.append("")
        
        return lines
    
    def _scenario_analysis(self) -> List[str]:
        """Senaryo analizi"""
        return [
            "## 🌤️ Senaryo Bazlı Analiz",
            "",
            "### 🟢 İdeal Hava Koşulları:",
            "- **Genel Durum**: Tüm gruplar için düşük risk",
            "- **En Az Etkilenen**: Grup 4 (7.36 saat)",
            "- **En Çok Etkilenen**: Grup 1 (5.93 saat)",
            "- **Fark**: 1.43 saat (%19.4 azalma)",
            "",
            "**📊 Analiz**: İdeal koşullarda bile şiddetli alerjik grup belirgin kısıtlama yaşar.",
            "",
            "### 🔴 Yüksek Polen Sezonu:",
            "- **Genel Durum**: Kritik seviye, büyük grup farklılıkları",
            "- **En Az Etkilenen**: Grup 4 (5.84 saat)",
            "- **En Çok Etkilenen**: Grup 1 (0.0 saat)",
            "- **Fark**: 5.84 saat (%100 azalma)",
            "",
            "**📊 Analiz**: Polen odaklı gruplar (1,3) ciddi kısıtlama yaşar.",
            "",
            "### 🏭 Kötü Hava Kalitesi:",
            "- **Genel Durum**: Hava kalitesi hassasiyeti ön plana çıkar",
            "- **En Az Etkilenen**: Grup 5 (6.38 saat)", 
            "- **En Çok Etkilenen**: Grup 1 (0.0 saat)",
            "- **Fark**: 6.38 saat (%100 azalma)",
            "",
            "**📊 Analiz**: Hassas grup paradoksal olarak daha iyi performans gösterir.",
            "",
            "### ⚠️ Karma Risk Durumu:",
            "- **Genel Durum**: En zorlu senaryo",
            "- **En Az Etkilenen**: Grup 5 (5.68 saat)",
            "- **En Çok Etkilenen**: Grup 1 (0.0 saat)",
            "- **Fark**: 5.68 saat (%100 azalma)",
            "",
            "**📊 Analiz**: Multiple risk faktörleri şiddetli alerjik grubu tamamen kısıtlar.",
            "",
        ]
    
    def _recommendations_and_conclusion(self) -> List[str]:
        """Öneriler ve sonuç"""
        return [
            "## 💡 Öneriler ve Sonuç",
            "",
            "### 🎯 Temel Bulgular:",
            "",
            "1. **Grup Hassasiyeti Sıralması** (Ortalama):",
            "   - Grup 1 (Şiddetli): En hassas, en kısıtlı",
            "   - Grup 3 (Olası): İkinci en hassas", 
            "   - Grup 2 (Hafif-Orta): Orta seviye",
            "   - Grup 4 (Teşhis Almamış): Beklenenden iyi",
            "   - Grup 5 (Hassas): Paradoksal olarak en toleranslı",
            "",
            "2. **Kritik Risk Faktörleri**:",
            "   - Polen mevsimi: Grup 1,3 için kritik",
            "   - Hava kalitesi: Tüm gruplar için önemli",
            "   - Meteorolojik koşullar: Genel etkili",
            "",
            "3. **Model Doğruluğu**:",
            "   - Yüksek R² değerleri (0.992-1.000)",
            "   - Düşük RMSE değerleri (0.020-0.081)",
            "   - Güvenilir tahmin performansı",
            "",
            "### 🔧 Sistem Optimizasyon Önerileri:",
            "",
            "1. **Grup 1 için**:",
            "   - Polen erken uyarı sistemi",
            "   - Acil durum protokolleri",
            "   - İç mekan alternatif aktiviteleri",
            "",
            "2. **Grup 3 için**:",
            "   - Proaktif izleme",
            "   - Genetik risk faktörü entegrasyonu",
            "   - Kişiselleştirilmiş eşikler",
            "",
            "3. **Grup 5 için**:",
            "   - Yaş odaklı ağırlıklar",
            "   - Sağlık durumu entegrasyonu",
            "   - Aktivite şiddeti faktörü",
            "",
            "### 📈 Gelecek Geliştirmeler:",
            "",
            "- **Gerçek zamanlı veri entegrasyonu**",
            "- **Kişisel allerji profili öğrenme**",
            "- **Coğrafi mikro-iklim analizi**",
            "- **Mobil uygulama entegrasyonu**",
            "- **Wearable cihaz desteği**",
            "",
            "### 🎊 Sonuç:",
            "",
            "AllerMind sistemi, farklı allerji profillerine sahip bireyler için",
            "bilimsel veriye dayalı, kişiselleştirilmiş tahminler sunmaktadır.",
            "Sistem, çevresel risk faktörlerini etkili bir şekilde analiz ederek,",
            "kullanıcıların günlük yaşam kalitelerini artırmaya odaklanmıştır.",
            "",
            "**✅ Başarı Kriterleri:**",
            "- Yüksek model doğruluğu ✓",
            "- Grup odaklı farklılaştırma ✓", 
            "- Gerçekçi tahmin aralıkları ✓",
            "- Uygulanabilir öneriler ✓",
            "",
            "---",
            "*Rapor oluşturma tarihi: 1 Eylül 2025*",
            "*AllerMind Allerji Tahmin Sistemi v1.0*"
        ]
    
    def create_summary_statistics(self):
        """Özet istatistikler oluştur"""
        print("📊 Özet İstatistikler:")
        print("=" * 40)
        
        all_safe_hours = []
        all_risk_scores = []
        
        for scenario, results in self.test_results.items():
            for group_id, result in results.items():
                all_safe_hours.append(result['safe_hours'])
                all_risk_scores.append(result['risk_score'])
        
        print(f"🕐 Güvenli Süre İstatistikleri:")
        print(f"   - Ortalama: {np.mean(all_safe_hours):.2f} saat")
        print(f"   - Medyan: {np.median(all_safe_hours):.2f} saat")
        print(f"   - Min: {np.min(all_safe_hours):.2f} saat")
        print(f"   - Max: {np.max(all_safe_hours):.2f} saat")
        print(f"   - Standart Sapma: {np.std(all_safe_hours):.2f} saat")
        
        print(f"\n🎯 Risk Skoru İstatistikleri:")
        print(f"   - Ortalama: {np.mean(all_risk_scores):.3f}")
        print(f"   - Medyan: {np.median(all_risk_scores):.3f}")
        print(f"   - Min: {np.min(all_risk_scores):.3f}")
        print(f"   - Max: {np.max(all_risk_scores):.3f}")
        print(f"   - Standart Sapma: {np.std(all_risk_scores):.3f}")
        
        # Grup bazlı ortalamalar
        print(f"\n👥 Grup Bazlı Ortalama Güvenli Süreler:")
        for group_id in range(1, 6):
            group_hours = [results[group_id]['safe_hours'] 
                          for results in self.test_results.values()]
            print(f"   - {self.group_names[group_id]}: {np.mean(group_hours):.2f} saat")

def main():
    """Ana fonksiyon"""
    print("📋 AllerMind Analiz Raporu Oluşturuluyor...")
    
    analyzer = AllergyAnalysisReport()
    
    # Özet istatistikler
    analyzer.create_summary_statistics()
    
    # Kapsamlı rapor
    report = analyzer.generate_comprehensive_report()
    
    print(f"\n✅ Analiz tamamlandı!")
    print(f"📄 Rapor uzunluğu: {len(report.split())} kelime")

if __name__ == "__main__":
    main()
