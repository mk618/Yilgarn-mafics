#!/bin/bash

# make lookup table for all melting curves
# Katz-Shorttle melting curves for each Tp and dtop at 1km intervals
# example with depth range 0-100 km; bulk H20 = 0.02

Tp_range=`seq 1250 1700`
dtop_range=`seq 0 100`

rm Adiabats_Shorttle-0.02_0-100.dat 2>/dev/null
for Tp in $Tp_range; do

  awk '{FS=","}{if (FNR>1) print $1*32,$3}' melt_paths/PTF_${Tp}_0.02_b_Shorttle.csv > temp
  xmax=`gmt info -C temp | awk '{printf "%.0f\n", $2}'`
  gmt greenspline temp -R0/$xmax -St0.2 -D0 -I1 -Gmelt_paths/PTF_${Tp}_0.02_Shorttle_smooth.txt

  for dtop in $dtop_range; do

    awk '{if ($1>='$dtop' && $2>0) print $2}' melt_paths/PTF_${Tp}_0.02_Shorttle_smooth.txt | awk '{ORS=" ";}; !NF{ORS="\n"};1' | awk '{print '$Tp', '$dtop', $0}' >> Adiabats_Shorttle-0.02_0-100.dat

  done

done
