# SynthStrip

This is a NiPreps implementation of the SynthStrip skull-stripping tool.

## Installation

```bash
# To install the base package
pip install nipreps-synthstrip

# For the nipype interface
pip install nipreps-synthstrip[nipype]

# For the pydra interface
pip install nipreps-synthstrip[pydra]
```

### Command Line Tool

```bash
$ nipreps-synthstrip
```

### Nipype Interface

```python
from nipreps.synthstrip.wrappers.nipype import SynthStrip
```

### Pydra Interface

```python
from nipreps.synthstrip.wrappers.pydra import SynthStrip
```

## Citation

> A Hoopes, JS Mora, AV Dalca, B Fischl, M Hoffmann.
> SynthStrip: Skull-Stripping for Any Brain Image.
> https://arxiv.org/abs/2203.09974
