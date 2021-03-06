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
