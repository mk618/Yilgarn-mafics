"""

Set of functions for continental isostatic calculations.

Fergus McNab, Mark Hoggard 2017


"""

import numpy as np

#------------------------------------------------------------------------------------------------------#
class Rho_a:

    """
    Calculate density of asthenospheric mantle, accounting for effects of 
    thermal expansion and compressibility.

    Methods:

    Attributes:

    """

    def __init__(self, alpha, rho_0, dT_dz, z_comp, z_top, T_p):

        self.alpha = alpha
        self.rho_0 = rho_0
        self.dT_dz = dT_dz
        self.z_comp = z_comp
        self.z_top = z_top
        self.T_p = T_p

    def z_a(self):

        z_comp = self.z_comp
        z_top = self.z_top

        return z_comp - z_top

    def T_base(self):

        T_p = self.T_p
        dT_dz = self.dT_dz
        z_comp = self.z_comp
        
        return T_p + z_comp*dT_dz

    def T_a(self):

        T_base = self.T_base()
        dT_dz = self.dT_dz
        z_a = self.z_a()
                
        return T_base - (0.5 * dT_dz * z_a)

    def rho_a(self):

        alpha = self.alpha
        rho_0 = self.rho_0
        T_a = self.T_a()

        return rho_0 * ( 1. - T_a*alpha )
#------------------------------------------------------------------------------------------------------#


#------------------------------------------------------------------------------------------------------#
class Rho_l:

    def __init__(self, alpha, rho_0, rho_cc, del_rho, z_l, z_cc, z_comp, T_comp, dT_dz):

        self.alpha = alpha
        self.rho_0 = rho_0
        self.rho_cc = rho_cc
        self.del_rho = del_rho
        self.z_l = z_l
        self.z_cc = z_cc
        self.z_comp = z_comp
        self.T_comp = T_comp
        self.dT_dz = dT_dz

    def T_base(self):

        T_comp = self.T_comp
        dT_dz = self.dT_dz
        z_l = self.z_l
        z_comp = self.z_comp

        return T_comp - (z_comp - z_l) * dT_dz

    def T_l(self):

        T_base = self.T_base()
        z_cc = self.z_cc
        z_l = self.z_l

        return (0.5*T_base) * ( 1 + ( z_cc/z_l ) )

    def P_l(self):

        P_base = self.P_base
        z_cc = self.z_cc
        rho_cc = self.rho_cc
        g = self.g

        return 0.5 * ( P_base + ( ( z_cc * rho_cc * g ) / 1000. ) )

    def rho_l(self):

        alpha = self.alpha
        rho_0 = self.rho_0
        del_rho = self.del_rho
        T_l = self.T_l()

        return (rho_0 - del_rho) * ( 1. - (alpha*T_l) )
#------------------------------------------------------------------------------------------------------#

#------------------------------------------------------------------------------------------------------#
class Rho_l_delam:

    def __init__(self, alpha, K, rho_0, rho_cc, del_rho, z_l, z_l_old, z_cc, T_base, P_base, g=9.8):

        self.alpha = alpha
        self.K = K
        self.rho_0 = rho_0
        self.rho_cc = rho_cc
        self.del_rho = del_rho
        self.z_l = z_l
        self.z_l_old = z_l_old
        self.z_cc = z_cc
        self.T_base = T_base
        self.P_base = P_base
        self.g = g

    def T_l(self):

        T_base = self.T_base
        z_cc = self.z_cc
        z_l = self.z_l
        z_l_old = self.z_l_old

        return (0.5*T_base) * (z_l / z_l_old) * ( 1 + ( z_cc/z_l ) )

    def P_l(self):

        P_base = self.P_base
        z_cc = self.z_cc
        rho_cc = self.rho_cc
        g = self.g

        return 0.5 * ( P_base + ( ( z_cc * rho_cc * g ) / 1000. ) )

    def rho_l(self):

        alpha = self.alpha
        K = self.K
        rho_0 = self.rho_0
        del_rho = self.del_rho
        T_l = self.T_l()
        P_l = self.P_l()

        return (rho_0 - del_rho) * ( 1. - (alpha*T_l) + (P_l/K) )
#------------------------------------------------------------------------------------------------------#

#------------------------------------------------------------------------------------------------------#
def E(z_cc, z_oc, z_w, z_l, rho_a, rho_cc, rho_oc, rho_w, rho_l):

    cc = z_cc * ((rho_a - rho_cc) / rho_a)
    oc = z_oc * ((rho_a - rho_oc) / rho_a)
    w = z_w * ((rho_a - rho_w) / rho_a)
    l = (z_l - z_cc) * ((rho_a - rho_l) / rho_a)

    return cc - oc - w + l
#------------------------------------------------------------------------------------------------------#

#------------------------------------------------------------------------------------------------------#
def E_with_ca(z_cc, z_oc, z_w, z_l, rho_a, rho_cc, rho_oc, rho_w, rho_l, z_comp, rho_ca):

    cc = z_cc * ((rho_l - rho_cc) / rho_a)
    l = z_l * ((rho_ca - rho_l) / rho_a)
    w = z_w * ((rho_a - rho_w) / rho_a)
    oc = z_oc * ((rho_a - rho_oc) / rho_a)
    a = z_comp * ((rho_ca - rho_a) / rho_a)

    return cc + l - w - oc - a
#------------------------------------------------------------------------------------------------------#
