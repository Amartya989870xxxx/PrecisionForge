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
mean delta accuracy:  +0.142
min  delta accuracy:  +0.047
mean spread reduction: 1.03x
min  spread reduction: 1.02x
total automated:       70.22 / 90
```

See README.md "Honest result note": full anisotropy credit is unreachable by
any diagonal precision on the public v0 operator (a property of the matrix,
not the solver); the geometry branch reports its true ceiling here.
