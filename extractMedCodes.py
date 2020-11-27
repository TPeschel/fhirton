import pandas as PA

def getMedicationIngredientCodes(df, sep, onlyAPI=False):
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
    
def getMedicationCodes(df, sep):
    df = df[["code.coding.code", "code.coding.system"]]

    systems = df["code.coding.system"]
    sys_split = systems[0].split(sep)
    
    codes = df["code.coding.code"]
    codes_split = codes[0].split(sep)

    medic_df = PA.DataFrame([sys_split, codes_split]).T
    medic_df.columns = ["system", "code"]

    return medic_df