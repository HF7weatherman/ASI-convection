import intake
import seaborn as sns
sns.set_context('talk')
import warnings
warnings.filterwarnings(action='ignore')

# some functions
def fix_vgrid(ds):
    return ds.rename({"height": "halflevel",
                      "height_2": "level",
                      "ncells": "cell",
                      "vertices": "vertex"})

# physical constants
CPD = 1004.64     # sp. heat const. pressure (dry air) J/kg/K
RD  = 287.04      # sp. gas const. (dry air) J/kg/K
CVD = CPD - RD    # sp. heat const. volume (dry air) J/kg/K

CPV = 1869.46     # sp. heat const. pressure (vapor) J/kg/K
RV  = 461.51      # sp. gas const. (vapor) J/kg/K
CVV = CPV - RV    # sp. heat const. volume (vapor) J/kg/K

CI = 2093         # sp. heat constant (ice) J/kg/K
CL = 4184         # sp. heat constant (liquid) J/kg/K

LV = 2.5008e6     # latent heat vaporization J/kg
LS = 2.8346e6     # latent heat sublimation J/kg
LF = LS - LV      # latent heat fusion J/kg
TMELT = 273.15    # melting pt. of water K
G = 9.80665       # acc. due to gravity m/s2


# calculate MSE in parallel
from dask.distributed import Client
client = Client(processes=False, threads_per_worker=256, n_workers=1) #, memory_limit='128GB')

# read in data
cat = intake.open_catalog("/home/m/m300827/catalogs/catalog.yaml")
dset = cat.nextGEMS.dpp0066.atm["3d_ml"].to_dask()
vgrid = cat.grids[dset.uuidOfVGrid].to_dask().pipe(fix_vgrid)
dset = dset.sel(time = slice('2020-06-01', '2020-08-31'))

qt = dset.hus + dset.clw + dset.cli
mse_e = (CPD + qt * (CL - CPD)) * dset.ta + LV * dset.hus - LF * dset.cli + G * vgrid.zg.drop(['clon', 'clat'])