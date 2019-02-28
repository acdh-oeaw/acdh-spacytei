from spacytei.tcf import Tcf
from spacytei.tei import TeiReader
from spacytei.tokenlist import doc_to_tokenlist
from spacytei.tokenlist import process_tokenlist
#from .base import check_validity_payload 



MAPPING_CONVERTERS = {'from': {
    'application/xml+tei': (TeiReader, [('xml', 'context.original_xml')], 'create_tokenlist', [],),
    'spacyDoc': (doc_to_tokenlist, [('doc', 'payload')]),
    'application/xml+tcf': (Tcf, [('xml', 'context.original_xml')], 'create_tokenlist', [],)
},
    'to': {
        'application/xml+tei': (TeiReader, [('xml', 'context.original_xml')], 'process_tokenlist', [('tokenlist', '$data_json',),]),
        'spacyDoc': (process_tokenlist, [('nlp', 'nlp'), ('tokenlist', '$data_json')]),
        'application/json+acdhlang': (doc_to_tokenlist, [('doc', 'payload')]),
    }
}


class Converter:

    def convert_bak(self, to):
        if len(MAPPING_CONVERTERS['to'][to]) == 2:
            self.data_converted = MAPPING_CONVERTERS['to'][to][0](self.data_json)
            self.data_converted = getattr(self.data_converted, MAPPING_CONVERTERS['to'][to][1])()
        else:
            self.data_converted = MAPPING_CONVERTERS['to'][to][0](self.data_json)
        return self.data_converted

    def _convert_internal(self, l, t):
        attr_dict = {}
        to = MAPPING_CONVERTERS[l][t]
        for d in to[1]:
            if d[1].startswith('$'):
                attr_dict[d[0]] = getattr(self, d[1][1:])
            else:
                lst_dict = d[1].split('.')
                attr_1 = lst_dict.pop(0)
                res_3 = getattr(self.original_process, attr_1)
                for att_2 in lst_dict:
                    res_3 = res_3[att_2]
                attr_dict[d[0]] = res_3
                #check_1 = getattr(self.original_process, 'context', None)
                #if check_1 is None:
                #    print('check worked correct')
                #    attr_dict[d[0]] = getattr(self.original_process, d[1])
                #else:
                #    print(d[1])
                #    if d[1] not in check_1.keys():
                #        attr_dict[d[0]] = getattr(self.original_process, d[1])
                #    else:
                #        attr_dict[d[0]] = check_1[d[1]]
        data_converted = to[0](**attr_dict)
        if len(to) > 2:
            attr_dict = {}
            for d in to[3]:
                if d[1].startswith('$'):
                    attr_dict[d[0]] = getattr(self, d[1][1:])
                else:
                    attr_dict[d[0]] = getattr(self.original_process, d[1])
            data_converted = getattr(data_converted, to[2])(**attr_dict)
        return data_converted

    def convert(self, to):
        self.data_converted = self._convert_internal('to', to)
        return self.data_converted
    
    def __init__(self, data_type=None, data=None, original_process=None):
        if data_type not in MAPPING_CONVERTERS['from'].keys() and data_type != 'application/json+acdhlang':
            raise ValueError('Data type specified is not supported by the converter.')
        if original_process is None:
            raise ValueError('Original process must be specified to get original files.') 
        else:
            self.original_process = original_process
        if data_type == 'application/json+acdhlang':
            self.data_json = data
        else:
            self.data_json = self._convert_internal('from', data_type)
