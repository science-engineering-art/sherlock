# import spacy

# nlp = spacy.load('en_core_web_sm')

# text = ('This tutorial is about Natural Language Processing in Spacy')
# txt = nlp(text)


# print ([token.text for token in txt])

# dictt = {
#     'hla': 4,
#     'fss':2.3
# }
# from models.dict import Dict
# dictt = Dict(dictt)
# print(len(dictt))
# print(dictt['hla'], dictt['fss'], dictt['fjs'])

text = """
experiments on the use of suction through perforated
strips for maintaining laminar flow . transition and
drag measurements .
  wind-tunnel tests are described in which suction
is applied at perforated strips, as an alternative to
porous strips or slots, in order to maintain a laminar boundary
layer .  a test was first carried out on a single row of
perforations on a cambered plate, as a preliminary to the main
tests which were performed on strips of multiple rows
of perforations drilled through the surface of a low-drag-type
aerofoil 13 per cent thick and of 5-ft chord .
  up to a wind speed of 180 ft sec it has been ascertained that
suction may be safely applied to extend laminar flow
provided the ratio of hole diameter to boundary-layer displacement
thickness is less than 2, the ratio of hole pitch to
diameter is less than 3 and there are at least three rows of holes
in the strip .  with less than three rows, the criteria
are much more restrictive .  it is possible to extend laminar flow
by suction through perforations whose diameters and
pitches exceed these values slightly, but only with the risk that
excessive suction quantities will produce wedges of
turbulent boundary layer originating at the holes .
  a uniform distribution of suction through the holes was
necessary .  this was successfully obtained by two methods,
the use of cells and throttle holes, and with tapered holes .
in particular, tests were carried out on some panels
supplied by handley page, ltd., in which the cells and tapered
holes had been constructed by commercial methods, and
the suction distribution proved satisfactory .
  the resistance of some of the cellular arrangements was
measured .  it was found that when the suction quantities
were the minimum required to maintain laminar flow, the
additional losses in total head of the sucked air due to
the resistance of the throttle holes could be made small compared
with the loss in total head of the sucked boundary
layer .
"""

import spacy
from collections import Counter
from models.dict import Dict

NLP = spacy.load('en_core_web_sm') 

terms = [ word.lemma_ for word in NLP(text) if word.pos_ == 'NOUN']
terms = Dict(Counter(terms))

print(text)
for t in terms:
    print(t, terms[t])

# terms = [ unidecode(word.lower()) for word in 
#             re.findall(r"[\w]+", "La muchacHÁ 33 también fue..") 
#             if not re.match(r"[\d]+", word) ]
# print(' '.join(terms))