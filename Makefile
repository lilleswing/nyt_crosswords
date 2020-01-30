install: anaconda/LICENSE.txt
	bash devtools/install/install.sh

.PHONY: test
test:
	rm -f solve_times.csv solve_times.html
	python merge_crosswords.py test_data solve_times.csv

deploy:
	export PATH=`pwd`/anaconda/bin:${PATH}
	cp -r /home/leswing/Public/crossword/raw ./
	python merge_crosswords.py raw solve_times.csv
	scp solve_times.csv karl_leswing@karlleswing.com:/home/karl_leswing/karlleswing.com/misc
	scp solve_times.html karl_leswing@karlleswing.com:/home/karl_leswing/karlleswing.com/misc
