import json
import os
from datetime import datetime
from typing import Dict, Any, List
from text_preprocessor import TextPreprocessor
from information_extractor import InformationExtractor
from inference_engine import InferenceEngine
from tone_analyzer import ToneAnalyzer


class PetitionAnalyzer:
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.extractor = InformationExtractor()
        self.inference_engine = InferenceEngine()
        self.tone_analyzer = ToneAnalyzer()

    def analyze_petition(self, text: str) -> Dict[str, Any]:
        """Dilekçenin tam analizinin yapılması"""
        # ön işleme
        cleaned_text = self.preprocessor.clean_text(text)
        sentences = self.preprocessor.sentence_tokenize(cleaned_text)
        entities = self.preprocessor.extract_entities(cleaned_text)

        # temel bilgi çıkarımının yapılması
        basic_info = self.extractor.extract_basic_info(cleaned_text)
        subject_category = self.extractor.extract_subject_classification(cleaned_text)

        # çıkarımların yapılması
        severity_analysis = self.inference_engine.infer_problem_severity(cleaned_text)
        citizen_profile = self.inference_engine.infer_citizen_profile(cleaned_text)

        # duygu ve resmilik analizi
        formality_analysis = self.tone_analyzer.analyze_formality(cleaned_text)
        emotional_analysis = self.tone_analyzer.analyze_emotional_tone(cleaned_text)

        # birleştirme
        results = {
            "metadata": {
                "analysis_date": datetime.now().isoformat(),
                "text_length": len(cleaned_text),
                "sentence_count": len(sentences)
            },
            "extracted_information": {
                "name": basic_info.get('name'),
                "address": basic_info.get('address'),
                "institution": basic_info.get('institution'),
                "date": basic_info.get('date'),
                "subject": basic_info.get('subject'),
                "subject_category": subject_category,
                "request": basic_info.get('request')
            },
            "inference_analysis": {
                "problem_severity": severity_analysis,
                "citizen_profile": citizen_profile
            },
            "tone_and_language": {
                "formality": formality_analysis,
                "emotional_tone": emotional_analysis
            },
            "named_entities": entities,
            "reasoning": {
                "extraction_confidence": self.calculate_extraction_confidence(basic_info),
                "analysis_notes": self.generate_analysis_notes(
                    severity_analysis, emotional_analysis, formality_analysis
                )
            }
        }

        return results

    def calculate_extraction_confidence(self, basic_info: Dict) -> float:
        """Çıkarımların güven skorunun hesaplaması"""
        filled_fields = sum(1 for value in basic_info.values() if value)
        total_fields = len(basic_info)
        return filled_fields / total_fields

    def generate_analysis_notes(self, severity, emotional, formality) -> List[str]:
        """Analiz notlarının üretilmesi"""
        notes = []

        if severity['severity_level'] == 'high':
            notes.append("Yüksek ciddiyette bir problem tespit edildi")

        if emotional['main_tone'] == 'angry':
            notes.append("Kişi öfkeli bir dil kullanıyor")
        elif emotional['main_tone'] == 'desperate':
            notes.append("Kişi çaresizlik belirtileri gösteriyor")

        if formality['formality_level'] == 'formal':
            notes.append("Metin formal dilde yazılmış")
        elif formality['formality_level'] == 'informal':
            notes.append("Metin günlük dilde yazılmış")

        return notes

    def save_results(self, results: Dict, filename: str = None):
        """Sonuçları JSON olarak kaydet"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"petition_analysis_{timestamp}.json"


        output_dir = "outputs"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"'{output_dir}' klasörü oluşturuldu")

        file_path = os.path.join(output_dir, filename)

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"Sonuçlar başarıyla kaydedildi: {file_path}")
        except Exception as e:
            print(f"Dosya kaydetme hatası: {e}")

            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)
                print(f"Sonuçlar mevcut dizine kaydedildi: {filename}")
            except Exception as e2:
                print(f"Alternatif kaydetme de başarısız: {e2}")
                return None

        return filename