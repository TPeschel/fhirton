d = {
    'Dictionary0': {
        'Tuple0': (
            'Anton',
            'Bert'
        ),
        'Tuple1': (
            'Anton',
            'Bert'
        ),
        'scalar0': 'f',
        'Dictionary0': {
            'Dictionary0': {
                'Tuple0': (
                    'Dietrich',
                    'Emil',
                    'Fred'
                ),
                'Scalar0': 'Curt',
                'Tuple1': (
                    'Gustav',
                    'Hans'
                ),
                'Scalar1': 'Igor',
                'Scalar2': 'Jens'
            }
        }
    },
    'Dictionary1': {
        'Dictionary0': {
            'Tuple0': (
                'Kurt',
                'Ludwig'
            )
        },
        'Dictionary1': {
            'List0': [
                'Max',
                'Norbert'
            ],
            'Tuple0': (
                [
                    'Otto',
                    'Paul',
                    (
                        'Quax',
                    )
                ],
                'Richard'
            )
        }
    },
    'Design': {
        "Observations": (
            ".//Observation",
            {
                "O.OID":      "./id",
                "O.PID":      "./subject/reference",
                "O.EID":      "./encounter/reference",
                "DIA.VALUE":  "./component/code/coding/code[@value='8462-4']/../../../valueQuantity/value",
                "DIA.UNIT":   "./component/code/coding/code[@value='8462-4']/../../../valueQuantity/unit",
                "DIA.SYSTEM": "./component/code/coding/code[@value='8462-4']/../system",
                "SYS.VALUE":  "./component/code/coding/code[@value='8480-6']/../../../valueQuantity/value",
                "SYS.UNIT":   "./component/code/coding/code[@value='8480-6']/../../../valueQuantity/unit",
                "SYS.SYSTEM": "./component/code/coding/code[@value='8480-6']/../system",
                "DATE":       "./effectiveDateTime"
            }
        )
    }
}


def t2s(obj, s='', p=0):
    first = True
    if isinstance(obj, dict):
        for k, v in obj.items():
            if first:
                first = False
                s += ' '
            else:
                s += '\n ' + p * ' '
            s += str(k) + ':'
            s = t2s(v, s, p + len(k) + 2)
    elif isinstance(obj, list) or isinstance(obj, tuple):
        bra = ']' if isinstance(obj, list) else ')'
        i = 0
        for v in obj:
            if first:
                first = False
            else:
                s += '\n' + p * ' '
            s += ' ' + str(i) + bra
            s = t2s(v, s, p + len(str(i)) + 2)
            i += 1
    else:
        s += ' ' + obj
    return s

design = {
    "Meta": {
        "Identifier": "Observations_Encounters_Patients_Blood_Pressure"
    },
    "Observations": (
        ".//Observation",
        {
            "O.OID": "./id",
            "O.PID": "./subject/reference",
            "O.EID": "./encounter/reference",
            "DIA.VALUE": "./component/code/coding/code[@value='8462-4']/../../../valueQuantity/value",
            "DIA.UNIT": "./component/code/coding/code[@value='8462-4']/../../../valueQuantity/unit",
            "DIA.SYSTEM": "./component/code/coding/code[@value='8462-4']/../system",
            "SYS.VALUE": "./component/code/coding/code[@value='8480-6']/../../../valueQuantity/value",
            "SYS.UNIT": "./component/code/coding/code[@value='8480-6']/../../../valueQuantity/unit",
            "SYS.SYSTEM": "./component/code/coding/code[@value='8480-6']/../system",
            "DATE": "./effectiveDateTime"
        }
    ),
    "Encounters": (
        ".//Encounter",
        {
            "E.EID": "./id",
            "E.PID": "./subject/reference",
            "START": "./period/start",
            "END": "./period/end"
        }
    ),
    "Patients": (
        ".//Patient",
        {
            "P.PID": "./id",
            "GVN.NAME": "./name/given",
            "FAM.NAME": "./name/family",
            "SEX": "./gender",
            "DOB": "./birthDate"
        }
    )
}

print(t2s(design))