import re
from textblob import TextBlob
from typing import Dict, List, Tuple


class ToneAnalyzer:
    def __init__(self):
        self.formal_indicators = [
            'saygılarımla', 'gereğini', 'müsaade', 'takdirlerinize',
            'arz ederim', 'rica ederim', 'sayın', 'muhterem'
        ]

        self.informal_indicators = [
            'ya', 'işte', 'yani', 'böyle', 'şöyle', 'falan', 'felan'
        ]

        self.angry_indicators = [
            'artık', 'yeter', 'bıktım', 'sinirliyim', 'öfke',
            'kabul edilemez', 'skandal', 'rezalet'
        ]

        self.polite_indicators = [
            'lütfen', 'rica', 'mümkünse', 'uygun görürseniz',
            'teşekkür', 'nazik', 'kibarca'
        ]

    def analyze_formality(self, text: str) -> Dict:
        """Resmiyyet düzeyinin analiz edilmesi"""
        text_lower = text.lower()

        formal_count = sum(1 for indicator in self.formal_indicators
                           if indicator in text_lower)
        informal_count = sum(1 for indicator in self.informal_indicators
                             if indicator in text_lower)

        # Yazım kurallarının  kontrol edilmesi
        grammar_score = self.check_grammar_compliance(text)

        if formal_count > informal_count and grammar_score > 0.7:
            formality = 'formal'
        elif informal_count > formal_count or grammar_score < 0.4:
            formality = 'informal'
        else:
            formality = 'semi_formal'

        return {
            'formality_level': formality,
            'formal_indicators': formal_count,
            'informal_indicators': informal_count,
            'grammar_compliance': grammar_score
        }

    def analyze_emotional_tone(self, text: str) -> Dict:
        """Duygusal tonun   analiz eedilmesi"""
        text_lower = text.lower()

        # Öfke skoru
        angry_score = sum(1 for indicator in self.angry_indicators
                          if indicator in text_lower)

        # Kibarlık skoru
        polite_score = sum(1 for indicator in self.polite_indicators
                           if indicator in text_lower)

        # Çaresizlik patternleri
        desperate_patterns = [
            r'ne yapacağımı bilmiyorum',
            r'çare[sş]izim',
            r'yardım[a-z]*\s+ihtiyacım',
            r'umut[a-z]*\s+kalmadı'
        ]

        desperate_score = sum(1 for pattern in desperate_patterns
                              if re.search(pattern, text_lower))

        # Ana tonun  belirlenmesi
        if angry_score > max(polite_score, desperate_score):
            main_tone = 'angry'
        elif desperate_score > max(angry_score, polite_score):
            main_tone = 'desperate'
        elif polite_score > 0:
            main_tone = 'polite_complaint'
        else:
            main_tone = 'neutral'

        return {
            'main_tone': main_tone,
            'angry_indicators': angry_score,
            'polite_indicators': polite_score,
            'desperate_indicators': desperate_score,
            'confidence': max(angry_score, polite_score, desperate_score) / 10
        }

    def check_grammar_compliance(self, text: str) -> float:
        """Yazım kurallarına uyum skorunun hesaplanamsı  """
        # Basit metrikler
        total_words = len(text.split())
        if total_words == 0:
            return 0.0

        # Büyük harf kullanımı
        sentences = re.split(r'[.!?]+', text)
        proper_start = sum(1 for s in sentences
                           if s.strip() and s.strip()[0].isupper())

        # Noktalama kullanımı
        punctuation_count = len(re.findall(r'[.!?,:;]', text))

        # Türkçe karakter kullanımı
        turkish_chars = len(re.findall(r'[çğıöşü]', text.lower()))

        # toplam Skor hesaplama
        sentence_score = proper_start / max(len(sentences) - 1, 1)
        punctuation_score = min(punctuation_count / (total_words / 10), 1.0)

        return (sentence_score + punctuation_score) / 2