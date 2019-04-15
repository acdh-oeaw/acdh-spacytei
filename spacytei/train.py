import spacy
import datetime
import random

from pathlib import Path
from spacy.util import minibatch, compounding
from sklearn.model_selection import train_test_split
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


def compare_models(models, examples, verbose=True):
    compared = []
    for x in models:
        ner_model = spacy.load(x)
        results = evaluate(ner_model, examples)
        if verbose:
            print(
                x, "p: {}; f: {}; r: {}".format(
                    results['ents_p'], results['ents_f'], results['ents_r']
                )
            )
        compared.append((x, results))
    return compared


def batch_train(
    model=None,
    blank_model='de',
    output_dir=None,
    dropout=0.2,
    n_iter=12,
    eval_split=0.3,
    train_data=None,
    n_samples=None,
    new_label=None
):
    """Load the model, set up the pipeline and train the entity recognizer."""

    abs_start_time = datetime.datetime.now()

    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '{}'".format(model))
    elif blank_model is not None:
        nlp = spacy.blank(blank_model)  # create blank Language class
        print("Created blank model from '{}'".format(blank_model))
    else:
        print("You have to add either a model or a blank model")
        print("No training possible")
        return "nothing"

    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner, last=True)
    # otherwise, get it so we can add labels
    else:
        ner = nlp.get_pipe("ner")

    if new_label is not None:
        if model is None:
            optimizer = nlp.begin_training()
        else:
            optimizer = nlp.entity.create_optimizer()
        ner.add_label(new_label)

    TRAIN_DATA = train_data
    if n_samples is not None:
        TRAIN_DATA = TRAIN_DATA[:n_samples]
    train, test = train_test_split(TRAIN_DATA, test_size=eval_split)
    print("{} train vs {} test samples".format(len(train), len(test)))
    for _, annotations in train:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    prev_acc = 0.0
    with nlp.disable_pipes(*other_pipes):  # only train NER
        # reset and initialize the weights randomly – but only if we're
        # training a new model
        if model is None:
            nlp.begin_training()
        for itn in range(n_iter):
            print("Iteration Number: {}".format(itn))
            start_time = datetime.datetime.now()
            random.shuffle(train)
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(train, size=compounding(4.0, 16.0, 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                if new_label:
                    try:
                        nlp.update(
                            texts,
                            annotations,
                            sgd=optimizer,
                            drop=0.35,
                            losses=losses
                        )
                    except Exception as e:
                        print(e)
                else:
                    try:
                        nlp.update(
                            texts,  # batch of texts
                            annotations,  # batch of annotations
                            drop=0.5,  # dropout - make it harder to memorise data
                            losses=losses,
                        )
                    except Exception as e:
                        print(e)
            print("Losses", losses)
            end_time = datetime.datetime.now()
            print("Duration: {}".format(end_time - start_time))
            results = evaluate(nlp, test)
            print(
                "p: {}; f: {}; r: {}".format(
                    results['ents_p'], results['ents_f'], results['ents_r']
                )
            )
            acc = float(results['ents_f'])
            if acc > prev_acc:
                if output_dir is not None:
                    output_dir = Path(output_dir)
                    if not output_dir.exists():
                        output_dir.mkdir()
                    nlp.to_disk(output_dir)
                    print("Saved model to: {}".format(output_dir))
                prev_acc = acc
            print("######################")

    abs_end_time = datetime.datetime.now()
    print("######################")
    print("######################")
    print("######################")
    overall_duration = str(abs_end_time - abs_start_time)
    print("Overal duration: {}".format(overall_duration))
    if output_dir is not None:
        print("model with f1 score: {} saved to location: {}".format(prev_acc, output_dir))

    return nlp
