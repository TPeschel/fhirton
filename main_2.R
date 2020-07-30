# Title     : main.R
# Objective : fhirton fhirckrar comparison
# Created by: tpeschel
# Created on: 19.07.20

devtools::install_github("POLAR-fhir/fhircrackr", quiet = T)
#install.packages( "fhircrackr" )
library('dplyr')
library('fhircrackr')

# fhir endpoint
endp <- "https://hapi.fhir.org/baseR4/"

# fhir request
req  <- paste0(
  "Observation?",
  "code=http://loinc.org|85354-9&",
  "_include=Observation:patient&",
  "_include=Observation:encounter&",
  "_format=xml&_pretty=true&_count=500" )

#req <- "Observation?_include=Observation:patient&_include=Observation:encounter&_format=xml&_pretty=true&_count=500"
#req <- "Observation?_include=Observation:patient&_include=Observation:encounter&_format=xml&_pretty=true&_count=500"

fsq <- paste_paths(endp, req)

# designs 3, 2, 3
design <- list(
  "Observations" = list(
    ".//Observation"
  ),
  "Encounters" = list(
    ".//Encounter",
    ".//*"
  ),
  "Patients" = list(
    ".//Patient"
  )
)

# download fhir bundles and babble a lot
bundles <- fhir_search(fsq, max_bundles = 3, verbose=2)

# crack/flatten the downloaded bundles to tables via designs
# use space as separator and [] as brackets for indexing and babble a lot
tables <- fhir_crack(bundles, design, sep = " ", brackets = c('[', ']'), verbose = 2)

# sort column names
tables <- lapply(
  tables,
  function(tbl) {
    tbl[, sort(names(tbl))]
  }
)

# create dir if not exist
if (! dir.exists('csv2'))
  dir.create( 'csv2', recursive = T )

# write tables as csv files
for (n in names(tables))
  write.table(tables[[n]], paste0("csv2/", n, "_r.csv" ), na = "", sep = ";", dec = ".", row.names = F, quote = F )
