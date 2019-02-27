"""
This module provides some helper functions\
to save, clean and load spacy-like NER training data.
"""
import re
import ast
import langid

import pandas as pd


def ne_offsets_by_sent(
    text_nest_list=[],
    model='de_core_news_sm',
):

    """ extracts offsets of NEs and the NE-type grouped by sents
    :param text_nest_list: A list of list with following structure:\
    [{"text": "Wien ist schön", "ner_dicts": [{"text": "Wien", "ne_type": "LOC"}]}]
    :param model: The name of the spacy model which should be used for sentence splitting.
    :return: A list of spacy-like NER Tuples [('some text'), entities{[(15, 19, 'place')]}]
    """
    import spacy
    nlp = spacy.load(model)
    text_nes = text_nest_list
    results = []
    for entry in text_nes:
        ner_dicts = entry['ner_dicts']
        in_text = entry['text']
        doc = nlp(in_text)
        for sent in doc.sents:
            entities = []
            if sent.text != "":
                plain_text = sent.text
                for x in ner_dicts:
                    for m in re.finditer(x['text'], plain_text):
                        entities.append([m.start(), m.end(), x['ne_type']])
                entities = [item for item in set(tuple(row) for row in entities)]
                entities = sorted(entities, key=lambda x: x[0])
                ents = []
                next_item_index = 1
                for x in entities:
                    cur_start = x[0]
                    try:
                        next_start = entities[next_item_index][0]
                    except IndexError:
                        next_start = 9999999999999999999999
                    if cur_start == next_start:
                        pass
                    else:
                        ents.append(x)
                    next_item_index = next_item_index + 1
            train_data = (
                plain_text,
                {
                    "entities": ents
                }
            )
            results.append(train_data)
    return results


def clean_train_data(train_data, min_ents=0, min_text_len=5, lang=['de']):

    """ removes items with no entities or fewer entities then min_ents
        :param train_data: A list of lists of spacy-like NER Tuple\
        [(('some text'), entities{[(15, 19, 'place')]}), (...)]
        :param min_ents: An integer defining the minimum amount of entities.
        :min_text_len: An integer defining the minimum length of the textself.
        :lang: A list of language codes. If populated, only samples matching those languages will\
        be included into the returned results.
        :return: A list of lists of spacy-like NER Tuple\
        [(('some text'), entities{[(15, 19, 'place')]}), (...)]
    """

    TRAIN_DATA = []
    for x in train_data:
        try:
            ents = x[1]
        except TypeError:
            ents = None
        if ents and len(ents['entities']) >= min_ents and len(x[0]) >= min_text_len:
            TRAIN_DATA.append(x)
    if len(lang) > 0:
        TRAIN_DATA_LANG = []
        for x in TRAIN_DATA:
            lng, prob = langid.classify(x[0])
            if lng in lang:
                TRAIN_DATA_LANG.append(x)
        return TRAIN_DATA_LANG

    return TRAIN_DATA


def traindata_to_csv(train_data, filename='out.csv'):

    """Saves list of lists of spacy-like NER Tuples as csv.
        :param train_data: A list of lists of spacy-like NER Tuple\
        [(('some text'), entities{[(15, 19, 'place')]}), (...)]
        :param filename: The name of the .csv file
        :returns: The filename.
    """

    df = pd.DataFrame(train_data, columns=["text", "entities"])
    df.to_csv(filename, index=False)
    return filename


def csv_to_traindata(csv):

    """ loads as csv and returns as TRAIN_DATA List
        :param csv: Path to the csv file.
        :return: A list of lists of spacy-like NER Tuple\
        [(('some text'), entities{[(15, 19, 'place')]}), (...)]
    """
    new = pd.read_csv(csv)
    TRAIN_DATA = []
    for i, row in new.iterrows():
        item = []
        item.append(row[0])
        ents = ast.literal_eval(row[1])
        item.append(ents)
        TRAIN_DATA.append(item)
    return TRAIN_DATA


TOKENEDITOR_SCHEMA = [
    {
        "propertyName": "dep",
        "propertyType": "closed list",
        "propertyValues": [
            {'value': 'ac'},
            {'value': 'adc'},
            {'value': 'ag'},
            {'value': 'ams'},
            {'value': 'app'},
            {'value': 'avc'},
            {'value': 'cc'},
            {'value': 'cd'},
            {'value': 'cj'},
            {'value': 'cm'},
            {'value': 'cp'},
            {'value': 'cvc'},
            {'value': 'da'},
            {'value': 'dh'},
            {'value': 'dm'},
            {'value': 'ep'},
            {'value': 'hd'},
            {'value': 'ju'},
            {'value': 'mnr'},
            {'value': 'mo'},
            {'value': 'ng'},
            {'value': 'nk'},
            {'value': 'nmc'},
            {'value': 'oa'},
            {'value': 'oa'},
            {'value': 'oc'},
            {'value': 'og'},
            {'value': 'op'},
            {'value': 'par'},
            {'value': 'pd'},
            {'value': 'pg'},
            {'value': 'ph'},
            {'value': 'pm'},
            {'value': 'pnc'},
            {'value': 'rc'},
            {'value': 're'},
            {'value': 'rs'},
            {'value': 'sb'},
            {'value': 'ac'},
            {'value': 'adc'},
            {'value': 'ag'},
            {'value': 'ams'},
            {'value': 'app'},
            {'value': 'avc'},
            {'value': 'cc'},
            {'value': 'cd'},
            {'value': 'cj'},
            {'value': 'cm'},
            {'value': 'cp'},
            {'value': 'cvc'},
            {'value': 'da'},
            {'value': 'dh'},
            {'value': 'dm'},
            {'value': 'ep'},
            {'value': 'hd'},
            {'value': 'ju'},
            {'value': 'mnr'},
            {'value': 'mo'},
            {'value': 'ng'},
            {'value': 'nk'},
            {'value': 'nmc'},
            {'value': 'oa'},
            {'value': 'oa'},
            {'value': 'oc'},
            {'value': 'og'},
            {'value': 'op'},
            {'value': 'par'},
            {'value': 'pd'},
            {'value': 'pg'},
            {'value': 'ph'},
            {'value': 'pm'},
            {'value': 'pnc'},
            {'value': 'rc'},
            {'value': 're'},
            {'value': 'rs'},
            {'value': 'sb'}
        ]
    },
    {
        "propertyName": "ent_iob",
        "propertyType": "closed list",
        "propertyValues": [
            {"value": "O"},
            {"value": "B"},
            {"value": "I"}
        ]
    },
    {
        "propertyName": "ent_type",
        "propertyType": "closed list",
        "propertyValues": [
            {"value": ""},
            {"value": "LOC"},
            {"value": "ORG"},
            {"value": "MISC"},
            {"value": "PER"}
        ]
    },
    {
        "propertyName": "iob",
        "propertyType": "closed list",
        "propertyValues": [
            {"value": "O"},
            {"value": "B-LOC"},
            {"value": "I-LOC"},
            {"value": "B-ORG"},
            {"value": "I-ORG"},
            {"value": "B-MISC"},
            {"value": "I-MISC"},
            {"value": "B-PER"},
            {"value": "I-PER"},
        ]
    },
    {
        "propertyName": "is_alpha",
        "propertyType": "bool"
    },
    {
        "propertyName": "lemma",
        "propertyType": "free text"
    },
    {
        "propertyName": "pos",
        "propertyType": "closed list",
        "propertyValues": [
            {'value': 'PUNCT'},
            {'value': 'ADV'},
            {'value': 'DET'},
            {'value': 'VERB'},
            {'value': 'NUM'},
            {'value': 'SPACE'},
            {'value': 'CONJ'},
            {'value': 'X'},
            {'value': 'SCONJ'},
            {'value': 'AUX'},
            {'value': 'ADP'},
            {'value': 'PART'},
            {'value': 'NOUN'},
            {'value': 'INTJ'},
            {'value': 'ADJ'},
            {'value': 'PROPN'},
            {'value': 'PRON'}
        ]
    },
    {
        "propertyName": "shape",
        "propertyType": "free text"
    },
    {
        "propertyName": "token_id",
        "propertyType": "free text"
    },
    {
        "propertyName": "type",
        "propertyType": "closed list",
        "propertyValues": [
            {'value': '$('},
            {'value': '$,'},
            {'value': '$.'},
            {'value': 'ADJA'},
            {'value': 'ADJD'},
            {'value': 'ADV'},
            {'value': 'APPO'},
            {'value': 'APPR'},
            {'value': 'APPRART'},
            {'value': 'APZR'},
            {'value': 'ART'},
            {'value': 'CARD'},
            {'value': 'FM'},
            {'value': 'ITJ'},
            {'value': 'KOKOM'},
            {'value': 'KON'},
            {'value': 'KOUI'},
            {'value': 'KOUS'},
            {'value': 'NE'},
            {'value': 'NNE'},
            {'value': 'NN'},
            {'value': 'PAV'},
            {'value': 'PROAV'},
            {'value': 'PDAT'},
            {'value': 'PDS'},
            {'value': 'PIAT'},
            {'value': 'PIDAT'},
            {'value': 'PIS'},
            {'value': 'PPER'},
            {'value': 'PPOSAT'},
            {'value': 'PPOSS'},
            {'value': 'PRELAT'},
            {'value': 'PRELS'},
            {'value': 'PRF'},
            {'value': 'PTKA'},
            {'value': 'PTKANT'},
            {'value': 'PTKNEG'},
            {'value': 'PTKVZ'},
            {'value': 'PTKZU'},
            {'value': 'PWAT'},
            {'value': 'PWAV'},
            {'value': 'PWS'},
            {'value': 'TRUNC'},
            {'value': 'VAFIN'},
            {'value': 'VAIMP'},
            {'value': 'VAINF'},
            {'value': 'VAPP'},
            {'value': 'VMFIN'},
            {'value': 'VMINF'},
            {'value': 'VMPP'},
            {'value': 'VVFIN'},
            {'value': 'VVIMP'},
            {'value': 'VVINF'},
            {'value': 'VVIZU'},
            {'value': 'VVPP'},
            {'value': 'XY'},
            {'value': 'SP'}
        ]
    },
    {
        "propertyName": "type",
        "propertyType": "free text"
    },
    {
        "propertyName": "value",
        "propertyType": "free text"
    }
]
