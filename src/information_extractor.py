import re
from datetime import datetime
from typing import Dict, List, Optional
import json

class InformationExtractor:
    def __init__(self):
        self.patterns = self.load_patterns()

    def load_patterns(self) -> Dict:
        """Regex desenlerini yükleme"""

        patterns = {
            'name': [
                r'(?:adım|ismim|ben)\s+([A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)',
                r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)(?:\s+(?:olarak|adına))',
            ],
            'address': [
                r'(?:yaşadığım|ikamet ettiğim|oturduğum)\s+([^.]+?)(?:\s+(?:mahalle|sokak|cadde))',
                r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+(?:Mahallesi|Caddesi|Sokağı))',
                r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+/[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)',
            ],
            'institution': [
                r'(?:belediye|müdürlük|başkanlık|ofis|daire|birim)\b([^.]+?)(?=\s+(?:tarafından|ile|için))',
                r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+(?:Belediyesi|Müdürlüğü|Başkanlığı))',
            ],
            'date': [
                r'(\d{1,2}[./]\d{1,2}[./]\d{4})',
                r'(\d{1,2}\s+(?:Ocak|Şubat|Mart|Nisan|Mayıs|Haziran|Temmuz|Ağustos|Eylül|Ekim|Kasım|Aralık)\s+\d{4})',
                r'(?:son|geçtiğimiz)\s+(\d+\s+(?:gün|hafta|ay|yıl))',
            ],
            'subject': [
                r'(?:hakkında|konusunda|ile ilgili)\s+([^.]+?)(?=\s+(?:şikayetim|talebim|başvurum))',
                r'(?:şikayetim|talebim)\s+([^.]+?)(?=\s+(?:hakkında|konusunda))',
            ],
            'request': [
                r'(?:talep ediyorum|istiyorum|bekliyorum)\s*[:.]?\s*([^.]+)',
                r'(?:yapılmasını|çözülmesini|giderilmesini)\s+([^.]+?)(?:\s+(?:talep|rica))',
            ]
        }
        return patterns

    def extract_basic_info(self, text: str) -> Dict:
        """ Temel basit bilgilerin çıkarımı"""
        results = {}

        # eşleşmeleri bulur
        for field, pattern_list in self.patterns.items():
            matches = []
            for pattern in pattern_list:
                found = re.findall(pattern, text, re.IGNORECASE)
                matches.extend(found)

            # En uzun ve en anlamlı eşleşmeyi alır
            if matches:
                results[field] = max(matches, key=len).strip()
            else:
                results[field] = None

        return results

    def extract_subject_classification(self, text: str) -> str:
        """Konu kategorilerinin belirlenmesi"""
        categories = {
            'yol_sorunu': ['yol', 'asfalt', 'kaldırım', 'çukur', 'bozuk'],
            'su_kanalizasyon': ['su', 'kanalizasyon', 'atık', 'tıkanık', 'akıt'],
            'gurultu': ['gürültü', 'ses', 'rahatsız', 'müzik', 'bağır'],
            'cevre_temizlik': ['çöp', 'kirli', 'temizlik', 'süpür', 'hijyen'],
            'isik_aydinlatma': ['ışık', 'aydınlatma', 'karanlık', 'lamba', 'elektrik'],
            'park_bahce': ['park', 'bahçe', 'yeşil', 'ağaç', 'çiçek'],
            'otopark': ['otopark', 'araç', 'park', 'yer', 'dolmuş'],
            'guvenlik': ['güvenlik', 'hırsız', 'tehlike', 'korku', 'emniyet']
        }

        text_lower = text.lower()
        scores = {}

        for category, keywords in categories.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                scores[category] = score

        if scores:
            return max(scores, key=scores.get)
        return 'diger'
