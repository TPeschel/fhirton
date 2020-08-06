import fhirton as ft
import os

if __name__ == '__main__':

    # fhir endpoint
    endp = "https://hapi.fhir.org/baseR4/"

    # fhir request
    req = "Observation?" \
          "code=http://loinc.org|85354-9&" \
          "_include=Observation:patient&" \
          "_include=Observation:encounter&" \
          "_format=xml&_count=500" \

    req = endp + req

    # designs 3, 2, 3
    designs = {
        "Observations": (".//Observation",),
        "Encounters": (".//Encounter", './/*'),
        "Patients": (".//Patient",)
    }

    # download fhir bundles and babble a lot
    bundles = ft.fhir_search(req=req, verbose=2)

    # crack/flatten the downloaded bundles to tables via designs
    # use space as separator and [] as brackets for indexing and babble a lot
    tables = ft.fhir_ton(bundles=bundles, designs=designs, sep=" ", bra=["[", "]"], verbose=3)

    # sort column names
    for k in tables.keys():
        tables[k].sort_index(axis=1, inplace=True)

    # create dir if not exist
    if not ('csv2' in os.listdir(".")):
        os.mkdir("csv2")

    # write tables as csv files
    for k in tables.keys():
        tables[k].to_csv("csv2/" + k + "_python.csv", sep=";", decimal=".", encoding="utf-8", index=False, na_rep='')

