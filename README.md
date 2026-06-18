# Postprocessing and analysis scripts used in Franke et al. (2026): Local modification of tropical precipitation by small-scale air-sea interactions in km-scale climate models, submitted to the *Journal of the Atmospheric Sciences*

## Before you start
Clone the following repositories to your local machine:
1. [grid_toolbox](https://github.com/HF7weatherman/grid_toolbox.git)
2. [hfutils](https://github.com/HF7weatherman/hfutils.git)
3. [hfplot](https://github.com/HF7weatherman/hfplot.git)
4. [pycompo](https://github.com/HF7weatherman/pycompo.git)

In `environment.yaml`, replace `<local_path>` by the path where you have cloned these four directories to.

## Project-specific environment

To install the project-specific environment, please run

```
mamba env create -f environment.yaml
```

Afterwards, the environment can be activated by

```
mamba activate ASI-conv
```

