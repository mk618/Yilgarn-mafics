#!/bin/bash

#####-------------------------------------------------------------------------------------#####
# filter Australian mafic compilation by a number of geographical and geochemical filters     #
# to select most primitive samples, least affected by fractionation or crustal assimilation   #
# Marthe Klöcking 2025                                                                        #
#####-------------------------------------------------------------------------------------#####

data_in="2025-xxx_Kloecking-et-al_compilation.csv"
data_out="Australia_mafic-compilation_Yilgarn_filtered.csv"
data_rej="Australia_mafic-compilation_Yilgarn_rejected.csv"


#####----------------------------------------------------------------------#####

### ASSIGN COLUMN NUMBERS FROM INPUT DATAFILE FOR COLUMNS OF INTEREST
#SiO2_col=`awk 'BEGIN{FS=","}{for(fn=1;fn<=NF;fn++) {if ($fn=="SiO2 [wt%]") print fn}}' $data_in`
#MgO_col=`awk 'BEGIN{FS=","}{for(fn=1;fn<=NF;fn++) {if ($fn=="MgO [wt%]") print fn}}' $data_in`
SiO2_col=`awk 'BEGIN{FS=","}{for(fn=1;fn<=NF;fn++) {if ($fn=="SiO2 [wt%] norm-anh") print fn}}' $data_in`
MgO_col=`awk 'BEGIN{FS=","}{for(fn=1;fn<=NF;fn++) {if ($fn=="MgO [wt%] norm-anh") print fn}}' $data_in`

Eu_col=`awk 'BEGIN{FS=","}{for(fn=1;fn<=NF;fn++) {if ($fn=="Eu [ppm]") print fn}}' $data_in`
Sm_col=`awk 'BEGIN{FS=","}{for(fn=1;fn<=NF;fn++) {if ($fn=="Sm [ppm]") print fn}}' $data_in`
Gd_col=`awk 'BEGIN{FS=","}{for(fn=1;fn<=NF;fn++) {if ($fn=="Gd [ppm]") print fn}}' $data_in`
Pr_col=`awk 'BEGIN{FS=","}{for(fn=1;fn<=NF;fn++) {if ($fn=="Pr [ppm]") print fn}}' $data_in`
Pb_col=`awk 'BEGIN{FS=","}{for(fn=1;fn<=NF;fn++) {if ($fn=="Pb [ppm]") print fn}}' $data_in`
Sr_col=`awk 'BEGIN{FS=","}{for(fn=1;fn<=NF;fn++) {if ($fn=="Sr [ppm]") print fn}}' $data_in`
Nd_col=`awk 'BEGIN{FS=","}{for(fn=1;fn<=NF;fn++) {if ($fn=="Nd [ppm]") print fn}}' $data_in`
Nb_col=`awk 'BEGIN{FS=","}{for(fn=1;fn<=NF;fn++) {if ($fn=="Nb [ppm]") print fn}}' $data_in`
U_col=`awk 'BEGIN{FS=","}{for(fn=1;fn<=NF;fn++) {if ($fn=="U [ppm]") print fn}}' $data_in`
Ta_col=`awk 'BEGIN{FS=","}{for(fn=1;fn<=NF;fn++) {if ($fn=="Ta [ppm]") print fn}}' $data_in`

Lat_col=`awk 'BEGIN{FS=","}{for(fn=1;fn<=NF;fn++) {if ($fn=="LATITUDE") print fn}}' $data_in`
Lon_col=`awk 'BEGIN{FS=","}{for(fn=1;fn<=NF;fn++) {if ($fn=="LONGITUDE") print fn}}' $data_in`
#####----------------------------------------------------------------------#####


### COPY COLUMN HEADERS INTO THE TWO OUTPUT FILES
awk 'BEGIN{FS=","; OFS=","}NR==1{print $0}' $data_in > $data_out
#awk 'BEGIN{FS=","; OFS=","}NR==1{print $0}' $data_in > $data_rej


### FILTER BY:
## geographical extent of the Yilgarn craton: $5=="WA" && $'$Lat_col'<=-27 && $'$Lon_col'<=125
## basaltic major element compositions: $'$SiO2_col'>=41 && $'$SiO2_col'<=53 && MgO>=7 && MgO<=13
## no significant Eu anomaly: Eu/Eu*<=1.1 && Eu/Eu*>=0.9
## no significant Sr anomaly: Sr/Sr*<=1.25 && Sr/Sr*>=0.75
## no positive Pb anomaly: Pb/Pb*<=1.1
## mantle-like Nb/U ratios: $'$Nb_col'/$'$U_col'>=30
## remove one sample with anomalously high Ta: $'$Ta_col'<=0.5
awk 'BEGIN{FS=","; OFS=","}{if (FNR>1 && $5=="WA" && $'$Lat_col'<=-27 && $'$Lon_col'<=125 && $'$SiO2_col'>=41 && $'$SiO2_col'<=53 && $'$Sm_col'!="" && $'$Gd_col'!="" && $'$Eu_col'!="" && $'$Nd_col'!="" && $'$Pr_col'!="" && $'$U_col'!="" && $'$U_col'!~/</ && $'$Gd_col'!~/</ && $'$Pr_col'>0 && $'$MgO_col'>=7 && $'$MgO_col'<=13 && $'$Ta_col'<=0.5 && ($'$Eu_col'/0.154)/(($'$Sm_col'/0.406)*($'$Gd_col'/0.544))^0.5>=0.9 && ($'$Eu_col'/0.154)/(($'$Sm_col'/0.406)*($'$Gd_col'/0.544))^0.5<=1.1 && ($'$Pb_col'/0.15)/(($'$Nd_col'/1.25)*($'$Pr_col'/0.254))^0.5<=1.1 && ($'$Sr_col'/19.9)/(($'$Nd_col'/1.25)*($'$Pr_col'/0.254))^0.5<=1.25 && ($'$Sr_col'/19.9)/(($'$Nd_col'/1.25)*($'$Pr_col'/0.254))^0.5>=0.75 && $'$U_col'>0 && $'$Nb_col'/$'$U_col'>=30) print $0}' $data_in >> $data_out

### ALL OTHER SAMPLES GO INTO THE REJECT FILE
#awk 'BEGIN{FS=","; OFS=","}{if (FNR>1 && $5=="WA" && $'$Lat_col'<=-27 && $'$Lon_col'<=125 && $'$Sm_col'!="" && $'$Gd_col'!="" && $'$Nd_col'!="" && $'$Pr_col'!="" && $'$Gd_col'!~/</ && $'$U_col'!~/</ && $'$Pr_col'>0 && $'$U_col'>0 && $'$U_col'!="") print $0}' $data_in | awk 'BEGIN{FS=","; OFS=","}{if ($'$MgO_col'<7 || $'$MgO_col'>13 || $'$Ta_col'>0.5 || $'$SiO2_col'<41 || $'$SiO2_col'>53 || ($'$Eu_col'/0.154)/(($'$Sm_col'/0.406)*($'$Gd_col'/0.544))^0.5<0.9 || ($'$Eu_col'/0.154)/(($'$Sm_col'/0.406)*($'$Gd_col'/0.544))^0.5>1.1 || ($'$Pb_col'/0.15)/(($'$Nd_col'/1.25)*($'$Pr_col'/0.254))^0.5>1.1 || ($'$Sr_col'/19.9)/(($'$Nd_col'/1.25)*($'$Pr_col'/0.254))^0.5>1.25 || ($'$Sr_col'/19.9)/(($'$Nd_col'/1.25)*($'$Pr_col'/0.254))^0.5<0.75 || $'$Nb_col'/$'$U_col'<30) print $0}' >> $data_rej
#awk 'BEGIN{FS=","; OFS=","}{if (FNR>1) print $0}' $data_in | awk 'BEGIN{FS=","; OFS=","}{if ($5!="WA" || $'$Lat_col'>-27 || $'$Lon_col'>125 || $'$Sm_col'=="" || $'$Gd_col'=="" || $'$Gd_col'~/</ || $'$Pr_col'=="" || $'$Nd_col'=="" || $'$U_col'=="" || $'$U_col'<=0 || $'$U_col'~/</ || $'$Pr_col'<=0) print $0}' >> $data_rej
