# Title     : main.R
# Objective : fhirton fhirckrar comparison
# Created by: tpeschel
# Created on: 19.07.20

devtools::install_github("POLAR-fhir/fhircrackr@remove-value-in-design")

library('fhircrackr')

endp <- "https://hapi.fhir.org/baseR4/"
#endp <- "https://vonk.fire.ly/R4/"
req  <- "Observation?code=http://loinc.org|85354-9&_include=Observation:patient&_include=Observation:encounter&_format=xml&_pretty=true&_count=500"
#    req <- "Observation?_include=Observation:patient&_include=Observation:encounter&_format=xml&_pretty=true&_count=500"

fsq <- paste_paths(endp, req)

design <- list(
  "Observations" = list(
    ".//Observation",
    list(
      "O.OID" = "./id/@value",
      "O.PID" = "./subject/reference/@value",
      "O.EID" = "./encounter/reference/@value",
      "DIA.VALUE" = "./component/code/coding/code[@value='8462-4']/../../../valueQuantity/value/@value",
      "DIA.UNIT" = "./component/code/coding/code[@value='8462-4']/../../../valueQuantity/unit/@value",
      "DIA.SYSTEM" = "./component/code/coding/code[@value='8462-4']/../system/@value",
      "SYS.VALUE" = "./component/code/coding/code[@value='8480-6']/../../../valueQuantity/value/@value",
      "SYS.UNIT" = "./component/code/coding/code[@value='8480-6']/../../../valueQuantity/unit/@value",
      "SYS.SYSTEM" = "./component/code/coding/code[@value='8480-6']/../system/@value",
      "DATE" = "./effectiveDateTime/@value"
    )
  ),
  "Encounters" = list(
    ".//Encounter",
    list(
      "E.EID" = "id/@value",
      "E.PID" = "subject/reference/@value",
      "START" = "period/start/@value",
      "END" = "period/end/@value"
    )
  ),
  "Patients" = list(
    ".//Patient",
    list(
      "P.PID" = "id/@value",
      "GVN.NAME" = "name/given/@value",
      "FAM.NAME" = "name/family/@value",
      "SEX" = "gender/@value",
      "DOB" = "birthDate/@value"
    )
  )
)

bundles <- fhir_search(fsq, verbose=2)

tables <- fhir_crack(bundles, design, sep = " ", add_indices = FALSE, verbose = 2)

#    tables['Observations']['O.PID'] = [re.sub("^.*/(\\w+$)", "\\1", p) for p in tables['Observations']['O.PID']]
#    tables['Encounters']['E.PID'] = [re.sub("^.*/(\\w+$)", "\\1", p) for p in tables['Encounters']['E.PID']]

#    tables['Total'] = pa.merge(tables['Observations'], tables['Patients'], left_on=['O.PID'], right_on=['P.PID'], how='left')
#    tables['Total'] = pa.merge(tables['Total'], tables['Encounters'], left_on=['O.PID'], right_on=['E.PID'], how='left')

#print(tables)

if (! dir.exists('csv'))
  dir.create( 'csv', recursive = T )

for (n in names(tables))
  write.table(tables[[n]], paste0("csv/", n, "_r.csv" ), na = "", sep = ";", dec = ".", row.names = F, quote = F )
