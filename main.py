import fhirton as ft
import os

if __name__ == '__main__':

    endp = "https://hapi.fhir.org/baseR4/"
#    endp = "https://vonk.fire.ly/R4/"
    req  = "Observation?code=http://loinc.org|85354-9&_include=Observation:patient&_include=Observation:encounter&_format=xml&_pretty=true&_count=500"
#    req = "Observation?_include=Observation:patient&_include=Observation:encounter&_format=xml&_pretty=true&_count=500"

    fsq = endp + req

    design = {
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
                "E.EID": "id",
                "E.PID": "subject/reference",
                "START": "period/start",
                "END": "period/end"
            }
        ),
        "Patients": (
            ".//Patient",
            {
                "P.PID": "id",
                "GVN.NAME": "name/given",
                "FAM.NAME": "name/family",
                "SEX": "gender",
                "DOB": "birthDate"
            }
        )
    }

    bundles = ft.fhir_search(fsq)

    tables = ft.fhir_table(bundles, design)

    print(tables)

    if not ('csv' in os.listdir(".")):
        os.mkdir("csv")

    for k in tables.keys():
        tables[k].to_csv("csv/"+k+".csv", sep=";", decimal=".", encoding="utf-8")