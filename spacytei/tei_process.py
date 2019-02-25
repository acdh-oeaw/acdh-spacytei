from spacytei.tei import TeiReader, NER_TAG_MAP


def teis_to_traindata(
    files,
    parent_node='.//tei:body',
    ne_xpath='.//tei:rs',
    verbose=True,
    NER_TAG_MAP=NER_TAG_MAP
):

    """ extract NER-Train-Data from bunch of TEI files
        :param files: A list of file paths to TEI documents
        :param parent_nodes: An XPath expressione pointing to\
        those element which text nodes should be extracted
        :param ne_xpath: An XPath expression pointing to elements used to tagged NEs.\
        Takes the parent node(s) as context
        :param NER_TAG_MAP: A dictionary providing mapping from TEI tags used to tag NEs to\
        spacy-tags
        :return: A list of lists of spacy-like NER Tuples\
        [(('some text'), entities{[(15, 19, 'place')]}), (...)]
    """

    TRAIN_DATA = []
    for x in files:
        tei_doc = TeiReader(x)
        try:
            ners = tei_doc.extract_ne_offsets(
                parent_nodes=parent_node, ne_xpath=ne_xpath, NER_TAG_MAP=NER_TAG_MAP
            )
        except Exception as e:
            print("Error: {} in file: {}".format(e, x))
        [TRAIN_DATA.append(x) for x in ners]

    return TRAIN_DATA


def teis_to_traindata_sents(
    files,
    parent_node='.//tei:body',
    ne_xpath='.//tei:rs',
    verbose=True,
    model='de_core_news_sm',
    NER_TAG_MAP=NER_TAG_MAP
):

    """ extract NER-Train-Data from bunch of TEI files
        :param files: A list of file paths to TEI documents
        :param parent_nodes: An XPath expressione pointing to\
        those element which text nodes should be extracted
        :param ne_xpath: An XPath expression pointing to elements used to tagged NEs.\
        Takes the parent node(s) as context
        :param model: The name of the spacy model which should be used for sentence splitting.
        :param NER_TAG_MAP: A dictionary providing mapping from TEI tags used to tag NEs to\
        spacy-tags
        :return: A list of lists of spacy-like NER Tuples\
        [(('some text'), entities{[(15, 19, 'place')]}), (...)]
    """

    TRAIN_DATA = []
    for x in files:
        tei_doc = TeiReader(x)
        try:
            ners = tei_doc.ne_offsets_by_sent(
                parent_nodes=parent_node, ne_xpath=ne_xpath, model=model, NER_TAG_MAP=NER_TAG_MAP
            )
        except Exception as e:
            print("Error: {} in file: {}".format(e, x))
        [TRAIN_DATA.append(x) for x in ners]

    return TRAIN_DATA
