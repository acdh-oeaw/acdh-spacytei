import re
import pandas as pd

from spacytei.tei import TeiReader
from spacytei.data_prep import ne_offsets_by_sent


def recogito_dump_to_spacy_ner(recogito_export, tei_doc):
    """turns a recogito csv dump and the according TEI/XML to spacy-like NER Tuples
    :param recogito_export: A recogito csv
    :param tei_doc: The XML/TEI the recogito csv was derived from
    :return: A list of spacy-like NER Tuples [('some text'), {'entities': [(15, 19, 'place')]}]
    """

    df = pd.read_csv(recogito_export)
    doc = TeiReader(tei_doc)

    samples = []
    for i, row in df.iterrows():
        startxp, endxp = row['ANCHOR'].split(';')
        startxp, startc = startxp[10:].split('::')
        endxp, endc = endxp[8:].split('::')
        if startxp.startswith('text/body') and startxp == endxp:
            ent_dict = {}
            parent_node = re.search(r'text/body/.+?/p\[[0-9]+\]', startxp).group()
            parent_node = "tei:{}".format(parent_node)
            parent_node = "/tei:".join(parent_node.split('/'))
            plaintext = doc.any_xpath("{}//text()".format(parent_node))
            plaintext = re.sub('\s+', ' ', "".join(plaintext).strip())
            ent_dict['text'] = plaintext
            ent_dict['ner_dicts'] = []
            ent_dict['ner_dicts'].append({
                "text": row['QUOTE_TRANSCRIPTION'],
                "ne_type": row['TYPE']
            })
            samples.append([plaintext, row['QUOTE_TRANSCRIPTION'], row['TYPE']])

    df = pd.DataFrame(samples)
    samples = []
    for _, group in df.groupby(0):
        sample = {}
        sample['text'] = _
        sample['ner_dicts'] = []
        for i, row in group.iterrows():
            sample['ner_dicts'].append({
                "text": row[1],
                "ne_type": row[2]
            })
        samples.append(sample)

    final = ne_offsets_by_sent(samples)
    return final
