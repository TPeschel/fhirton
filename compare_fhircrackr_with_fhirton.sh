echo "first run fhircrackr solution..."
time Rscript main_2.R

echo "next run fhirton solution..."
time python3 main_2.py

echo "Compare results in directory csv!"