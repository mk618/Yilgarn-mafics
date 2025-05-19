"""

Continental isostatic calculations, balanced against a present-day mid-oceanic ridge.

2017: Originally written by Fergus McNab and Mark Hoggard for McNab et al. (2018), https://doi.org/10.1002/2017GC007251
2018: Modified by Marthe Klöcking for cratonic continental lithosphere for Klöcking et al. (2018), https://doi.org/10.1029/2018GC007559
2025: Modified by Marthe Klöcking for cratonic continental lithosphere at multiple age steps

"""


import numpy as np
from isostatic_balance_functions import *

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ USER INPUTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
alpha = 3.3e-5                                  # mantle thermal expansion                oC^(-1)       
K = 115.2                                       # mantle bulk modulus                     GPa           
                                                                    
rho_0 = 3.33                                    # mantle reference density                Mg m^(-3)     
rho_w = 1.03                                    # water density                           Mg m^(-3)     
rho_oc = 2.86                                   # oceanic crust density                   Mg m^(-3)
# rho_cc = 2.80                                   # continental crust density               Mg m^(-3)
# del_rho = 0.015                                 # continental lithosphere depletion       Mg m^(-3)

dT_dz = 0.44                                    # mantle temperature gradient             oC km^(-1)
dP_dz = 0.033                                   # mantle pressure gradient                GPa km ^(-1)

z_w = 2.8                                       # mid-ocean ridge depth                   km
z_oc = 7.1                                      # oceanic crust thickness                 km

z_comp = 220.

T_p_o = 1330.                                   # potential temperature of oceanic column oC
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# calculate density of oceanic asthenosphere
R_oa = Rho_a(alpha, rho_0, dT_dz, z_comp, (z_w + z_oc), T_p_o)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

## set input parameters for continental columns
##                  present; 2.65; 2.72 (post/pre-eruption); pre-2.72 (pref - max - min)
z_l     = np.array([ 220.,  180., 180.,  110.,   40.,   50.,   60.,   30.])
z_cc    = np.array([  40.,   50., 50.,   30.,   10.,   15.,   20.,   15.])
T_p_c   = np.array([1330., 1420., 1550., 1550., 1550., 1420., 1420., 1420.])
rho_cc  = np.array([2.74,  2.9, 2.9,   2.9,   2.8,   2.8,   2.8,   2.8])
del_rho = np.array([0.015, 0.015, 0.015,    0.,    0.,    0.,    0.,    0.])

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
## calculate predicted elevation of continental column

R_ca = Rho_a(alpha, rho_0, dT_dz, z_comp, z_l, T_p_c)
R_l = Rho_l(alpha, rho_0, rho_cc, del_rho, z_l, z_cc, z_comp, R_ca.T_base(), dT_dz)
elev = E_with_ca(z_cc, z_oc, z_w, z_l, R_oa.rho_a(), rho_cc, rho_oc, rho_w, R_l.rho_l(), z_comp, R_ca.rho_a())

print(np.around(elev,2))

np.savetxt("uplift_yilgarn.txt", elev)


