# Submission Manifest

Copy these files into `bench-p04-pcam/` or keep the same structure in your
submission repository:

```text
adapters/myteam.py
adapters/__init__.py
README.md
```

Run from the benchmark folder after copying:

```bash
python3 self_check.py --adapter adapters.myteam:Engine
python3 -m py_compile adapters/myteam.py
```

Last verified public full self-check (5 seeds):

```text
mean delta accuracy:  +0.269
min  delta accuracy:  +0.088
mean spread reduction: 1.30x
min  spread reduction: 1.27x
total automated:       73.26 / 90   (self_check.py, full at 5x)
                       ~72.28 / 90  (official guide, anisotropy full at 10x)
```

The geometry branch now preconditions the Hessian at the true equilibrium
`a* = find_equilibrium(x_i)` (Lemma E3), the point the harness actually
scores — not the stored pattern `x_i`. See README.md "Scoring vs. official
guide" and "Honest result note": full anisotropy credit is unreachable by any
diagonal precision on the public v0 operator (a property of the operator's
rotational structure, not the solver — triangulated three ways); the geometry
branch reports its true ceiling here while remaining the correct principled
construction for the council-only L3 held-out data.
