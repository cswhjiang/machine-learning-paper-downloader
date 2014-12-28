#!/bin/bash

for i in {1987..2014}
do
  echo "NIPS$i/*.bib"
 # ls "NIPS$i"/*.bib
  cat "NIPS$i"/*.bib > "NIPS$i.bib"
done

cat NIPS*.bib > nipsAll.bib
rm NIPS*.bib
