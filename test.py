from fhirton import fhir_search, fhir_melt, fhir_ton, load_bundle

#kann wechselseitig auskommentiert werden um eine Medication- oder Patient-Ressource zu testen + weiter unten!
#restype = "Medication"
#bundles = fhir_search("https://mii-agiop-3p.life.uni-leipzig.de/fhir/Medication?_id=UKB001-M-762044846&_format=xml")
# bundles = load_bundle("medication_bsp.xml")

restype = "Patient"
bundles = load_bundle("patient_bsp.xml")

dct = fhir_ton([bundles], {restype: ("//" + restype,)}, sep=";", verbose=3)
df = dct[restype]
print("-------------------NON molten dataframe-------------------------")
print(df)

#!!!hier auch ggf. Kommentar wechseln!!!
#df_molten = fhir_melt(df, ["code.coding.system", "code.coding.code"], sep=";")
df_molten = fhir_melt(df, ["address.country", "address.city", "birthDate", "id"], sep=";")

print("-------------------molten dataframe-----------------------------")
print(df_molten)