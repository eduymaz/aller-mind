"""
AllerMind Kullanıcı Tercihleri ve Grup Belirleme Sistemi
Immunolojik prensiplere dayalı hiyerarşik karar ağacı ile grup sınıflandırması

"""

import json
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass


# Alerji grupları sabit tanımları
ALLERGY_GROUPS = {
    1: {
        'id': 1,
        'name': 'Şiddetli Alerjik Grup',
        'description': 'IgE > 1000 IU/mL, Anaphylaxis riski yüksek',
        'immunologic_profile': {
            'ige_level': 'very_high',  # >1000 IU/mL
            'th2_activation': 'maximal',
            'mast_cell_degranulation': 'rapid_widespread',
            'cytokine_profile': ['IL-4', 'IL-5', 'IL-13']
        },
        'weight': 0.18
    },
    2: {
        'id': 2,
        'name': 'Hafif-Orta Alerjik Grup',
        'description': 'IgE 200-1000 IU/mL, Kontrol edilebilir belirtiler',
        'immunologic_profile': {
            'ige_level': 'moderate_high',  # 200-1000 IU/mL
            'inflammatory_response': 'local',
            'antihistamine_response': 'good',
            'seasonal_pattern': 'rhinitis'
        },
        'weight': 0.22
    },
    3: {
        'id': 3,
        'name': 'Genetik Yatkınlık Grubu',
        'description': 'Atopik yapı, ailesel yüklenme',
        'immunologic_profile': {
            'atopic_structure': True,
            'family_loading': True,
            'ige_production_capacity': 'increased',
            'th1_th2_imbalance': True,
            'sensitization_risk': 'high'
        },
        'weight': 0.24
    },
    4: {
        'id': 4,
        'name': 'Teşhis Almamış Grup',
        'description': 'Normal/sınırda IgE, belirsiz sensibilizasyon',
        'immunologic_profile': {
            'ige_level': 'normal_borderline',
            'sensitization': 'unclear',
            'environmental_triggers': True,
            'inflammatory_response': 'non_specific'
        },
        'weight': 0.24
    },
    5: {
        'id': 5,
        'name': 'Hassas Çocuk/Yaşlı Grubu',
        'description': 'İmmün sistem immatüritesi/yaşlanması',
        'immunologic_profile': {
            'immune_system': 'immature_aged',
            'inflammatory_response': 'increased',
            'immune_tolerance': 'low',
            'multisystem_risk': 'high'
        },
        'weight': 0.12
    }
}


@dataclass
class UserPreferences:
    """Kullanıcı tercihleri veri yapısı"""
    # Temel Bilgiler
    age: int
    gender: str  # male, female, other
    location: Dict[str, float]  # {'latitude': float, 'longitude': float}
    
    # Klinik Geçmiş
    clinical_diagnosis: str  # none, mild_moderate_allergy, severe_allergy, asthma
    family_allergy_history: bool
    previous_allergic_reactions: Dict[str, bool]
    current_medications: List[str]
    
    # Polen Hassasiyeti Profili
    tree_pollen_allergy: Dict[str, bool]
    grass_pollen_allergy: Dict[str, bool] 
    weed_pollen_allergy: Dict[str, bool]
    
    # Besin Alerjisi ve Çapraz Reaksiyonlar
    food_allergies: Dict[str, bool]
    
    # Çevresel Hassasiyetler
    environmental_triggers: Dict[str, bool]


class AllergyGroupClassifier:
    """
    İmmunolojik prensiplere dayalı alerji grubu sınıflandırıcı
    Hiyerarşik karar ağacı kullanarak grup belirleme
    """
    
    def __init__(self):
        self.pollen_risk_weights = {
            # Ağaç poleni hassasiyeti
            'tree': {
                'birch': 0.9,      # Düşük-orta risk
                'olive': 0.5,      # En düşük alerjenik potansiyel
                'pine': 0.6,       # Düşük risk
                'oak': 0.8,        # Orta risk
                'cedar': 0.7       # Orta-düşük risk
            },
            # Çim poleni hassasiyeti
            'grass': {
                'graminales': 1.0  # Çim poleni ana risk faktörü
            },
            # Yabani ot hassasiyeti
            'weed': {
                'ragweed': 1.3,    # En yüksek alerjenik potansiyel
                'mugwort': 1.1,    # Yüksek alerjenik potansiyel
                'plantain': 1.0,   # Orta risk
                'nettle': 0.9      # Orta-düşük risk
            }
        }
        
        self.cross_reactivity_matrix = {
            # Çapraz reaksiyon riski matrisi
            'birch': ['apple', 'cherry', 'pear', 'almond'],
            'ragweed': ['melon', 'banana', 'cucumber'],
            'mugwort': ['celery', 'spices', 'herbs']
        }
    
    def determine_allergy_group(self, preferences: UserPreferences) -> Dict[str, Any]:
        """
        Ana grup belirleme algoritması
        İmmunolojik karar matrisi kullanarak grup ataması
        """
        
        # 1. Ana yaş değerlendirmesi
        age = preferences.age
        vulnerable_population = self._assess_age_vulnerability(age)
        
        # 2. Klinik durum değerlendirmesi
        clinical_group = self._assess_clinical_status(preferences.clinical_diagnosis)
        if clinical_group:
            return self._create_group_result(
                clinical_group, 
                preferences, 
                "Klinik tanı temelinde"
            )
        
        # 3. Polen hassasiyeti değerlendirmesi
        pollen_risk_score = self._calculate_pollen_risk_score(preferences)
        
        # 4. Genetik predispozisyon
        family_history = preferences.family_allergy_history
        
        # Karar matrisi
        if family_history and pollen_risk_score > 0.6:
            return self._create_group_result(
                3, 
                preferences, 
                f"Genetik yatkınlık + yüksek polen riski ({pollen_risk_score:.2f})"
            )
        
        # Hassas populasyon kontrolü
        if vulnerable_population:
            return self._create_group_result(
                5, 
                preferences, 
                f"Yaş tabanlı vulnerabilite ({age} yaş)"
            )
        
        # Varsayılan grup (teşhis almamış)
        return self._create_group_result(
            4, 
            preferences, 
            f"Teşhis almamış, polen riski: {pollen_risk_score:.2f}"
        )
    
    def _assess_age_vulnerability(self, age: int) -> bool:
        """Yaş tabanlı vulnerabilite değerlendirmesi"""
        return age <= 12 or age >= 65
    
    def _assess_clinical_status(self, clinical_diagnosis: str) -> Optional[int]:
        """Klinik durum değerlendirmesi"""
        if clinical_diagnosis == 'severe_allergy':
            return 1  # Şiddetli Alerjik Grup
        elif clinical_diagnosis == 'mild_moderate_allergy':
            return 2  # Hafif-Orta Alerjik Grup
        return None
    
    def _calculate_pollen_risk_score(self, preferences: UserPreferences) -> float:
        """
        Polen hassasiyeti risk skorunu hesapla
        İmmunolojik çapraz reaksiyon riskini dahil et
        """
        risk_score = 0.0
        
        # Ağaç poleni hassasiyeti
        for tree, sensitivity in preferences.tree_pollen_allergy.items():
            if sensitivity and tree in self.pollen_risk_weights['tree']:
                risk_score += self.pollen_risk_weights['tree'][tree] * 0.3
        
        # Çim poleni hassasiyeti  
        for grass, sensitivity in preferences.grass_pollen_allergy.items():
            if sensitivity and grass in self.pollen_risk_weights['grass']:
                risk_score += self.pollen_risk_weights['grass'][grass] * 0.4
        
        # Yabani ot hassasiyeti
        for weed, sensitivity in preferences.weed_pollen_allergy.items():
            if sensitivity and weed in self.pollen_risk_weights['weed']:
                risk_score += self.pollen_risk_weights['weed'][weed] * 0.4
        
        # Çapraz reaksiyon riski eklenmesi
        cross_reaction_bonus = self._calculate_cross_reactivity_risk(preferences)
        risk_score += cross_reaction_bonus
        
        return min(risk_score, 1.0)  # 0-1 arası normalize
    
    def _calculate_cross_reactivity_risk(self, preferences: UserPreferences) -> float:
        """Çapraz reaksiyon riskini hesapla"""
        cross_risk = 0.0
        
        # Polen-besin çapraz reaksiyonu kontrolü
        for pollen_type, related_foods in self.cross_reactivity_matrix.items():
            pollen_sensitive = False
            
            # Polen hassasiyeti kontrolü
            for category in ['tree_pollen_allergy', 'weed_pollen_allergy']:
                pollen_dict = getattr(preferences, category, {})
                if pollen_dict.get(pollen_type, False):
                    pollen_sensitive = True
                    break
            
            # İlgili besine hassasiyet kontrolü
            if pollen_sensitive:
                for food in related_foods:
                    if preferences.food_allergies.get(food, False):
                        cross_risk += 0.2  # Çapraz reaksiyon riski
        
        return min(cross_risk, 0.5)  # Maksimum %50 bonus risk
    
    def _create_group_result(self, group_id: int, preferences: UserPreferences, reason: str) -> Dict[str, Any]:
        """Grup sonucu oluştur ve kişisel risk faktörleri ekle"""
        
        # Grup bilgilerini al
        group_info = ALLERGY_GROUPS[group_id]
        
        # Kişisel risk modifikasyonları
        personal_modifiers = self._calculate_personal_modifiers(preferences, group_id)
        
        return {
            'group_id': group_id,
            'group_name': group_info['name'],
            'group_description': group_info['description'],
            'assignment_reason': reason,
            'model_weight': group_info['weight'],
            'personal_risk_modifiers': personal_modifiers,
            'immunologic_profile': group_info['immunologic_profile'],
            'environmental_sensitivity_factors': self._get_environmental_factors(preferences),
            'pollen_specific_risks': self._get_pollen_specific_risks(preferences),
            'recommendation_adjustments': self._get_recommendation_adjustments(preferences, group_id)
        }
    
    def _calculate_personal_modifiers(self, preferences: UserPreferences, group_id: int) -> Dict[str, float]:
        """Kişisel risk modifikasyonlarını hesapla"""
        modifiers = {
            'base_sensitivity': 1.0,
            'environmental_amplifier': 1.0,
            'seasonal_modifier': 1.0,
            'comorbidity_factor': 1.0
        }
        
        # Yaş tabanlı modifikasyon
        if preferences.age <= 12:
            modifiers['base_sensitivity'] = 1.3  # Çocuklar için artırılmış hassasiyet
        elif preferences.age >= 65:
            modifiers['base_sensitivity'] = 1.2  # Yaşlılar için artırılmış hassasiyet
        
        # Çevresel tetikleyici faktörleri
        environmental_triggers_count = sum(preferences.environmental_triggers.values())
        modifiers['environmental_amplifier'] = 1.0 + (environmental_triggers_count * 0.1)
        
        # Astım komorbidite faktörü
        if 'asthma' in preferences.current_medications:
            modifiers['comorbidity_factor'] = 1.4
        elif 'bronchodilator' in preferences.current_medications:
            modifiers['comorbidity_factor'] = 1.2
        
        # Grup spesifik modifikasyonlar
        if group_id == 1:  # Şiddetli alerjik grup
            modifiers['seasonal_modifier'] = 1.5  # Mevsimsel yoğunlaşma
        elif group_id == 2:  # Hafif-orta grup
            modifiers['seasonal_modifier'] = 1.2
        elif group_id == 5:  # Hassas grup
            modifiers['environmental_amplifier'] *= 1.3
        
        return modifiers
    
    def _get_environmental_factors(self, preferences: UserPreferences) -> Dict[str, bool]:
        """Çevresel hassasiyet faktörlerini döndür"""
        return {
            'dust_mite_sensitivity': preferences.environmental_triggers.get('dust_mites', False),
            'pet_dander_sensitivity': preferences.environmental_triggers.get('pet_dander', False),
            'mold_sensitivity': preferences.environmental_triggers.get('mold', False),
            'air_pollution_sensitivity': preferences.environmental_triggers.get('air_pollution', False),
            'smoke_sensitivity': preferences.environmental_triggers.get('smoke', False)
        }
    
    def _get_pollen_specific_risks(self, preferences: UserPreferences) -> Dict[str, List[str]]:
        """Polen özel risklerini belirle"""
        risks = {
            'high_risk_pollens': [],
            'moderate_risk_pollens': [],
            'cross_reactive_foods': []
        }
        
        # Yüksek risk pollenleri
        for category, pollens in [
            ('tree_pollen_allergy', preferences.tree_pollen_allergy),
            ('grass_pollen_allergy', preferences.grass_pollen_allergy),
            ('weed_pollen_allergy', preferences.weed_pollen_allergy)
        ]:
            for pollen, sensitive in pollens.items():
                if sensitive:
                    # Risk seviyesini belirle
                    risk_level = self._get_pollen_risk_level(pollen)
                    if risk_level == 'high':
                        risks['high_risk_pollens'].append(pollen)
                    elif risk_level == 'moderate':
                        risks['moderate_risk_pollens'].append(pollen)
                    
                    # Çapraz reaktif besinler
                    if pollen in self.cross_reactivity_matrix:
                        risks['cross_reactive_foods'].extend(
                            self.cross_reactivity_matrix[pollen]
                        )
        
        return risks
    
    def _get_pollen_risk_level(self, pollen: str) -> str:
        """Polen risk seviyesini belirle"""
        all_weights = {}
        all_weights.update(self.pollen_risk_weights['tree'])
        all_weights.update(self.pollen_risk_weights['grass'])
        all_weights.update(self.pollen_risk_weights['weed'])
        
        weight = all_weights.get(pollen, 0.5)
        
        if weight >= 1.1:
            return 'high'
        elif weight >= 0.8:
            return 'moderate'
        else:
            return 'low'
    
    def _get_recommendation_adjustments(self, preferences: UserPreferences, group_id: int) -> Dict[str, Any]:
        """Grup ve kişisel özelliklere göre öneri ayarlamaları"""
        adjustments = {
            'medication_priority': 'standard',
            'environmental_control_level': 'standard',
            'monitoring_frequency': 'standard',
            'emergency_preparedness': False
        }
        
        if group_id == 1:  # Şiddetli alerjik grup
            adjustments.update({
                'medication_priority': 'high',
                'environmental_control_level': 'strict',
                'monitoring_frequency': 'daily',
                'emergency_preparedness': True
            })
        elif group_id == 2:  # Hafif-orta grup
            adjustments.update({
                'medication_priority': 'moderate',
                'environmental_control_level': 'moderate',
                'monitoring_frequency': 'weekly'
            })
        elif group_id == 5:  # Hassas grup
            adjustments.update({
                'medication_priority': 'high',
                'environmental_control_level': 'strict',
                'monitoring_frequency': 'daily'
            })
        
        # Kişisel modifikasyonlar
        if preferences.previous_allergic_reactions.get('anaphylaxis', False):
            adjustments['emergency_preparedness'] = True
            adjustments['medication_priority'] = 'critical'
        
        return adjustments


def create_sample_user_preferences() -> UserPreferences:
    """Test için örnek kullanıcı tercihleri"""
    return UserPreferences(
        age=28,
        gender='female',
        location={'latitude': 41.0082, 'longitude': 28.9784},  # Istanbul
        clinical_diagnosis='mild_moderate_allergy',
        family_allergy_history=True,
        previous_allergic_reactions={
            'anaphylaxis': False,
            'severe_asthma': False,
            'hospitalization': False
        },
        current_medications=['antihistamine', 'nasal_spray'],
        tree_pollen_allergy={
            'birch': True,
            'olive': False,
            'pine': False
        },
        grass_pollen_allergy={
            'graminales': True
        },
        weed_pollen_allergy={
            'ragweed': True,
            'mugwort': False
        },
        food_allergies={
            'apple': True,  # Birch çapraz reaksiyonu
            'nuts': False,
            'shellfish': False
        },
        environmental_triggers={
            'dust_mites': True,
            'pet_dander': False,
            'mold': True,
            'air_pollution': True,
            'smoke': True
        }
    )


if __name__ == "__main__":
    # Test sistemi
    classifier = AllergyGroupClassifier()
    sample_user = create_sample_user_preferences()
    
    result = classifier.determine_allergy_group(sample_user)
    
    print("=== ALLERMİND GRUP SINIFLANDIRMA SONUCU ===")
    print(f"Grup: {result['group_name']} (ID: {result['group_id']})")
    print(f"Açıklama: {result['group_description']}")
    print(f"Atama Nedeni: {result['assignment_reason']}")
    print(f"Model Ağırlığı: {result['model_weight']}")
    print("\nKişisel Risk Modifikasyonları:")
    for key, value in result['personal_risk_modifiers'].items():
        print(f"  {key}: {value}")
    
    print("\nPolen Spesifik Riskler:")
    for key, value in result['pollen_specific_risks'].items():
        print(f"  {key}: {value}")
    
    print(f"\nJSON formatında:\n{json.dumps(result, indent=2, ensure_ascii=False)}")