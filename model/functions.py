import numpy as np

def ahrrenius(A0, EA, K):
    return     


def temperature_dependance(t ,var):
    act = config['activation']

    k1 = act['k_10'] * np.exp(- act['E_1'] / (K.R * T))
    k_agg = act['k_agg0'] * np.exp(- act['E_agg'] / (K.R * T))
    k_gr = act['k_gr0'] * np.exp(- act['E_gr'] / (K.R * T))
    active_sat = act['k_sol0'] * np.exp(- act['E_sol'] / (K.R * T))

    self.Beta = 4 * self.k * self.T / (9 * self.eta * self.v_m)
    self.R_cap = 2 * self.gamma * self.v_m / (self.k * self.T)
    self.dG = (16 * pi * self.gamma**3 * self.v_m**2) / (self.k**3 * self.T**3)
    self.D = (self.k * self.T) / (6 * pi * self.eta * self.R_0)
    self.A_gr = 4 * pi * self.D * N_A


def calc_nuc_rate(K, var, c):
    var['S'] = c['active'] / K.active_sat

    if var['S'] < 1:
        var['k_nuc'], var['V_nuc'], var['R_nuc'] = 0, 0, 0
        return var

    var['R_nuc'] = K.R_cap / np.log(var['S'])
    var['V_nuc'] = 4 * np.pi * var['R_nuc']**3 / 3
    
    ns = var['V_nuc'] / K.v_m
    if ns < 1:
        var['k_nuc'] = 0
        return var 

    var['k_nuc'] = K.Beta * ns * \
        np.exp(- K.dG / np.log(var['S'])**2)
    return var


def calc_growth_rate(prev, K, J, c, var):
    var['P'] = prev['P']

    if var['S'] == 0:
        return var

    cnd = var['P'] > 0
    var['V'][cnd] = (4 * np.pi / 3) * prev['R'][cnd]**3
    var['V'][cnd] += prev['grown'][cnd] * K.v_m / var['P'][cnd]
    cnd = cnd & (var['V'] > 0)
    var['R'][cnd] = (3 / (4 * np.pi) * var['V'][cnd])**(1/3)

    cnd = var['R'] != 0
    var['r_ratio'][cnd] = K.R_cap / var['R'][cnd]
    var['r_ratio'][var['r_ratio'] > 7] = 7

    cnd = var['R'] != 0
    var['k_gr'][cnd] = 1 - 1 / var['S'] * np.exp(var['r_ratio'][cnd])
    var['k_gr'][cnd] /= (1 + K.D / (var['R'][cnd] * K.k_gr))
    var['k_gr'][cnd] *= K.A_gr * var['R'][cnd] * var['P'][cnd]

    if var['S'] > 1 and var['R_nuc'] > 0:
        var['P'][J] = var['k_nuc'] * c['active']
        var['P'][J] *= K.v_m / var['V_nuc']
        var['P_nuc'][J] = var['P'][J]
        var['R'][J] = var['R_nuc'] if var['P'][J] > 0 else 0
    return var


def apply_agg_avg(P, P_nuc, R, t_nuc, t, t_old, sol):
    P_10_1, P_11_2, P_12_3, P_22_4, P_13_4, *_ = sol(t - t_nuc) * P_nuc
    R_10_1, R_11_2, R_12_3, R_22_4, R_13_4 = R.reshape(5, -1)

    *_, dP_11_2__22_4, dP_10_1__13_4, dP_10_1__11_2, dP_10_1__12_3 \
    = (sol(t - t_nuc) * P_nuc) - (sol(t_old - t_nuc) * P_nuc)

    # 1 + 1 -> 2 (11) ---------------------------------------------------------
    cnd = (dP_10_1__11_2 > 0) & (P_11_2 > 0)
    R_11_2[cnd] = (
                    2 * R_10_1[cnd] * dP_10_1__11_2[cnd] 
                    + R_11_2[cnd] * P_11_2[cnd]
                ) / (dP_10_1__11_2[cnd] + P_11_2[cnd])

    P_10_1[cnd] -= 2 * dP_10_1__11_2[cnd]
    P_11_2[cnd] += dP_10_1__11_2[cnd]


    # 1 + 2 -> 3 (12) ---------------------------------------------------------
    cnd = (dP_10_1__12_3 > 0) & (P_12_3 > 0)
    R_12_3[cnd] = (
                    (R_10_1[cnd] + R_11_2[cnd]) * dP_10_1__12_3[cnd] 
                    + R_12_3[cnd] * P_12_3[cnd]
                ) / (dP_10_1__12_3[cnd] + P_12_3[cnd])

    P_10_1[cnd] -= dP_10_1__12_3[cnd] 
    P_11_2[cnd] -= dP_10_1__12_3[cnd] 
    P_12_3[cnd] += dP_10_1__12_3[cnd]

    # 2 + 2 -> 4 (22) ---------------------------------------------------------
    cnd = (dP_11_2__22_4 > 0) & (P_22_4 > 0)
    R_22_4[cnd] = (
                    2 * R_11_2[cnd] * dP_11_2__22_4[cnd] 
                    + R_22_4[cnd] * P_22_4[cnd]
                ) / (dP_11_2__22_4[cnd] + P_22_4[cnd])

    P_11_2[cnd] -= 2 * dP_11_2__22_4[cnd]
    P_22_4[cnd] += dP_11_2__22_4[cnd]

    # 1 + 3 -> 4 (13) ---------------------------------------------------------
    cnd = (dP_10_1__13_4 > 0) & (P_13_4 > 0)
    R_13_4[cnd] = (
                    (R_10_1[cnd] + R_12_3[cnd]) * dP_10_1__13_4[cnd] 
                    + R_13_4[cnd] * P_13_4[cnd]
                ) / (dP_10_1__13_4[cnd] + P_13_4[cnd])

    P_10_1[cnd] -= dP_10_1__13_4[cnd]
    P_12_3[cnd] -= dP_10_1__13_4[cnd]
    P_13_4[cnd] += dP_10_1__13_4[cnd]
    # -------------------------------------------------------------------------
    P = np.concatenate((P_10_1, P_11_2, P_12_3, P_22_4, P_13_4))
    R = np.concatenate((R_10_1, R_11_2, R_12_3, R_22_4, R_13_4))
    return P, R
