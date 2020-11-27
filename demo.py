from fhirton import *

bundles = load_bundle("medication_bsp.xml")

dct_med = fhir_ton(bundles, {'Medications': ('//Medication',)}, sep=";", bra=["<", ">"], verbose=3)
dct_ing = fhir_ton(bundles, {'Medications': ('//Medication/ingredient',)}, sep=";", bra=["<", ">"], verbose=3)



df_med = dct_med["Medications"]
df_med = rm_indices(df_med)
df_med_codes = getMedicationCodes(df_med, ";")
mask_atc = df_med_codes["system"] == "http://www.dimdi.de/atcgm2018"
print(df_med_codes[mask_atc])

df = dct_ing['Medications']
df = rm_indices(df)
df_codes = getMedicationIngredientCodes(df, ";", onlyAPI=True)
mask_cas = df_codes[0]["system"] == "http://www.cas.org/cas"
print(df_codes[0][mask_cas])