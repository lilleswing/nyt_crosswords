


install: anaconda/LICENSE.txt
	bash devtools/install/install.sh

.PHONY: test
test:
	rm -f solve_times.csv solve_times.html
	python merge_crosswords.py all_scores solve_times.csv
