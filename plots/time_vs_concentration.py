"""
plot of time vs concentration, showing the actual Nucleation Growth model
"""
import numpy as np


def time_vs_concentration(df, ax):
    gr_col = df.columns[df.columns.str.startswith("grown")]
    df["grown"] = df[gr_col].sum(axis=1)
    nuc_max = df["nucleated"].max()
    f = df["initial"].max() * 0.8 / df["amorphus"].max()
    df["amorphus"] = df["amorphus"] * f
    expnt = np.floor(np.log10(abs(nuc_max)))
    expnt = np.floor(np.log10(abs(nuc_max)))
    df["nucleated"] *= 10 ** -(expnt + 1)

    config = {
        "initial": {"label": r"[$\mathrm{Fe(OA)_3}$]", "linestyle": "-"},
        "amorphus": {"label": r"$[\mathrm{FeO_x^*}] \cdot$"+f'{f:1.0f}'+r"$^{-1}$", "linestyle": "-"},
        "active": {"label": r"[$\mathrm{Fe(OA)_m}$]", "linestyle": "-"},
        "nucleated": {
            "label": r"[$\mathrm{Fe(OA)_m^{nucleated}}]\cdot$" + f"1e{expnt+1:1.0f}" ,
            "linestyle": "-",
        },
        "grown": {"label": r"$\sum$[$\mathrm{Fe(OA)_m^{grown}}$]", "linestyle": "-"},
    }

    configAu = {
        "initial": {"label": r"[Au$^+$]", "linestyle": "-"},
        "amorphus": {"label": r"[B]", "linestyle": "-"},
        "active": {"label": r"[Au$^0$]", "linestyle": "-"},
        "nucleated": {
            "label": f"1e{expnt+1:1.0f}" + r"$\cdot$[Au$^0_\mathrm{Nucleation}$]",
            "linestyle": "-",
        },
        "grown": {"label": r"$\sum$[Au$^0_\mathrm{Growth}$]", "linestyle": "-"},
    }
    for species, species_style in config.items():
        ax.plot(df.t, df[species], **species_style)
    ax.set_xlim(100, df.t.iloc[-1])
    ax.set_xscale("log")
    ax.set_ylim(0, df["initial"].max())
    ax.legend(loc="center right")

    return ax
