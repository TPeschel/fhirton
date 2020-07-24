import fhirton as ft
import os
import pandas as pa
import re

if __name__ == '__main__':

    endp = "https://hapi.fhir.org/baseR4/"
    req  = "Observation?code=http://loinc.org|85354-9&_include=Observation:patient&_include=Observation:encounter&_format=xml&_pretty=true&_count=500"
    #req = "Observation?_include=Observation:patient&_include=Observation:encounter&_format=xml&_pretty=true&_count=500"
#    req = "Observation?_include=Observation:patient&_include=Observation:encounter&_format=xml&_pretty=true&_count=500"

    fsq = endp + req

    design = {
        "Observations": (".//Observation",),
        "Encounters": (".//Encounter", './/*'),
        "Patients": (".//Patient",)
    }

    bundles = ft.fhir_search(fsq)

    tables = ft.fhir_ton(bundles, design)

    for k in tables.keys():
        cols = tables[k].columns.values
        cols = list(filter(lambda x: re.findall('((encounter|subject)\\.reference$)|(id$)', x), cols))
        tables[k] = ft.rm_indices(tables[k], cols)
        for c in cols:
            tables[k][c] = [re.sub("^.*/(\\w+$)", "\\1", p) if p else None for p in tables[k][c]]

    tables['Total'] = pa.merge(
        tables['Observations'],
        tables['Encounters'],
        left_on=['encounter.reference', 'subject.reference'],
        right_on=['id', 'subject.reference'], how='left')

    tables['Total'] = pa.merge(
        tables['Total'],
        tables['Patients'],
        left_on=['subject.reference'],
        right_on=['id'], how='left')

    tables['Total'] = tables['Total'][
        ["subject.reference", 'id', 'id_x', "encounter.reference",
         "name.given", "name.family",
         "birthDate", "gender",
         "component.valueQuantity.value", "component.valueQuantity.unit",
         "component.valueQuantity.system", "component.valueQuantity.code",
         "effectiveDateTime", "period.start", "period.end"]
    ]

    tables['Total'] = tables['Total'].sort_values(by=['subject.reference', 'id_x', 'encounter.reference', "period.start"], ascending=True)

    if not ('csv2' in os.listdir(".")):
        os.mkdir("csv2")

    for k in tables.keys():
        tables[k].to_csv("csv2/" + k + "_python.csv", sep=";", decimal=".", encoding="utf-8", index=False, na_rep='')