from fhirton import *
import lxml.etree as LX
from treestring import *

def designs2xml(designs):
    xml_designs = LX.Element('Designs')
    id = 0
    for k in designs:
        design = designs[k]
        if tuple == type(design):
            id += 1
            xml_design = LX.SubElement(xml_designs, 'Design')
            LX.SubElement(xml_design, 'Id', {'value': str(id)})
            LX.SubElement(xml_design, 'Name', {'value': str(k)})
            LX.SubElement(xml_design, 'Type', {'value': str(which_design(design))})
            LX.SubElement(xml_design, 'Resource', {'value': str(design[0])})
            if 1 < len(design):
                xml_design_table = LX.SubElement(xml_design, 'Table')
                if dict == type(design[1]):
                    for col_key in design[1].keys():
                        xml_design_table_column = LX.SubElement(xml_design_table, 'Column')
                        LX.SubElement(xml_design_table_column, 'Name', {'value': str(col_key)})
                        LX.SubElement(xml_design_table_column, 'XPath', {'value': str(design[1][col_key])})
                else:
                    xml_design_table_meta = LX.SubElement(xml_design, 'XPath', {'value': design[1]})
        else:
            xml_meta = LX.SubElement(xml_designs, k)
            for i, j in design.items():
                LX.SubElement(xml_meta, i,  {'value': str(j)})
    return xml_designs


designs = {
    "Meta": {
        "Identifier": "Observations_Encounters_Patients_Blood_Pressure"
    },
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

print(t2s(designs))


b = fhir_search("https://vonk.fire.ly/R4/Patient?_format=xml&_count=500&_revinclude=*", 3, 10)
d = fhir_ton(b, {"Pat": (".//Patient",)}, ' ', ['[', ']'], 3)

d['Pat'] = d['Pat'][d['Pat'].columns.sort_values()]
print(d['Pat'])


# xml_designs = designs2xml(designs)
# LX.dump(xml_designs)
# # with open("/home/tpeschel/POLAR/repos/fhirton/xml/design_oep.xml", "wb") as f:
# #     f.write(LX.tostring(xml_designs, pretty_print=True))
#
# print(tree2str(designs))

d = fhir_ton(b, {"Res": ("/Bundle/entry/resource/*",)})

for i in d:
    print(d[i])