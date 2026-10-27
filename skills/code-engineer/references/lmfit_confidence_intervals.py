"""Runnable lmfit 1.3.x confidence-interval reference.

Tested with lmfit 1.3.4 (the version used by the science demos).

Run:
    python lmfit_confidence_intervals.py
"""

import lmfit
import numpy as np


def michaelis_menten(substrate, vmax, km):
    return vmax * substrate / (km + substrate)


def main():
    rng = np.random.default_rng(0)
    substrate = np.linspace(0.1, 10.0, 40)
    observed = michaelis_menten(substrate, 12.0, 2.5)
    observed = observed + rng.normal(0.0, 0.15, substrate.size)

    # Path 1: lmfit.Model returns a ModelResult.
    model = lmfit.Model(michaelis_menten)
    model_result = model.fit(observed, substrate=substrate, vmax=10.0, km=1.0)
    if not model_result.errorbars:
        raise RuntimeError(
            "ModelResult has no error bars; fix the fit before computing intervals"
        )
    model_ci = model_result.conf_interval(sigmas=[1, 2])

    # Path 2: lmfit.Minimizer.minimize() returns a MinimizerResult.
    params = lmfit.Parameters()
    params.add("vmax", value=10.0, min=0.0)
    params.add("km", value=1.0, min=0.0)

    def residual(params, x, data):
        return michaelis_menten(x, params["vmax"].value, params["km"].value) - data

    minimizer = lmfit.Minimizer(residual, params, fcn_args=(substrate, observed))
    minimizer_result = minimizer.minimize()
    if not minimizer_result.errorbars:
        raise RuntimeError(
            "MinimizerResult has no error bars; fix the fit before computing intervals"
        )
    minimizer_ci = lmfit.conf_interval(minimizer, minimizer_result, sigmas=[1, 2])

    print(f"lmfit version: {lmfit.__version__}")
    print(f"ModelResult vmax: {model_result.params['vmax'].value:.3f}")
    print(f"ModelResult vmax stderr: {model_result.params['vmax'].stderr:.3f}")
    print(f"ModelResult CI parameters: {sorted(model_ci)}")
    print(f"MinimizerResult vmax: {minimizer_result.params['vmax'].value:.3f}")
    print(f"MinimizerResult vmax stderr: {minimizer_result.params['vmax'].stderr:.3f}")
    print(f"MinimizerResult CI parameters: {sorted(minimizer_ci)}")


if __name__ == "__main__":
    main()
