import numpy as np
import xarray as xr

# ------------------------------------------------------------------------------
# Constants
# ---------
G = 9.80665       # acc. due to gravity m/s2

LV = 2.5008e6     # latent heat vaporization J/kg
LS = 2.8346e6     # latent heat sublimation J/kg

CPD_BF = 1005.7   # sp. heat const. pressure (dry air) J/kg/K, at about 20degC
CPD = 1004.64     # sp. heat const. pressure (dry air) J/kg/K, at about 5degC
CL = 4184         # sp. heat constant (liquid) J/kg/K
LF = LS - LV      # latent heat fusion J/kg

BETA = 0.6078


# ------------------------------------------------------------------------------
# Functions
# ---------
def calc_T_v(T: xr.DataArray, hus: xr.DataArray) -> xr.DataArray:
    return T * (1. + BETA * hus)


def calc_sfc_bf(
        pres: xr.DataArray,
        shf: xr.DataArray,
        lhf: xr.DataArray,
        T: xr.DataArray,
        hus: xr.DataArray,
        ) -> xr.DataArray:
    """
    ref: from X. Chen et al. (2025), who actually got it from de Szoeke
    full terms 
    Output is in W/m^2 by multiplying rho*cp to the density temperature flux. 
    """
    Tv = calc_T_v(T, hus)
    rho = calc_density(T, hus, pres)

    # units: m^2/s^3 (flux of KE) 
    return G/(rho*Tv) * (shf/CPD_BF * (1+BETA*hus) + lhf/LV * BETA * T)


def calc_mse_e(dset: xr.Dataset) -> xr.Dataset:

    qt = dset['hus'] + dset['clw'] + dset['cli']

    thermal_energy = (CPD + qt * (CL - CPD)) * dset['ta']
    latent_energy = LV * dset['hus'] - LF * dset['cli']
    potential_energy = G * dset['zg']

    return thermal_energy + latent_energy + potential_energy


def calc_mse_sfc(dset: xr.Dataset) -> xr.Dataset:
    Z = 2.
    return (CPD_BF * dset['tas'] + LV * dset['hus2m'] + G * Z)


def calc_mse_sfc_ifs(dset: xr.Dataset) -> xr.Dataset:
    hus2m = calc_hus2m_from_td(dset['2d'], dset['ps'])
    Z = 2.
    return (CPD_BF * dset['tas'] + LV * hus2m + G * Z)


def calc_density(
        T: xr.DataArray,
        hus: xr.DataArray,
        pres: xr.DataArray,
        ) -> xr.DataArray:
    R_D = 287.085    # specific gas constant for dry air (J/kg/K)
    T_v = calc_T_v(T, hus)
    return pres / (R_D * T_v)


def calc_clwvi(
        cllvi: xr.DataArray,
        clivi: xr.DataArray,
        ) -> xr.DataArray:
    return cllvi + clivi


def magnus_formula_Pa(T):
    """Calculate saturation vapor pressure over liquid water using Magnus formula."""
    a = 610.78  # Pa
    b = 17.1
    c = 235  # °C
    return a * np.exp(b * T / (T + c))


def calc_hus2m_from_td(td, ps):
    """Calculate specific humidity at 2m from dew point temperature and surface pressure."""
    # Convert dew point temperature from K to °C
    td_c = td - 273.15

    # Calculate saturation vapor pressure at dew point temperature
    e_s = magnus_formula_Pa(td_c)  # in Pa

    # Calculate specific humidity from saturation vapor pressure and surface pressure reduced by 2m
    return 0.622 * e_s / (ps - 0.25 - 0.37 * e_s)