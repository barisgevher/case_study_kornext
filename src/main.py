from main_analyzer import PetitionAnalyzer


def main():
    analyzer = PetitionAnalyzer()

    sample_text = """
    Sayın Belediye Başkanımız,

    Ben Mehmet Yılmaz, Çankaya Mahallesi Atatürk Caddesi'nde ikamet etmekteyim.
    Son 3 aydır mahallemizdeki yol sorunundan dolayı çok mağdur oluyoruz.
    Her yağmurda çukurlar su doluyor ve araçlarımız zarar görüyor.

    Defalarca bildirdiğimiz halde henüz bir çözüm bulamadık.
    Bu durumun bir an önce çözülmesini talep ediyoruz.

    Saygılarımla,
    Mehmet Yılmaz
    """

    results = analyzer.analyze_petition(sample_text)

    # Sonuçları kaydet
    result = analyzer.save_results(results)
    print(f"Analiz sonucu kaydedildi: {result}")

    # Özet göster
    print("\n=== ANALİZ ÖZETİ ===")
    print(f"İsim: {results['extracted_information']['name']}")
    print(f"Konu: {results['extracted_information']['subject_category']}")
    print(f"Ciddiyet: {results['inference_analysis']['problem_severity']['severity_level']}")
    print(f"Ton: {results['tone_and_language']['emotional_tone']['main_tone']}")


if __name__ == "__main__":
    main()