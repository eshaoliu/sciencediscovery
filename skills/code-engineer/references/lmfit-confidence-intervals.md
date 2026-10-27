# lmfit confidence intervals

Read this before the first `conf_interval` call in an lmfit analysis. The science
demos pin lmfit 1.3.4; every call and error below was verified against that
version.

## Check the installed version first

```bash
python -c "import lmfit; print(lmfit.__version__)"
```

If the installed version is not 1.3.4, check its API before using the calls
below. Do not retry different argument shapes until one happens to work; inspect
the installed signature:

```python
import inspect
import lmfit

print(inspect.signature(lmfit.conf_interval))
```

## Use the call that matches the result object

| Fit path | Result type | Correct confidence-interval call |
|---|---|---|
| `model = lmfit.Model(...)`; `result = model.fit(...)` | `ModelResult` | `result.conf_interval(sigmas=[1, 2])` |
| `minimizer = lmfit.Minimizer(...)`; `result = minimizer.minimize()` | `MinimizerResult` | `lmfit.conf_interval(minimizer, result, sigmas=[1, 2])` |

These related calls fail on lmfit 1.3.4:

| Invalid call | Actual error |
|---|---|
| `lmfit.conf_interval(result)` | `TypeError: conf_interval() missing 1 required positional argument: 'result'` |
| `lmfit.conf_interval(result.minimizer, result)` where `result` is a `ModelResult` | `AttributeError: 'ModelResult' object has no attribute 'minimizer'` |
| `result.conf_interval()` where `result` is a `MinimizerResult` | `AttributeError: 'MinimizerResult' object has no attribute 'conf_interval'` |

`ModelResult` owns the convenience method; a plain `MinimizerResult` does not.
For the minimizer path, keep the `Minimizer` object and pass it to the module
function.

## Check that the fit produced error bars

Calling `conf_interval` does not make an uncertain fit reliable. Check
`result.errorbars` and the parameter `stderr` values first:

```python
if not result.errorbars:
    raise RuntimeError("fit has no error bars; fix the fit before computing intervals")
```

If `errorbars` is `False`, do not present confidence intervals as valid results.
Inspect the model, parameter bounds, and data, then refit. Report the actual
failure instead of swallowing it.

## Runnable example

[`lmfit_confidence_intervals.py`](lmfit_confidence_intervals.py) fits the same
Michaelis-Menten data through both supported paths:

```bash
python "$SCIENCEDISCOVERY_SKILLS_DIR/code-engineer/references/lmfit_confidence_intervals.py"
```

Expected output on lmfit 1.3.4:

```text
lmfit version: 1.3.4
ModelResult vmax: 12.071
ModelResult vmax stderr: 0.091
ModelResult CI parameters: ['km', 'vmax']
MinimizerResult vmax: 12.071
MinimizerResult vmax stderr: 0.091
MinimizerResult CI parameters: ['km', 'vmax']
```
