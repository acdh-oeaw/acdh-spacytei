import spacy
from spacy.gold import GoldParse
from spacy.scorer import Scorer


def evaluate(ner_model, examples):
    scorer = Scorer()
    for x in examples:
        doc_gold_text = ner_model.make_doc(x[0])
        gold = GoldParse(doc_gold_text, entities=x[1]['entities'])
        pred_value = ner_model(x[0])
        scorer.score(pred_value, gold)
    return scorer.scores


def compare_models(models, examples):
    for x in models:
        ner_model = spacy.load(x)
        results = evaluate(ner_model, examples)
        print(
            x, "p: {}; f: {}; r: {}".format(
                results['ents_p'], results['ents_f'], results['ents_r']
            )
        )
