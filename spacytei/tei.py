import logging
import re
from copy import deepcopy

import lxml.etree as ET

from spacytei.xml import XMLReader
from spacytei.data_prep import ne_offsets_by_sent


NER_TAG_MAP = {
    "persName": "PER",
    "person": "PER",
    "placeName": "LOC",
    "place": "LOC",
    "orgName": "ORG",
    "org": "ORG",
    "work": "MISC",
    "workName": "MISC"
}


class TeiReader(XMLReader):

    """ a class to read an process tei-documents"""

    def any_xpath(self, any_xpath='//tei:rs'):

        """ Runs any xpath expressions against the parsed document
        :param any_xpath: Any XPath expression.
        :return: The result of the xpath

        """
        return self.tree.xpath(any_xpath, namespaces=self.ns_tei)

    def extract_ne_elements(self, parent_node, ne_xpath='//tei:rs'):

        """ extract elements tagged as named entities
        :param ne_xpath: An XPath expression pointing to elements used to tagged NEs.
        :return: A list of elements

        """

        ne_elements = parent_node.xpath(ne_xpath, namespaces=self.ns_tei)
        return ne_elements

    def extract_ne_dicts(self, parent_node, ne_xpath='//tei:rs', NER_TAG_MAP=NER_TAG_MAP):

        """ extract strings tagged as named entities
        :param ne_xpath: An XPath expression pointing to elements used to tagged NEs.
        :param NER_TAG_MAP: A dictionary providing mapping from TEI tags used to tag NEs to\
        spacy-tags
        :return: A list of NE-dicts containing the 'text' and the 'ne_type'
        """

        ne_elements = self.extract_ne_elements(parent_node, ne_xpath)
        ne_dicts = []
        for x in ne_elements:
            item = {}
            text = "".join(x.xpath('.//text()'))
            item['text'] = re.sub('\s+', ' ', text).strip()
            try:
                ne_type = NER_TAG_MAP.get("{}".format(x.xpath('./@type')[0]), 'MISC')
            except IndexError as e:
                ne_type = NER_TAG_MAP.get("{}".format(x.xpath("name()")), 'MISC')
            item['ne_type'] = ne_type
            ne_dicts.append(item)

        return ne_dicts

    def create_plain_text(self, node):

        """ extracts all text nodes from given element
        :param start_node: An XPath expressione pointing to\
        an element which text nodes should be extracted
        :return: A normalized, cleaned plain text
        """
        result = re.sub('\s+', ' ', "".join(node.xpath(".//text()"))).strip()

        return result

    def get_text_nes_list(
            self,
            parent_nodes='.//tei:body//tei:p',
            ne_xpath='.//tei:rs',
            NER_TAG_MAP=NER_TAG_MAP
    ):

        """ extracts all text nodes from given elements and their NE
        :param parent_nodes: An XPath expressione pointing to\
        those elements which text nodes should be extracted
        :param ne_xpath:  An XPath expression pointing to elements used to tagged NEs.\
        Takes the parent node(s) as context
        :param NER_TAG_MAP: A dictionary providing mapping from TEI tags used to tag NEs to\
        spacy-tags
        :return: A list of dicts like [{"text": "Wien ist schön", "ner_dicts": [{"text": "Wien",\
        "ne_type": "LOC"}]}]
        """

        parents = self.tree.xpath(parent_nodes, namespaces=self.ns_tei)
        result = []
        for node in parents:
            text = self.create_plain_text(node)
            ner_dicts = self.extract_ne_dicts(node, ne_xpath, NER_TAG_MAP)
            result.append({'text': text, 'ner_dicts': ner_dicts})
        return result

    def extract_ne_offsets(
        self,
        parent_nodes='.//tei:body//tei:p',
        ne_xpath='.//tei:rs',
        NER_TAG_MAP=NER_TAG_MAP
    ):

        """ extracts offsets of NEs and the NE-type
        :param parent_nodes: An XPath expressione pointing to\
        those element which text nodes should be extracted
        :param ne_xpath: An XPath expression pointing to elements used to tagged NEs.\
        Takes the parent node(s) as context
        :param NER_TAG_MAP: A dictionary providing mapping from TEI tags used to tag NEs to\
        spacy-tags
        :return: A list of spacy-like NER Tuples [('some text'), {'entities': [(15, 19, 'place')]}]
        """

        text_nes_dict = self.get_text_nes_list(parent_nodes, ne_xpath, NER_TAG_MAP)
        result = []
        for x in text_nes_dict:
            plain_text = x['text']
            ner_dicts = x['ner_dicts']
            entities = []
            for x in ner_dicts:
                if x['text'] != "":
                    for m in re.finditer(x['text'], plain_text):
                        entities.append([m.start(), m.end(), x['ne_type']])
            entities = [item for item in set(tuple(row) for row in entities)]
            entities = sorted(entities, key=lambda x: x[0])
            ents = []
            next_item_index = 1
            # remove entities with the same start offset
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
            result.append(train_data)
        return result

    def ne_offsets_by_sent(
        self,
        parent_nodes='.//tei:body//tei:p',
        ne_xpath='.//tei:rs',
        model='de_core_news_sm',
        NER_TAG_MAP=NER_TAG_MAP
    ):

        """ extracts offsets of NEs and the NE-type grouped by sents
        :param parent_nodes: An XPath expressione pointing to\
        those element which text nodes should be extracted
        :param ne_xpath: An XPath expression pointing to elements used to tagged NEs.\
        Takes the parent node(s) as context
        :param model: The name of the spacy model which should be used for sentence splitting.
        :param NER_TAG_MAP: A dictionary providing mapping from TEI tags used to tag NEs to\
        spacy-tags
        :return: A list of spacy-like NER Tuples [('some text'), entities{[(15, 19, 'place')]}]
        """
        import spacy
        nlp = spacy.load(model)
        text_nes = self.get_text_nes_list(parent_nodes, ne_xpath, NER_TAG_MAP)
        results = ne_offsets_by_sent(text_nes, model=model)
        return results

    def create_tokenlist(self):
        """
        creates of token-dicts extracted from tei:w, tei:pc and tei:seg
        :return: a list of token dicts like:\
        [{'value': 'Ofen', 'tokenId': 'xTok_000001', 'whitespace': False}]
        """

        doc = self.tree
        expr = "//tei:*[local-name() = $name or local-name() = $pc]"
        words = doc.xpath(expr, name="w", pc="pc", namespaces=self.ns_tei)
        token_list = []
        for x in words:
            token = {}
            token['value'] = x.text
            token['tokenId'] = x.xpath('./@xml:id', namespaces=self.ns_tei)[0]
            try:
                if x.getnext().tag.endswith('seg'):
                    token['whitespace'] = True
                else:
                    token['whitespace'] = False
            except AttributeError:
                token['whitespace'] = False
            token_list.append(token)
        return token_list

    def process_tokenlist(self, tokenlist):
        """
        takes enriched tokenlist and updates the tei:w tags. Returns the updated self.tree
        :param tokenlist: An enriched tokenlist
        :return: The enriched self.tree
        """
        expr = './/tei:w[@xml:id=$xmlid]'
        parent_node = None
        node_pos = 0
        entity_element = None
        for sent in tokenlist:
            for x in sent['tokens']:
                try:
                    node = self.tree.xpath(expr, xmlid=x['tokenId'], namespaces=self.nsmap)[0]
                except IndexError:
                    node = None
                if node is not None:
                    if x.get('lemma'):
                        node.attrib['lemma'] = x.get('lemma')

                    if x.get('type'):
                        node.attrib['type'] = x.get('type')

                    if x.get('ana'):
                        node.attrib['ana'] = x.get('pos')

                    if x.get('iob'):
                        # TO DO: Preserve the position other TEI tags such as
                        # pg, lb, etc.
                        # At the moment, they'll get pushed to
                        # the end of the enclosing rs tag.
                        node.attrib['ent_iob'] = x.get('iob')
                        if x.get('iob').startswith('B-'):
                            ent_pos, ent_label = x.get('iob').split('-')

                            # find the position of the node in its parent
                            parent_node = node.getparent()
                            node_pos = parent_node.index(node)

                            # start the appropriate entity tag BEFORE word
                            entity_element = ET.Element('rs', {'type': ent_label})
                            entity_element.append(deepcopy(node))
                            node.clear()

                        elif x.get('iob').startswith('I') and entity_element is not None:
                            entity_element.append(deepcopy(node))
                            node.clear()

                        elif x.get('iob').startswith('O') and entity_element is not None:
                            # insert the entity element
                            # hoping that all the words in the entity have the same parent
                            parent_node.insert(node_pos, entity_element)
                            # reset the entity tag
                            parent_node = None
                            entity_element = None

        return self.tree

    def tokenize(
        self,
        XTX_URL='https://xtx.acdh.oeaw.ac.at/exist/restxq/xtx/tokenize/',
        profile='default'
    ):
        """
        posts self.tree to XTX endpoint for tokenization
        :param XTX_URL: Endpoint for the XTX service
        :param profile: The profile-id used for tokenization
        :return: The tokenized TEI document
        """
        try:
            import requests
        except ImportError:
            raise ImportError('Looks like requests is not installed, try pip install -U requests')

        url = "{}{}".format(XTX_URL, profile)
        payload = self.return_byte_like_object()
        headers = {
            'Content-Type': "application/xml",
            'Accept': "application/xml",
        }
        try:
            response = requests.request("POST", url, data=payload, headers=headers)
        except Exception as e:
            print(e)
            response is False
        if response:
            return response.text
        else:
            return response
