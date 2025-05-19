import numpy as np
import pandas as pd

##############################
# Functions

def calc_misfit(obs_rees,calc_rees,sigma):
    """
    Calculate misfit (sum of squares difference) between forward calculated
    and observed REE compositions.
    Observed compositions are assigned 5% analytical uncertainty.

    INPUT:
    obs_rees: list of floats (1x14)
    calc_rees: array of floats (Nx14)

    OUTPUT:
    misfit: list of floats (Nx1)
    """

    # sig = sigma * obs_rees
    sig = sigma
    misfit = np.sqrt(np.sum( (calc_rees-obs_rees)**2, axis=1) / sum(sig**2) )

    return (misfit)



##############################
# Main program

inputfile="../data_filtering/Results_15kbar_cpx93fo93_Langmuir_traces-O.csv"

outfile = 'invmel_misfit_best.dat'


### READ IN REES FROM FORWARD MODELS AT VARYING TP AND DTOP

filename = "INVMEL_Katz-Shorttle_0-100/0.023_epsil3/forward_models.dat"
#filename = "INVMEL_Katz-Shorttle_0-100/0.020_epsil5/forward_models.dat"

H2O_bulk = 0.023


df2 = pd.read_csv(filename, sep="\s+|\t| ", engine="python")
df2.dropna(inplace=True)

### SET POTENTIAL TEMPERATURE BOUNDS (optional)
df2 = df2[df2.Temp >= 1350]
df2 = df2[df2.Temp <= 1600]

calc_rees = df2.loc[:,[ 'La','Ce','Pr','Nd','Sm','Eu','Gd','Tb','Dy','Ho','Er','Yb','Lu' ] ]
calc_rees2 = np.array(calc_rees, dtype=float)

calc_rees_all = df2.loc[:,[ 'La','Ce','Pr','Nd','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb','Lu' ] ]
calc_rees2_all = np.array(calc_rees_all, dtype=float)

calc_traces = df2.loc[:,[ 'Cs', 'Rb', 'Ba', 'Th', 'U', 'Ta', 'Nb', 'Sr', 'Zr', 'Hf', 'Ti', 'Y' ] ]
calc_traces2 = np.array(calc_traces, dtype=float)


### ALTERNATIVELY, JUST USE 3 REES FOR MISFIT CALCULATION
#calc_3rees = df2.loc[:,[ 'La','Gd','Yb' ] ]
calc_3rees = df2.loc[:,[ 'La','Nd','Dy','Yb' ] ]
calc_3rees2 = np.array(calc_3rees, dtype=float)

### CONDITIONS OF FORWARD MODELS
conds = df2.loc[:,['Temp','Dtop']]
conds2 = np.array(conds)


output2 = []
output2.append(['rms', 'Tp_best', 'Tp_min', 'Tp_max', 'dtop_best', 'dtop_min', 'dtop_max', 'rms_13', 'Tp_best_13', 'Tp_min_13', 'Tp_max_13', 'dtop_best_13', 'dtop_min_13', 'dtop_max_13'])

output3 = []
output3.append(['rms', 'Tp_best', 'Tp_min', 'Tp_max', 'dtop_best', 'dtop_min', 'dtop_max'])


### READ INPUT DATA: SAMPLE COMPOSITIONS

df_input = pd.read_csv(inputfile, engine="python")
input_rees = df_input.loc[:,[ 'La_melt','Ce_melt','Pr_melt','Nd_melt','Sm_melt','Eu_melt','Gd_melt','Tb_melt','Dy_melt','Ho_melt','Er_melt','Tm_calc','Yb_melt','Lu_melt' ] ]

avg_input = input_rees.mean(axis=0)
sigma_input = 3*input_rees.std(axis=0)
avg_rees2 = np.array(avg_input)
sigma_rees2 = np.array(sigma_input)

input_3rees = df_input.loc[:,[ 'La_melt','Nd_melt','Dy_melt','Yb_melt' ] ]
avg_input3 = input_3rees.mean(axis=0)
sigma_input3 = 3*input_3rees.std(axis=0)
avg_3rees2 = np.array(avg_input3)
sigma_3rees2 = np.array(sigma_input3)

input_traces = df_input.loc[:,[ 'Cs_melt', 'Rb_melt', 'Ba_melt', 'Th_calc', 'U_calc', 'Ta_calc', 'Nb_calc', 'Sr_calc', 'Zr_calc', 'Hf_calc', 'Ti_calc', 'Y_calc' ] ]
avg_traces = input_traces.mean(axis=0)
sigma_traces = 3*input_traces.std(axis=0)
avg_traces2 = np.array(avg_traces)
sigma_traces2 = np.array(sigma_traces)



### CALCULATE MISFIT IN MANY WAYS
misfit_all = calc_misfit(avg_rees2,calc_rees2_all,sigma_rees2)

misfit_3 = calc_misfit(avg_3rees2,calc_3rees2,sigma_3rees2)

### MERGE FORWARD MODEL CONDITIONS AND VARIOUS MISFITS INTO ONE FILE PER SAMPLE
output = np.column_stack((conds2,misfit_3, misfit_all))

#################################################################################################################

### FIND MINIMIUM MISFIT AND ACCEPTABLE RANGE OF TP AND Dtop
rms_min = np.min(output[:,2])
best_all =  output[output[:,2]==rms_min]

Tp_best = best_all[0,0]
dtop_best = best_all[0,1]

best_rees = calc_rees2_all[output[:,2]==rms_min]
best_traces = calc_traces2[output[:,2]==rms_min]

# minmax_all = output[np.where(output[:,2]<=1)]
minmax_all = output[np.where(output[:,2]<=(2))]

# ADD IF STATEMENT TO ACCOUNT FOR MIN MISFIT >1
if rms_min <= 2.5:
    Tp_max = np.max(minmax_all[:,0])
    dtop_max = np.max(minmax_all[:,1])
    Tp_min = np.min(minmax_all[:,0])
    dtop_min = np.min(minmax_all[:,1])

    good_rees = calc_rees2_all[np.where(output[:,2]<=(2))]
    good_traces = calc_traces2[np.where(output[:,2]<=(2))]
else:
    Tp_max = np.nan
    dtop_max = np.nan
    Tp_min = np.nan
    dtop_min = np.nan

    good_rees = best_rees * np.nan
    good_traces = best_traces * np.nan
##### END IF STATEMENT

##########################################################
## SAME FOR 13REE MISFIT

rms_13min = np.min(output[:,3])
best_13all =  output[output[:,3]==rms_13min]

if np.isnan(rms_13min) == False:
    Tp_13best = best_13all[0,0]
    dtop_13best = best_13all[0,1]
    best_13rees = calc_rees2_all[output[:,3]==rms_13min]
    best_13traces = calc_traces2[output[:,3]==rms_13min]
else:
    Tp_13best = np.nan
    dtop_13best = np.nan
    best_13rees = best_rees * np.nan
    best_13traces = best_traces * np.nan

minmax_13all = output[np.where(output[:,3]<=(2))]

# ADD IF STATEMENT TO ACCOUNT FOR MIN MISFIT >1
if rms_13min <= 2.5 and np.isnan(rms_13min) == False:
    minmax_13all = output[np.where(output[:,3]<=2.5)]
    Tp_13max = np.max(minmax_13all[:,0])
    dtop_13max = np.max(minmax_13all[:,1])
    Tp_13min = np.min(minmax_13all[:,0])
    dtop_13min = np.min(minmax_13all[:,1])

    good_13rees = calc_rees2_all[np.where(output[:,3]<=(2))]
    good_13traces = calc_traces2[np.where(output[:,3]<=(2))]
else:
    Tp_13max = np.nan
    dtop_13max = np.nan
    Tp_13min = np.nan
    dtop_13min = np.nan

    good_13rees = best_rees * np.nan
    good_13traces = best_traces * np.nan
##### END IF STATEMENT

output_sum = [rms_min, Tp_best, Tp_min, Tp_max, dtop_best, dtop_min, dtop_max, rms_13min, Tp_13best, Tp_13min, Tp_13max, dtop_13best, dtop_13min, dtop_13max]

if (rms_min <= rms_13min) or (np.isnan(rms_13min)):
    rms_min_fav = rms_min
    Tp_best_fav = Tp_best
    Tp_min_fav = Tp_min
    Tp_max_fav = Tp_max
    dtop_best_fav = dtop_best
    dtop_min_fav = dtop_min
    dtop_max_fav = dtop_max
    best_rees_fav = best_rees
    good_rees_fav = good_rees
    best_traces_fav = best_traces
    good_traces_fav = good_traces
else:
    rms_min_fav = rms_13min
    Tp_best_fav = Tp_13best
    Tp_min_fav = Tp_13min
    Tp_max_fav = Tp_13max
    dtop_best_fav = dtop_13best
    dtop_min_fav = dtop_13min
    dtop_max_fav = dtop_13max
    best_rees_fav = best_13rees
    good_rees_fav = good_13rees
    best_traces_fav = best_13traces
    good_traces_fav = good_13traces

output_sum2 = [rms_min_fav, Tp_best_fav, Tp_min_fav, Tp_max_fav, dtop_best_fav, dtop_min_fav, dtop_max_fav]

output2.append(output_sum)
output3.append(output_sum2)


#################################################################################################################

### SAVE BEST-FIT OUTPUT
np.savetxt(outfile,output2, fmt='%s')
