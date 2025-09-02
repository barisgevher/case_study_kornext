# inference_engine.py
import re
from typing import Dict, List, Tuple
from datetime import datetime, timedelta


class InferenceEngine:
    def __init__(self):
        self.inference_rules = self.load_inference_rules()

    def load_inference_rules(self) -> Dict:
        """Çıkarım kurallarının yüklenmesi"""
        return {
            'urgency_indicators': {
                'high': ['acil', 'hemen', 'derhal', 'çok önemli', 'tehlikeli'],
                'medium': ['bir an önce', 'mümkün olan', 'yakın zamanda'],
                'low': ['uygun görürseniz', 'müsait olduğunuzda']
            },
            'duration_indicators': {
                'chronic': ['aylar', 'yıllar', 'uzun süredir', 'defalarca', 'sürekli'],
                'recurring': ['her gün', 'her akşam', 'sürekli', 'tekrar tekrar'],
                'recent': ['dün', 'geçen hafta', 'kısa süre önce', 'yeni']
            },
            'impact_indicators': {
                'high': ['yaşam kalitesi', 'sağlık', 'güvenlik', 'tehlike'],
                'medium': ['rahatsızlık', 'zorluk', 'problem'],
                'low': ['küçük', 'basit', 'hafif']
            },
            'emotional_indicators': {
                'angry': ['öfke', 'sinir', 'kızgın', 'tepki'],
                'desperate': ['çare', 'yardım', 'umut', 'bitkin'],
                'disappointed': ['hayal kırıklığı', 'üzüntü', 'beklenti']
            }
        }

    def infer_problem_severity(self, text: str) -> Dict:
        """Problemin ciddiyetinin çıkarılması"""
        text_lower = text.lower()

        severity_score = 0
        reasons = []

        # Aciliyet göstergelerin derecelndirilmesi
        for level, indicators in self.inference_rules['urgency_indicators'].items():
            for indicator in indicators:
                if indicator in text_lower:
                    if level == 'high':
                        severity_score += 3
                    elif level == 'medium':
                        severity_score += 2
                    else:
                        severity_score += 1
                    reasons.append(f"'{indicator}' kelimesi {level} aciliyet gösteriyor")

        # Süre göstergelerinin kategorize edilmesi
        for duration_type, indicators in self.inference_rules['duration_indicators'].items():
            for indicator in indicators:
                if indicator in text_lower:
                    if duration_type == 'chronic':
                        severity_score += 2
                        reasons.append(f"'{indicator}' kronik problem gösteriyor")
                    elif duration_type == 'recurring':
                        severity_score += 1
                        reasons.append(f"'{indicator}' tekrarlayan problem gösteriyor")

        # Etki göstergesinin ölçülmesi
        for impact_level, indicators in self.inference_rules['impact_indicators'].items():
            for indicator in indicators:
                if indicator in text_lower:
                    if impact_level == 'high':
                        severity_score += 3
                        reasons.append(f"'{indicator}' yüksek etki gösteriyor")

        severity_level = 'low'
        if severity_score >= 6:
            severity_level = 'high'
        elif severity_score >= 3:
            severity_level = 'medium'

        return {
            'severity_level': severity_level,
            'severity_score': severity_score,
            'reasoning': reasons
        }

    def infer_citizen_profile(self, text: str) -> Dict:
        """Kişinin  profilinin  çıkarılması"""
        text_lower = text.lower()
        profile = {
            'age_group': 'unknown',
            'family_status': 'unknown',
            'social_awareness': 'medium',
            'communication_style': 'formal'
        }

        # Yaş grubunun çıkarılması
        if any(word in text_lower for word in ['emekli', 'yaşlı', 'yaşım', 'büyük']):
            profile['age_group'] = 'elderly'
        elif any(word in text_lower for word in ['öğrenci', 'genç', 'yeni']):
            profile['age_group'] = 'young'
        elif any(word in text_lower for word in ['çocuk', 'aile', 'eş']):
            profile['age_group'] = 'middle_aged'

        # Aile durumunun belirlenmesi
        if any(word in text_lower for word in ['çocuk', 'bebek', 'anne', 'baba']):
            profile['family_status'] = 'has_family'
        elif any(word in text_lower for word in ['tek', 'yalnız']):
            profile['family_status'] = 'single'

        return profile