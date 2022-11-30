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
the problem of obtaining high lift-drag ratios at supersonic speeds .
the importance of the lift to drag ratio is well
known to all aircraft designers since it gives, to a
great extent, the aerodynamic efficiency of the airplane .
aerodynamic efficiency, however, is only one
component of the grand compromise that a completed
airplane represents .  at subsonic speeds, lift-drag
ratios of well over 200 have been measured in wind
tunnels on airfoil sections., but few powered aircraft
have attained (lift to drag ratio) value of 20 .  it is invariably true
that the requirements of stability and control, structure,
and flight operation all contribute to reducing the
design (lift to drag ratio) considerably below those exotic values
which can be predicted from unrestricted aerodynamic
theory .  if, however, a certain range or operating
efficiency is required, there is most certainly a minimum
if we examine the range equation we see that range is
proportional to the lift-drag ratio, the thermopropulsive
efficiency, and the logarithm of the initial to final
weight ratio .  the appearance of the lift-drag ratio as a
linear factor in the range equation indicates that every
attempt should be made to increase (lift to drag ratio)., however,
the search for higher (lift to drag ratio) may lead to strange
and unorthodox configurations .  most frequently, such
configurations are ruled out by the adverse effects of
their geometry on the weight ratios .  in the present
paper, we will deal with the maximum lift-drag ratio
problem for conventional configurations having a wing
and a body in close proximity to each other .  no attempt
will be made to select a particular configuration
as being the best .  however, the promising direction
to go from the aerodynamic view will be stressed with
the understanding that the other factors may outweight
the aerodynamics .
"""

import spacy
from collections import Counter
from models.dict import Dict

NLP = spacy.load('en_core_web_sm') 

terms = [ word.lemma_ for word in NLP(text) if word.pos_ == 'NOUN']
print('search' in terms)
terms = Dict(Counter(terms))

print(text)
for t in terms:
  print(t, terms[t])

# terms = [ unidecode(word.lower()) for word in 
#             re.findall(r"[\w]+", "La muchacHÁ 33 también fue..") 
#             if not re.match(r"[\d]+", word) ]
# print(' '.join(terms))

# import ir_datasets
# dataset = ir_datasets.load('cranfield')
# print(dataset)
