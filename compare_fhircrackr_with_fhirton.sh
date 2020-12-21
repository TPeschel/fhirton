echo "first run fhircrackr solution 1..."
time Rscript main_1.R

echo "next run fhirton solution 1..."
time python3 main_1.py

echo "first run fhircrackr solution 2..."
time Rscript main_2.R

echo "next run fhirton solution 2..."
time python3 main_2.py

echo "next run fhirton solution 3..."
time python3 main_3.py

echo "Compare results in directory csv!"