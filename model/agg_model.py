from scipy import integrate


def solve_agg(agg, t_bound, **kwargs):
    y0 = [1, 0, 0, 0, 0, 0, 0]
    ode = integrate.solve_ivp(
        Aggregation(agg).model, t_span=(0, t_bound), y0=y0, dense_output=True
    )
    return ode


class Aggregation:
    def __init__(self, k_agg):
        self.c = {}
        self.ddt = {}
        self.k_agg = k_agg

    def model(self, t, y):
        c, ddt, k_agg = self.c, self.ddt, self.k_agg
        c['P_01_1'], c['P_11_2'], c['P_12_3'], c['P_22_4'], c['P_13_4'], *_ = y

        # -------------------------------------
        ddt['P_01_1_P_01_1__P_11_2'] = k_agg * (+ 1 * c['P_01_1'] * c['P_01_1'])
        ddt['P_01_1_P_11_2__P_12_3'] = k_agg * (+ 1 * c['P_01_1'] * c['P_11_2'])
        ddt['P_01_1'] = k_agg * (
                - 2 * c['P_01_1'] * c['P_01_1']
                - 1 * c['P_01_1'] * c['P_12_3']
                - 1 * c['P_01_1'] * c['P_13_4']
        )
        # -------------------------------------
        ddt['P_11_2'] = k_agg * (
                + 1 * c['P_01_1'] * c['P_01_1']
                - 2 * c['P_11_2'] * c['P_11_2']
        )
        # -------------------------------------
        ddt['P_12_3'] = k_agg * (
                + 1 * c['P_01_1'] * c['P_11_2']
                - 1 * c['P_12_3'] * c['P_01_1']
        )
        # -------------------------------------
        ddt['P_22_4'] = k_agg * (
                + 1 * c['P_11_2'] * c['P_11_2']
        )
        # -------------------------------------
        ddt['P_13_4'] = k_agg * (
                + 1 * c['P_01_1'] * c['P_12_3']
        )
        # -------------------------------------

        return [ddt['P_01_1'],
                ddt['P_11_2'],
                ddt['P_12_3'],
                ddt['P_22_4'],
                ddt['P_13_4'],
                ddt['P_01_1_P_01_1__P_11_2'],
                ddt['P_01_1_P_11_2__P_12_3'],
                ]


if __name__ == "__main__":
    ode = solve_agg(0.1, 0.1)
