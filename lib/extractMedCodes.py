import pandas as PA
from ..fhirton import rm_indices

def getMedicationIngredientCodes(dct_ing, sep=";", onlyAPI=False):
    """Extract ingredient specific codes (e.g. ASK) from given dictionary

    Args:
        dct_ing: dictionary, derived from a flattened FHIR-medication resource via fhir_ton, e.g.: dct_ing = fhir_ton(bundles, {'Medications': ('//Medication/ingredient',)}, sep, bra, verbose))
        sep: character to seperate different codes, default: ";"
        onlyAPI: if true -> returns only active pharmaceutical ingredients
        
    Returns:
        list of Pandas dataframes, one dataframe for each ingredient: [ DataFrame(index|system|code|display) ]
    """

    df = dct_ing['Medications']
    df = rm_indices(df)

    df_list = []
    if onlyAPI:
        mask = df["isActive"] == "true"
        df = df[mask]
    
    for index, row in df.iterrows():
        systems = row["itemCodeableConcept.coding.system"]
        sys_split = systems.split(sep)
    
        codes = row["itemCodeableConcept.coding.code"]
        codes_split = codes.split(sep)

        display = row["itemCodeableConcept.coding.display"]
        display_split = display.split(sep)

        substance_df = PA.DataFrame([sys_split, codes_split, display_split]).T
        substance_df.columns = ["system", "code", "display"]
        df_list.append(substance_df)

    return df_list
    
def getMedicationCodes(dct_med, sep=";"):
    """Extract medication specific codes (e.g. ATC) from given dictionary

    Args:
        dct_med: dictionary, derived from a flattened FHIR-medication resource via fhir_ton, e.g.: dct_med = fhir_ton(bundles, {'Medications': ('//Medication',)}, sep, bra, verbose)
        sep: character to seperate different codes, default: ";"
        
    Returns:
        Pandas dataframe: index|system|code
    """
    df_med = dct_med["Medications"]
    df = rm_indices(df_med)

    df = df[["code.coding.code", "code.coding.system"]]

    systems = df["code.coding.system"]
    sys_split = systems[0].split(sep)
    
    codes = df["code.coding.code"]
    codes_split = codes[0].split(sep)

    medic_df = PA.DataFrame([sys_split, codes_split]).T
    medic_df.columns = ["system", "code"]

    return medic_df