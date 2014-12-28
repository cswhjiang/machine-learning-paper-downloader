#!/bin/bash

rm -f icml_all.bib
for i in {2003..2014}
do
	cat "icml_$i/icml_$i.bib" >> "icml_all.bib"
done
