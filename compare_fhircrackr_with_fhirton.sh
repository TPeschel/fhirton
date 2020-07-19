echo "first run fhircrackr solution...\n"
Rscript main.R

echo "\nnext run fhirton solution...\n"
python3 main.py

echo "Compare results in directory csv!"