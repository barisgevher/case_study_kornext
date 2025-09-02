
import spacy
nlp = spacy.blank("tr")
nlp.add_pipe('sentencizer')
doc = nlp("Bu bir test cümlesi. Bu ikinci cümle.")
for sent in doc.sents:
    print(sent.text)