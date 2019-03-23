#!/bin/bash
for (( year = 1953; year < 1954;  year++ ))
do
    echo $year
    mv "$year"* "../year-wise/"
done