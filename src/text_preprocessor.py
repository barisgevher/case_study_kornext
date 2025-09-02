import re
import spacy
from typing import Dict, List

class TextPreprocessor:
    def __init__(self):
        # türkçe dil modelini yükle başarısız olursa hata ver
        try:
            self.nlp = spacy.load("tr_core_news_sm")
        except OSError:
            print("Could not load turkish model continuing general model")
            self.nlp = spacy.blank("tr")

    def clean_text(self, text: str) -> str:
        """Metni temizler ve normalize eder"""

        #Özel karakterlerin temizlenmesi
        text = re.sub(r'\w\s\.\,\;\!\?\-\(\)','', text)

        # çoklu boşluklu alanları tek boşluk haline getirme
        text = re.sub(r'\s+', ' ', text)

        # türkçe karakter düzeltmeleri
        replacements = {
            'ı': 'ı', 'İ': 'İ', 'ş': 'ş', 'Ş': 'Ş',
            'ğ': 'ğ', 'Ğ': 'Ğ', 'ü': 'ü', 'Ü': 'Ü',
            'ö': 'ö', 'Ö': 'Ö', 'ç': 'ç', 'Ç': 'Ç'
        }
        return text.strip()

    def sentence_tokenize(self, text: str) -> List[str]:
        """ Metni cümlelere ayırma"""

        doc = self.nlp(text)
        return [sent.text.strip() for sent in doc.sents]

    def extract_entities(self, text: str) -> Dict:
        """Adlandırılmış varlıkları tanıma"""

        doc = self.nlp(text)
        entities = {
            'PERSON': [],
            'ORG': [],
            'LOC': [],
            'DATE': []
        }

        for ent in doc.ents:
            if ent.label_ in entities:
                entities[ent.label_].append(ent.text)

        return entities




