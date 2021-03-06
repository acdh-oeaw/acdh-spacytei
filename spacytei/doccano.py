import json

DOCCANO_TAG_MAP = {
    '1': 'PER',
    '2': 'LOC',
}


def doccano_to_spacy_ner_gold(
    input_file, output_file='out.jsonl', DOCCANO_TAG_MAP=DOCCANO_TAG_MAP, include_blanks=True
):
    """reads a doccano export file and returns a spacy-gold jsonl
    :param input_file: Path to doccano export file
    :param output_file: Name of file to store the spacy gold jsonl
    :param DOCCANO_TAG_MAP: A dict mapping doccano labels to spacy labels
    :return: the output file name
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        with open(output_file, 'w', encoding='utf-8') as out_file:
            for x in f.readlines():
                sample = json.loads(x)
                spacy_sample = []
                spacy_sample.append(sample['text'])
                spacy_annos = {}
                spacy_sample.append(spacy_annos)
                spacy_sample[1]['entities'] = []
                for y in sample['annotations']:
                    sp_anno = [
                        y['start_offset'],
                        y['end_offset'],
                        DOCCANO_TAG_MAP.get(y['label'], 'OBJECT')
                    ]
                    spacy_sample[1]['entities'].append(sp_anno)
                if include_blanks:
                    out_file.write(json.dumps(spacy_sample) + '\n')
                else:
                    if len(spacy_sample[1]['entities']) < 1:
                        pass
                    else:
                        out_file.write(json.dumps(spacy_sample) + '\n')

    return out_file
