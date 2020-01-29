#!/bin/bash

echo "running first part of program:"
echo "- tfidf frequency per-year"
echo "- clustering"
echo "- pmi per-year"

python3 mcwatera_fp.py > mcwatera_fp_results.txt

echo "results of part 1 written to mcwatera_fp_results.txt"
