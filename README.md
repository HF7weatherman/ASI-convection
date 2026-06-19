# Code to reproduce Figures in Franke et al. (2026, JAS)
**Reference publication:**
H. Franke et al. (2026): Local modification of tropical precipitation by small-scale air-sea interactions in km-scale climate models, submitted to the *Journal of the Atmospheric Sciences*

## Before you start
Get the following repositories to your local machine:
1. [grid_toolbox](https://github.com/HF7weatherman/grid_toolbox.git)
2. [hfutils](https://github.com/HF7weatherman/hfutils.git)
3. [hfplot](https://github.com/HF7weatherman/hfplot.git)
4. [pycompo](https://github.com/HF7weatherman/pycompo.git)

You could access them via two ways:
1. Download the release *Primary data of Franke et al. (2026, JAS)*.
2. Clone the repository and checkout the tag *publication_Franke_etal_2026_JAS*.

## Project-specific environment

First of all: replace `<local_path>` in `environment.yaml` by the path you have saved the above four directories at.

Afterwards, install the project-specific environment:

```
mamba env create -f environment.yaml
```

The environment can be activated by

```
mamba activate ASI-conv
```

