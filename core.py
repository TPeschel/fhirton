import xml.etree.ElementTree as ET
import pandas as PA
#import xml.parsers.expat as EP
import re as RE
from typing import Dict, Any


def load_bundle(path: str):
    bundle_str = open(path, "r",encoding='utf-8').read()
    bundle_str = RE.sub('\s*xmlns\s*=\s*"[^"]+\s*"', '', bundle_str)
    return ET.fromstring(bundle_str)

def bundle2df(bundle, design_df):
    #ns: Dict[Any, str] = dict(f="http://hl7.org/fhir")

    xpath_resource = design_df[0]
    table_design = design_df[1]

    xml_res = bundle.findall(xpath_resource)

    df = [[0 for x in range(len(table_design.keys()))] for y in range(len(xml_res))]

    row = 0
    for r in xml_res:
        col = 0
        for col_name in table_design.keys():
            #xp = RE.sub("/@[-\w]+$", "", table_design[col_name])
            xp = table_design[col_name]
            y = r.findall(xp)
            z = [x.attrib['value'] if 'value' in x.attrib else 'NA' for x in y]
            df[row][col] = ' '.join(z)
            col += 1
        row += 1

    df = PA.DataFrame(df)
    df.columns = [str(k) for k in table_design.keys()]

    return df


def main():
    design = {
        "Observations": (
            ".//Observation",
            {
                "O.OID": "./id",
                "O.PID": "./subject/reference",
                "O.EID": "./encounter/reference",
                "DIA": "./component/code/coding/code[@value='8462-4']/../../../valueQuantity/value",
                "DIA.SYSTEM": "./component/code/coding/code[@value='8462-4']/../system",
                "SYS": "./component/code/coding/code[@value='8480-6']/../../../valueQuantity/value",
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

    bundle = load_bundle('bundles/observations_with_patients_and_encounters_hapi.xml')

    dfs = dict([(k, bundle2df(bundle, design[k])) for k in design.keys()])

    print(dfs)

    for k in dfs.keys():
        dfs[k].to_csv(k+".csv")
