import matplotlib.pyplot as plt
from scipy.constants import k, N_A
from pint import UnitRegistry
from dataclasses import dataclass
import numpy as np

ureg = UnitRegistry()
Q_ = ureg.Quantity

from ezplot import create_basic_plot

@dataclass
class Constants():
    k = Q_(k, 'joule / kelvin')
    N_A = Q_(N_A, 'mole ** -1')
    
    rho = Q_(1.93e7, 'gram / meter ** 3') # gold density
    M = Q_(196.9665, 'gram / mole') # gold molar mass
    eta = Q_(0.55, 'millipascal * second') # gold viscosity
    T = Q_(295.15, 'kelvin') # temperature
    gamma = Q_(245, 'millinewton / meter') # surface tension
    k_gr_0 = Q_(5.3e-4, 'meter / second') # growth rate constant


def derived_constants(K):
    K.v_m = K.M / (K.rho * K.N_A)
    K.R_cap = 2 * K.gamma * K.v_m / (K.k * K.T) 
    K.R_0 = ((3 * K.v_m) / (4 * np.pi)) ** (1 / 3)
    K.D = K.k * K.T / (6 * np.pi * K.eta * K.R_0)

def growth_rate(K, R, S):
        r_ratio = K.R_cap / R
        k_gr = 1 - 1 / S * np.exp(r_ratio)
        k_gr /= 1 + K.D / (R * K.k_gr_0)  
        k_gr *= R * np.pi * K.D * K.N_A
        return k_gr

def main():
    K = Constants()
    derived_constants(K)
    S = [10, 5, 2, 1.5, 1.1]
    R = np.linspace(0.1e-9, 5e-9, 100)
    R = Q_(R, 'meter')

    unit = growth_rate(K, R, S[0]).to_base_units().units
    # parse unit to a better formatted string
    unit = str(unit).replace('**', '^').replace('meter', 'm').replace('second', 's')

    fig, ax = create_basic_plot(xlabel='Radius (m)', ylabel='Growth rate (m/s)')

    for s in S:
        # convert R to meters
        k_gr = growth_rate(K, R, s).to_base_units()
        plt.plot(R, k_gr, label=f'S = {s}')
    plt.xlabel('Radius (m)')
    plt.ylabel(f'Growth rate {unit}')
    plt.axhline(0, color='black', linewidth=0.5)
    print(f'Critical radius: {K.R_cap}')
    plt.xlim(0, K.R_cap.to_base_units().magnitude * 2)
    plt.ylim(-4e4, 2e4)
    plt.legend()
    plt.savefig('growth.pdf')
plt.show()


if __name__ == '__main__':
        main()
