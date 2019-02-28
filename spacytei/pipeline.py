#from exceptions import ValueError, AttributeError
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import json
import spacy
import requests
from .conversion import Converter
from enrich.default_settings import SPACY_LANG_LST, SPACY_PIPELINE
import os
from lxml import etree
from io import StringIO, BytesIO


def check_validity_payload(kind, payload):
    if kind == "application/json+acdhlang":
        with open('jsonschema/acdh_lang_jsonschema.json') as s:
            schema = json.load(s)
            try:
                validate(payload, schema)
                return True
            except ValidationError:
                return False
    elif kind == "spacyDoc":
        if type(payload) == spacy.tokens.doc.Doc:
            return True
        else:
            return False
    elif kind == "text/plain":
        if type(payload) == str:
            return True
        else:
            return False
    elif kind == "application/xml+tei":
        return True
        with open('jsonschema/tei_all.xsd', 'rb') as schema_tei:
            schema_tei = schema_tei.read()
        xml_doc = etree.parse(BytesIO(payload))
        schema_tei_doc = etree.parse(BytesIO(schema_tei))
        schema_tei = etree.XMLSchema(schema_tei_doc)
        if not schema_tei.assertValid(xml_doc):
            return False
        else:
            return True
    elif kind == "application/xml+tcf":
        return True


class PipelineProcessBase:
    """PipelineProcessBase: Baseclass for deriving NLP processes"""
    accepts = ["application/json+acdhlang"]
    returns = "application/json+acdhlang"
    payload = None
    valid = False
    
    def convert_payload(self):
        self.payload = Converter(data_type=self.mime, data=self.payload, original_process=self).convert(to=self.accepts[0])
        #print('payload converted: {}'.format(self.payload))
        self.mime = self.accepts[0]
        self.check_validity()

    def check_validity(self):
        """check_validity: checks if the payload is accepted by the function.
           Starts converting process if needed.
        """
        if self.mime is None:
            raise ValueError('You must specify a mime type of the payload.')
        if self.payload is None:
            raise ValueError('You cant call pipeline processes without specifying a payload.')
        if not check_validity_payload(self.mime, self.payload):
            raise ValueError('Payload is not in the correct format')
        if self.mime not in self.accepts:
            self.convert_payload()
        self.valid = True

    def __init__(self, *args, **kwargs):
        """__init__

        :param payload: data for the process
        :param mime: mime type of the payload data
        """
        self.payload = kwargs.get('payload', None)
        self.mime = kwargs.get('mime', None)
        self.context = kwargs.get('context', None)
        if self.context is None:
            self.context = {}
        #print(kwargs)
        print(self.mime)
        #print('payload: {}'.format(self.payload))
        self.check_validity()


class SpacyProcess(PipelineProcessBase):
    accepts = ["spacyDoc", "text/plain"]
    returns = "spacyDoc"

    def process(self):
        if self.mime == "text/plain":
            self.payload = self.nlp(self.payload)
        else:
            for name, proc in self.nlp.pipeline:
                self.payload = proc(self.payload)
        return self.payload

    def __init__(self, options=None, pipeline=None, **kwargs):
        self.pipeline = pipeline
        self.options = options
        if self.options is not None:
            if self.options['model']:
                model = os.path.join('~/media/pipeline_models', self.options['model']) 
            elif self.options['language']:
                model = SPACY_LANG_LST[self.options['language'].lower()]
        else:
            model = 'de'
        if self.pipeline is None:
            disable_pipeline = []
        else:
            disable_pipeline = [
                x for x in SPACY_PIPELINE if x not in self.pipeline
            ]
        self.nlp = spacy.load(
            model,
            disable=disable_pipeline,
        )
        super().__init__(**kwargs)
        if not self.valid:
            raise ValueError('Something went wrong in the data conversion. Data is not valid.')


class XtxProcess(PipelineProcessBase):
    accepts = ['application/xml+tei']
    returns = 'application/xml+tei'
    
    def process(self):
        headers = {
            'Content-type': 'application/xml;charset=UTF-8', 'accept': 'application/xml'
        }
        url = self.XTX_URL
        res = requests.post(url, headers=headers, data=self.payload.encode('utf-8'))
        if res.status_code == 200:
            self.payload = res.text
            self.context['original_xml'] = self.payload
        else:
            raise ValueError('XTX did not respond with status code 200.')
        return self.payload

    def __init__(self, options=None, pipeline=None, **kwargs):
        self.pipeline = pipeline
        self.options = options
        self.XTX_URL = kwargs.get('XTX_URL', None)
        if self.XTX_URL is None:
            from django.conf import settings
            self.XTX_URL = settings.XTX_URL
        super().__init__(**kwargs)
        if not self.valid:
            raise ValueError('Something went wrong in the data conversion. Data is not valid.')
