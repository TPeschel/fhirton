echo "first run fhircrackr solution..."
time Rscript main.R

echo "next run fhirton solution..."
time python3 main.py

echo "Compare results in directory csv!"