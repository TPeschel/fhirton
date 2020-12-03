from fhirton import *
from extractMedCodes import *

bundles = load_bundle("medication_bsp.xml")

dct_med = fhir_ton(bundles, {'Medications': ('//Medication',)}, sep=";", bra=["<", ">"], verbose=3)
dct_ing = fhir_ton(bundles, {'Medications': ('//Medication/ingredient',)}, sep=";", bra=["<", ">"], verbose=3)

df_med_codes = getMedicationCodes(dct_med, ";")
mask_atc = df_med_codes["system"] == "http://www.dimdi.de/atcgm2018"
print(df_med_codes[mask_atc])

df_codes = getMedicationIngredientCodes(dct_ing, ";", onlyAPI=True)
mask_cas = df_codes[0]["system"] == "http://www.cas.org/cas"
print(df_codes[0][mask_cas])