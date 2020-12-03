from fhirton import *
import os

print(os.getcwd())

#bundle = fhir_search("http://10.50.8.14:8080/fhir/_/Medication/?code=http://www.kbv.de/pzn%7C0850589&_format=xml")
#bundles = [bundle]

bundles = fhir_search(
     'http://hapi.fhir.org/'
     'baseR4/'
     'Medication?'
     'code:text=24 HR Metformin hydrochloride 500 MG Extended Release Oral Tablet&'
     '_format=xml&_count=100', verbose=2, max_bundles=5)

dct_med = fhir_ton(bundles, {'Medications': ('//Medication',)}, sep=";", bra=["<", ">"], verbose=3)
dct_ing = fhir_ton(bundles, {'Medications': ('//Medication/ingredients',)}, sep=";", bra=["<", ">"], verbose=3)


df = dct_ing['Medications']
print(df)
df = rm_indices(df)
df_codes = getMedicationIngredientCodes(df, ";", onlyAPI=False)
print(df_codes)
mask_cas = df_codes[0]["system"] == "http://www.nlm.nih.gov/research/umls/rxnorm"
print(df_codes[mask_cas])



df_med = dct_med["Medications"]
df_med = rm_indices(df_med)
df_med_codes = getMedicationCodes(df_med, ";")
mask_atc = df_med_codes["system"] == "http://www.dimdi.de/atcgm2018"
print(df_med_codes[mask_atc]["code"].values)




#df_med.to_csv('Medications.csv', sep=";", decimal=".", encoding="utf-8", index=False, na_rep='')

