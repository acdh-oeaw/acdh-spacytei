import spacy
from spacy.scorer import Scorer
from spacy.gold import GoldParse
from spacy.tokens import Doc
from spacy.vocab import Vocab

# evaluation script

# tag_acc = []
# scorer = Scorer()
# for text, annot in TEST_DATA:
#     doc = Doc(nlp.vocab, words=annot[0]['word'])
#     gold = GoldParse(doc, tags=annot[1]['tags'])
#     pred_value = nlp(text)
#     try:
#         scorer.score(pred_value, gold)
#         tag_acc.append(scorer.scores['tags_acc'])
#     except Exception as e:
#         pass
