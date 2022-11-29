# import spacy

# nlp = spacy.load('en_core_web_sm')

# text = ('This tutorial is about Natural Language Processing in Spacy')
# txt = nlp(text)


# print ([token.text for token in txt])

dictt = {
    'hla': 4,
    'fss':2.3
}
from models.dict import Dict
dictt = Dict(dictt)
print(len(dictt))
print(dictt['hla'], dictt['fss'], dictt['fjs'])

# terms = [ unidecode(word.lower()) for word in 
#             re.findall(r"[\w]+", "La muchacHÁ 33 también fue..") 
#             if not re.match(r"[\d]+", word) ]
# print(' '.join(terms))