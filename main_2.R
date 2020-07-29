# Title     : main.R
# Objective : fhirton fhirckrar comparison
# Created by: tpeschel
# Created on: 19.07.20

install.packages( "fhircrackr" )

library('dplyr')
library('fhircrackr')

endp <- "https://hapi.fhir.org/baseR4/"
#req  <- "Observation?code=http://loinc.org|85354-9&_include=Observation:patient&_include=Observation:encounter&_format=xml&_pretty=true&_count=500"
req <- "Observation?_include=Observation:patient&_include=Observation:encounter&_format=xml&_pretty=true&_count=500"
#req <- "Observation?_include=Observation:patient&_include=Observation:encounter&_format=xml&_pretty=true&_count=500"

fsq <- paste0(endp, req)

design <- list(
  "Observations" = list(
    ".//Observation",
    ".//*"
  ),
  "Encounters" = list(
    ".//Encounter",
    ".//*"
  ),
  "Patients" = list(
    ".//Patient",
    ".//*"
  )
)

bundles <- fhir_search(fsq, max_bundles = 3, verbose=2)

tables <- fhir_crack(bundles, design, sep = " ", add_indices = FALSE, verbose = 2)

tables <- lapply(
  tables,
  function(tbl) {
    tbl[, sort(names(tbl))]
  }
)

#tables[['Observations']][['O.PID']] <- sub("^.*/(\\w+$)", "\\1", tables[['Observations']][['O.PID']])
#tables[['Observations']][['O.EID']] <- sub("^.*/(\\w+$)", "\\1", tables[['Observations']][['O.EID']])
#tables[['Encounters']][['E.PID']] <- sub("^.*/(\\w+$)", "\\1", tables[['Encounters']][['E.PID']])
#
#
#tables[['Total']] <- merge(tables[['Observations']], tables[['Patients']], by.x='O.PID', by.y='P.PID', all=FALSE)
#tables[['Total']] <- merge(tables[['Total']], tables[['Encounters']], by.x='O.PID', by.y='E.PID', all=FALSE)
#
#tables[['Total']] <- tables[['Total']][, c(
#  "O.PID", "O.OID", "O.EID",
#  "GVN.NAME", "FAM.NAME",
#  "DOB", "SEX",
#  "DIA.VALUE", "DIA.UNIT", "DIA.SYSTEM",
#  "SYS.VALUE", "SYS.UNIT", "SYS.SYSTEM",
#  "DATE", "START", "END")
#]
#
#tables[['Total']] <- tables[['Total']] %>% arrange(O.PID, O.OID, O.EID, START)

if (! dir.exists('csv'))
  dir.create( 'csv', recursive = T )

for (n in names(tables))
  write.table(tables[[n]], paste0("csv/", n, "_r.csv" ), na = "", sep = ";", dec = ".", row.names = F, quote = F )
