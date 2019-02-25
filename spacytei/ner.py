import spacy


def format_iob_tag(token):
    if token.ent_iob_ != 'O':
        iob_tag = "{0}-{1}".format(token.ent_iob_, token.ent_type_)
    else:
        iob_tag = token.ent_iob_
    return iob_tag


def fetch_ner_samples(
        nlp,
        spacydoc,
        dont_split=False,
        ent_types=['OBJECT']
):
    """ takes a doc object and genereates NER-Training samples """
    spacy_samples = []
    if dont_split:
        spacy_sample = (spacydoc.text, {'entities': []})
        for ent in spacydoc.ents:
            if ent.label_ in ent_types:
                spacy_sample[1]['entities'].append((ent.start_char, ent.end_char, ent.label_))
        spacy_samples.append(spacy_sample)
        return spacy_samples
    else:
        sents = [x for x in spacydoc.sents]
        doc = None
        for sent in sents:
            doc = nlp(sent.text)
            spacy_sample = (sent.text, {'entities': []})
            for ent in doc.ents:
                if ent.label_ in ent_types:
                    spacy_sample[1]['entities'].append((ent.start_char, ent.end_char, ent.label_))
            spacy_samples.append(spacy_sample)
        return spacy_samples
