import ast


def extract_ents(spans):
    """ extracts spans from a prodigy sample
    :input spans: a list of prodigy prodigy samples
    :return: a dict {"entities": 0, 4, 'LABEL'}
    """
    ents = {"entities": []}
    for x in spans:
        ents["entities"].append((x['start'], x['end'], x['label']))
    return ents


def prodigy_jsonl_to_spacy(file):
    """ reads a prodigy NER output file and concerts it to a spacy jsonl
    :param file: Path to the file containing prodigy_samples
    :return: A list of spacy samples ['some text', {'entities': 0, 3, 'LABEL'}]
    """
    with open(file) as f:
        TRAIN_DATA = f.readlines()
        train_data = [ast.literal_eval(x) for x in TRAIN_DATA]
        return [((x['text']), extract_ents(x['spans'])) for x in train_data]


PRODIGY_SAMPLE = {
    "text": "Erbteilung für die Kinder der Regina Hoferin",
    "_input_hash": 854175238,
    "_task_hash": -741462820,
    "tokens": [
        {
            "text": "Erbteilung",
            "start": 0,
            "end": 10,
            "id": 0
        },
        {
            "text": "für",
            "start": 11,
            "end": 14,
            "id": 1
        },
        {
            "text": "die",
            "start": 15,
            "end": 18,
            "id": 2
        },
        {
            "text": "Kinder",
            "start": 19,
            "end": 25,
            "id": 3
        },
        {
            "text": "der",
            "start": 26,
            "end": 29,
            "id": 4
        },
        {
            "text": "Regina",
            "start": 30,
            "end": 36,
            "id": 5
        },
        {
            "text": "Hoferin",
            "start": 37,
            "end": 44,
            "id": 6
        }
    ],
    "spans": [
        {
            "start": 30,
            "end": 36,
            "token_start": 5,
            "token_end": 5,
            "label": "VN",
            "answer": "accept"
        }
    ],
    "answer": "accept"
}
