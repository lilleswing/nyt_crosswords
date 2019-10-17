#!/bin/bash
rm -rf all_scores
scp -r tentacruel.bb.schrodinger.com:/home/leswing/Public/crossword/raw/ all_scores
python merge_crosswords.py all_scores test/out.csv
