from spacy.tokens import Doc, Token
from spacytei.ner import format_iob_tag


SPACY_ACCEPTED_DATA = ['POS', 'ENT_TYPE', 'ENT_TYPE_']


def doc_to_tokenlist_no_sents(doc):
    """ serializes a spacy DOC object into a python list with tokens grouped by sents
    :param doc: spacy DOC element
    :return: a list of of token objects/dicts
    """
    result = []
    for x in doc:
        token = {}
        if y.has_extension('tokenId'):
            parts['tokenId'] = y._.tokenId
        else:
            parts['tokenId'] = y.i
        token['value'] = x.text
        token['lemma'] = x.lemma_
        token['pos'] = x.pos_
        token['type'] = x.tag_
        token['dep'] = x.dep_
        token['shape'] = x.shape_
        token['is_alpha'] = x.is_alpha
        token['ent_iob'] = x.ent_iob_
        token['iob'] = format_iob_tag(x)
        token['ent_type'] = x.ent_type_
        result.append(token)
    return result


def doc_to_tokenlist(doc):
    """ serializes a spacy DOC object into a python list with tokens grouped by sents
    :param doc: spacy DOC element
    :return: a list of of token objects/dicts grouped by sents
    """
    sents = [x for x in doc.sents]
    result = []
    counter = 0
    for x in sents:
        chunk = {}
        chunk['sent'] = "{}".format(x)
        chunk['tokens'] = []
        for y in x:
            parts = {}
            try:
                parts['tokenId'] = y._.tokenId
            except:
                parts['tokenId'] = y.i
            parts['value'] = y.text
            parts['lemma'] = y.lemma_
            parts['pos'] = y.pos_
            parts['type'] = y.tag_
            parts['dep'] = y.dep_
            parts['shape'] = y.shape_
            parts['is_alpha'] = y.is_alpha
            parts['ent_iob'] = y.ent_iob_
            parts['iob'] = format_iob_tag(y)
            parts['ent_type'] = y.ent_type_
            chunk['tokens'].append(parts)
            counter += 1
        result.append(chunk)
    return result


def process_tokenlist(nlp, tokenlist, enriched=False, SPACY_ACCEPTED_DATA=SPACY_ACCEPTED_DATA):
    """process_tokenlist: creates a spacy doc element of a token list

    :param nlp: spacy NLP element
    :param tokenlist: list of dicts containing tokens and parameters
    :param enriched: if set to True spacy pipeline is run
    """
    json = {}
    json['tokenArray'] = tokenlist
    ar_tok = [x['value'] for x in json['tokenArray']]
    ar_wsp = [x.get('whitespace', True) for x in json['tokenArray']]
    doc = Doc(nlp.vocab, words=ar_tok, spaces=ar_wsp)
    for id, t in enumerate(doc):
        if t.get_extension('tokenId') is None:
            t.set_extension('tokenId', default=False)
        t._.set('tokenId', json['tokenArray'][id].get('tokenId', False))
        t_type = json['tokenArray'][id].get('type', False)
        if not t.tag_ and t_type:
            t.tag_ = t_type
        for k in json['tokenArray'][id].keys():
            if k.upper() in SPACY_ACCEPTED_DATA:
                setattr(
                    t,
                    k.lower(),
                    json['tokenArray'][id][k],
                )  # TODO: need to set ent_iob
    if enriched:
        for name, proc in nlp.pipeline:
            doc = proc(doc)
    return doc
