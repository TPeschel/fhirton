import fhirton as ft
import os
import pandas as pa
import re

if __name__ == '__main__':

    # fhir endpoint
    endp = "https://hapi.fhir.org/baseR4/"
    
    # fhir request
    req = "Observation?code=http://loinc.org|85354-9&_include=Observation:patient&_include=Observation:encounter" \
          "&_format=xml&_pretty=true&_count=500"

    fsq = endp + req

    # designs 1, 1, 1
    designs = {
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
        ),
        "Encounters": (
            ".//Encounter",
            {
                "E.EID": "./id",
                "E.PID": "./subject/reference",
                "START": "./period/start",
                "END":   "./period/end"
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

    # download fhir bundles and babble a lot
    bundles = ft.fhir_search(fsq, verbose=3)

    # crack/flatten the downloaded bundles to tables via designs and babble a lot
    tables = ft.fhir_ton(bundles, designs, sep=' ', bra=('[', ']'), verbose=3)

    # delete indices and prefixes for ids and references for merge
    for k in tables.keys():
        cols = tables[k].columns.values
        cols = list(filter(lambda x: re.findall('[OPE].[OPE]ID', x), cols))
        tables[k] = ft.rm_indices(tables[k], cols, ['[', ']'])
        for c in cols:
            tables[k][c] = [re.sub("^.*/(\\w+$)", "\\1", p) if p else None for p in tables[k][c]]

    # merge all tables
    tables['Total'] = pa.merge(tables['Observations'], tables['Encounters'],
                               left_on=['O.EID', 'O.PID'], right_on=['E.EID', 'E.PID'], how='inner')
    tables['Total'] = pa.merge(tables['Total'], tables['Patients'],
                               left_on=['O.PID'], right_on=['P.PID'], how='inner')

    # select some interesting columns
    tables['Total'] = tables['Total'][
        ["O.PID", "O.OID", "O.EID",
         "GVN.NAME", "FAM.NAME",
         "DOB", "SEX",
         "DIA.VALUE", "DIA.UNIT", "DIA.SYSTEM",
         "SYS.VALUE", "SYS.UNIT", "SYS.SYSTEM",
         "DATE", "START", "END"]
    ]

    # sort table columns
    tables['Total'] = tables['Total'].sort_values(by=['O.PID', 'O.OID', 'O.EID', "START"], ascending=True)

    # create dir if not exists
    if not ('csv1' in os.listdir(".")):
        os.mkdir("csv1")

    # save tables as csv files
    for k in tables.keys():
        tables[k].to_csv("csv1/" + k + "_python.csv", sep=";", decimal=".", encoding="utf-8", index=False, na_rep='')
