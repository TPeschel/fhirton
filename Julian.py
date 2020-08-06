from fhirton import *

bundles = fhir_search(
    'http://hapi.fhir.org/'
    'baseR4/'
    'Medication?'
    'code:text=24 HR Metformin hydrochloride 500 MG Extended Release Oral Tablet&'
    '_format=xml&_count=100', verbose=2, max_bundles=5)


df = fhir_ton(bundles, {'Medications': ('//Medication',)}, verbose=3)

print(df['Medications'])

df['Medications'].to_csv('Medications.csv', sep=";", decimal=".", encoding="utf-8", index=False, na_rep='')