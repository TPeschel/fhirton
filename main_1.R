# Title     : main.R
# Objective : fhirton fhirckrar comparison
# Created by: tpeschel
# Created on: 19.07.20

devtools::install_github("POLAR-fhir/fhircrackr", quiet = T)
#install.packages( 'fhircrackr' )
library('dplyr')
library('fhircrackr')

# fhir endpoint
endp <- "https://hapi.fhir.org/baseR4/"

# fhir request
req  <- "Observation?code=http://loinc.org|85354-9&_include=Observation:patient&_include=Observation:encounter&_format=xml&_pretty=true&_count=500"
#req <- "Observation?_include=Observation:patient&_include=Observation:encounter&_format=xml&_pretty=true&_count=500"

fsq <- paste0(endp, req)

# designs 1, 1, 1
designs <- list(
  "Observations" = list(
    ".//Observation",
    list(
      "O.OID" = "./id",
      "O.PID" = "./subject/reference",
      "O.EID" = "./encounter/reference",
      "DIA.VALUE" = "./component/code/coding/code[@value='8462-4']/../../../valueQuantity/value",
      "DIA.UNIT" = "./component/code/coding/code[@value='8462-4']/../../../valueQuantity/unit",
      "DIA.SYSTEM" = "./component/code/coding/code[@value='8462-4']/../system",
      "SYS.VALUE" = "./component/code/coding/code[@value='8480-6']/../../../valueQuantity/value",
      "SYS.UNIT" = "./component/code/coding/code[@value='8480-6']/../../../valueQuantity/unit",
      "SYS.SYSTEM" = "./component/code/coding/code[@value='8480-6']/../system",
      "DATE" = "./effectiveDateTime"
    )
  ),
  "Encounters" = list(
    ".//Encounter",
    list(
      "E.EID" = "./id",
      "E.PID" = "./subject/reference",
      "START" = "./period/start",
      "END" = "./period/end"
    )
  ),
  "Patients" = list(
    ".//Patient",
    list(
      "P.PID" = "./id",
      "GVN.NAME" = "./name/given",
      "FAM.NAME" = "./name/family",
      "SEX" = "./gender",
      "DOB" = "./birthDate"
    )
  )
)

# download fhir bundles and babble a lot
bundles <- fhir_search(fsq, verbose=2, max_bundles=5)

# crack/flatten the downloaded bundles to tables via designs and babble a lot
tables <- fhir_crack(bundles, designs, sep = " ", brackets = c('[', ']'), verbose = 3)

# delete indices for ids
tables[['Observations']] <- fhir_rm_indices(tables[['Observations']], brackets = c('[', ']'), columns = c( 'O.OID', 'O.EID', 'O.PID'))
tables[['Encounters']] <- fhir_rm_indices(tables[['Encounters']], brackets = c('[', ']'), columns = c( 'E.EID', 'E.PID'))
tables[['Patients']] <- fhir_rm_indices(tables[['Patients']], brackets = c('[', ']'), columns = c( 'P.PID'))

# delete prefixes for ids
tables[['Observations']][['O.PID']] <- sub("^.*/(\\w+$)", "\\1", tables[['Observations']][['O.PID']])
tables[['Observations']][['O.EID']] <- sub("^.*/(\\w+$)", "\\1", tables[['Observations']][['O.EID']])
tables[['Encounters']][['E.PID']] <- sub("^.*/(\\w+$)", "\\1", tables[['Encounters']][['E.PID']])

# merge all tables
tables[['Total']] <- merge(tables[['Observations']], tables[['Encounters']], by.x=c('O.EID', 'O.PID'), by.y=c('E.EID', 'E.PID'), all=FALSE)
tables[['Total']] <- merge(tables[['Total']], tables[['Patients']], by.x='O.PID', by.y='P.PID', all=FALSE)

# select some interesting columns
tables[['Total']] <- tables[['Total']][, c(
  "O.PID", "O.OID", "O.EID",
  "GVN.NAME", "FAM.NAME",
  "DOB", "SEX",
  "DIA.VALUE", "DIA.UNIT", "DIA.SYSTEM",
  "SYS.VALUE", "SYS.UNIT", "SYS.SYSTEM",
  "DATE", "START", "END")
]

# sort table columns
tables[['Total']] <- tables[['Total']] %>% arrange(O.PID, O.OID, O.EID, START)

# create dir if not exists
if (! dir.exists('csv1'))
  dir.create( 'csv1', recursive = T )

# save tables as csv files
for (n in names(tables))
  write.table(tables[[n]], paste0("csv1/", n, "_r.csv" ), na = "", sep = ";", dec = ".", row.names = F, quote = F )
