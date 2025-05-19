import pyMelt as pyMelt
import numpy as np
import pandas as pd


lz = pyMelt.lithologies.katz.lherzolite(CP=1187.0,DeltaS=407.0,alphas=30.0)    # Shorttle et al. (2014)

mantle_dry = pyMelt.mantle([lz],[1],['Lz'])

#bulk_H2O = 0.028    # for PM, norm=4, Ce=1.40
#bulk_H2O = 0.014    # for DMM, norm=6, Ce=0.722
bulk_H2O = 0.020    # for epsil=5, Ce=1.014
#bulk_H2O = 0.023    # for epsil=3, Ce=1.154


# wet, batch melting
hlz005_b = pyMelt.hydrousLithology(lz, bulk_H2O, continuous=False)
hm005_b = pyMelt.mantle([hlz005_b], [1.0])

morb_wet_b_array = []
t_array = list(range(1250,1751))

for t in t_array:
    print(t)
    column_wet_b = hm005_b.adiabaticMelt(t)
    results_wet_b = pd.DataFrame()
    results_wet_b['P'] = column_wet_b.P
    results_wet_b['T'] = column_wet_b.T
    results_wet_b['F_total'] = column_wet_b.F
    results_wet_b.to_csv('melt_paths/PTF_'+str(t)+'_'+str(bulk_H2O)+'_b_Shorttle.csv',index=False)

