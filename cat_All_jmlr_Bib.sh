#!/bin/bash

rm jmlr_all.bib
for i in {1..15}
do
	cat "Volume_$i/jmlr_$i.bib" >> "jmlr_all.bib"
done