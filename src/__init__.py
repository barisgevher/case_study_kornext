from main_analyzer import PetitionAnalyzer


def main():
    analyzer = PetitionAnalyzer()

    sample_text = """
  Sayın Yetkili,
Son iki haftadır her akşam saat 20:00 civarında mahallemizde elektrikler kesilmektedir.
 Özellikle çocukların ders saatine denk gelen bu kesintiler nedeniyle mağduriyet yaşıyoruz. 
 Konuyla ilgili defalarca arıza bildirimi yapmamıza rağmen kalıcı bir çözüm sunulmamıştır. 
 Gereğinin yapılmasını arz ederim.
Ali Demirtaş, Bahçelievler / İstanbul
    """

    results = analyzer.analyze_petition(sample_text)

    # Sonuçları kaydet
    result_demo = analyzer.save_results(results)
    print(f"Analiz sonucu kaydedildi: {result_demo}")

    # Özet göster
    print("\n=== ANALİZ ÖZETİ ===")
    print(f"İsim: {results['extracted_information']['name']}")
    print(f"Konu: {results['extracted_information']['subject_category']}")
    print(f"Ciddiyet: {results['inference_analysis']['problem_severity']['severity_level']}")
    print(f"Ton: {results['tone_and_language']['emotional_tone']['main_tone']}")


if __name__ == "__main__":
    main()