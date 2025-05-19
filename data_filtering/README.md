# Data Filtering & Fractionation Correction

## Contents
- `filtering_Yilgarn-mafics.sh`: shell script for filtering the source dataset (DATA CITATION) by a number of geographical and geochemical filters
- `Australia_mafic-compilation_Yilgarn_filtered.csv`: output of `filtering_Yilgarn-mafics.sh`
- `Results_15kbar_cpx93fo93_Langmuir_traces-O.xlsx`: output of Petrolog3 fractionation correction on `Australia_mafic-compilation_Yilgarn_filtered.csv`; includes all calculation steps and model parameters
- `Results_15kbar_cpx93fo93_Langmuir_traces-O.csv`: post-processed version of final melt compositions for each sample calculated in `Results_15kbar_cpx93fo93_Langmuir_traces-O.xlsx`; includes re-calculated trace element concentrations

## Step 1: Filtering

### Data file pre-treatment
- Download a copy of the full data compilation from [DATA CITATION].
- Save main data sheet in CSV format.


### Run filtering script
- Make sure the `data_in` filename matches your CSV file from the previous step 
- On Linux or MacOS, run `./filtering_Yilgarn-mafics.sh` in a terminal
- Output: `Australia_mafic-compilation_Yilgarn_filtered.csv` (and optionally also `_rejected.csv`)

This shell script filters for samples that match:
- the geographical extent of the Yilgarn craton: Latitude <= -27 and Longitude <= 125
- basaltic major element compositions: 41 wt% <= SiO2 <= 53 wt% and 7 wt% <= MgO <= 13 wt%
- no significant Eu anomaly: 0.9 <= Eu/Eu* <= 1.1
- no significant Sr anomaly: 0.75 <= Sr/Sr* <= 1.25
- no positive Pb anomaly: Pb/Pb* <= 1.1
- mantle-like Nb/U ratios: Nb/U >= 30

All samples/analyses that pass the filtering are from the WACHEM database:

Geological Survey of Western Australia (2021). WACHEM database. https://www.wa.gov.au/service/natural-resources/mineral-resources/access-geochemistry-geochem-extract (accessed 2019-2021).



## Step 2: Fractionation Correction

Input: `Australia_mafic-compilation_Yilgarn_filtered.csv`
Output: `Results_15kbar_cpx93fo93_Langmuir_traces-O.xlsx`

Using the Petrolog3 software of [Danyushevsky & Plechov (2011)](http://doi.org/10.1029/2011GC003516) available for free download [here](https://www.fshomepage.com/filestore/Ptl3/Petrolog3.html). User manual available at the same location. 

### Reverse Crystallisation

Calculation parameters:
- Mineral-melt models:
    - olivine: Langmuir et al., 1992
    - clinopyroxene: Langmuir et al., 1992
- Kd model for olivine: Sobolev & Danyushevsky 1994
- Trace element partition cofficients (entered manually): [Oliveira et al. (2020)](http://doi.org/10.1093/petrology/egaa067)
- Initial P: 15 kbar (keep constant)
- Parameters for exclusion: clinopyroxene at Mg# = 93
- Conditions to stop calculations: olivine Fo = 93
- default settings for oxidation state, density, viscosity and calculation step

### Post-processing
Only REEs (excluding Tm) were assigned cpx-melt partition coefficients from Oliveira et al. (2020). 
Due to the low precision of the Petrolog3 output (one decimal place for trace elements), all other trace elements were re-calculated separately by mass balance from the observed concentrations and the total predicted amount of olivine and clinopyroxene addition (suffix `_calc`).
