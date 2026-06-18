import gc
import intake
import logging
import os
import sys

import easygems.healpix as egh
import numpy as np
import xarray as xr

from joblib import Parallel, delayed
from pandas import date_range
from pathlib import Path

import grid_toolbox.spherical_derivatives_latlon as sphder_latlon
import grid_toolbox.basic_healpix as hp_basic
import hfutils.datetime_utils as dtutil

import physics
from variables import VARS


# ------------------------------------------------------------------------------
# Global variables
# ----------------
TARGET_LATLON = {
    'lats': (-30, 30, 680),
    'lons': (-180, 180, 4080),
    'supersampling': {"lon": 4, "lat": 4},
}

IFS_EXPS = ["ifs_tco3999-ng5_deepoff", "ifs_tco3999-ng5_rcbmf"]
CAT = {
    "ICON": "https://data.nextgems-h2020.eu/catalog.yaml",
    "IFS": "https://digital-earths-global-hackathon.github.io/catalog/catalog.yaml"
}

IFS2ICON_RENAME_MAP = {
    "10u": "uas",
    "10v": "vas",
    "10si": "sfcwind",
    "2t": "tas",
    "tp": "pr",
    "sp": "ps",
    "sst": "ts",
    "ttr": "rlut",
    "tcwv": "prw",
    "sshf": "hfss",
    "slhf": "hfls",
    "tclw": "cllvi",
    "tciw": "clivi",
    "u": "ua",
    "v": "va",
    "w": "wap",
    "t": "ta",
    "q": "hus",
    "ciwc": "cli",
    "clwc": "clw",
    }


# ------------------------------------------------------------------------------
# Parallel execution functions
# ----------------------------
def process_one_timestep_remap(dset, index, target_latlon):
    data = dset.isel(time=index)
    return hp_basic.remap_nn_hp2latlon(
        data, target_latlon['lats'], target_latlon['lons'],
        target_latlon['supersampling'],
        )


def process_one_timestep_calc_conv(dset, index):
    data = dset.isel(time=index)
    return sphder_latlon.compute_hor_wind_conv_on_latlon(
        data['uas'], data['vas'],
        )


def process_one_timestep_calc_conv_components(dset, index):
    data = dset.isel(time=index)
    return sphder_latlon.compute_hor_wind_conv_components_on_latlon(
        data['uas'], data['vas'],
        )


def process_one_timestep_calc_mse_e(dset, index):
    data = dset.isel(time=index)
    return physics.calc_mse_e(data)


def process_one_timestep_calc_mse_sfc(dset, index):
    data = dset.isel(time=index)
    return physics.calc_mse_sfc(data)


def process_one_timestep_calc_mse_sfc_ifs(dset, index):
    data = dset.isel(time=index)
    return physics.calc_mse_sfc_ifs(data)


def process_one_timestep_calc_sfc_density(dset, index):
    data = dset.isel(time=index)
    return physics.calc_density(data['tas'], data['hus2m'], data['ps'])


def process_one_timestep_calc_sfc_bf(dset, index):
    data = dset.isel(time=index)
    return physics.calc_sfc_bf(
        data['ps'], data['hfss'], data['hfls'], data['tas'], data['hus2m'],
        )


def process_one_timestep_calc_clwvi(dset, index):
    data = dset.isel(time=index)
    return physics.calc_clwvi(data['cllvi'], data['clivi'])


FUNC_REGISTRY = {
    'sfcwind_conv': process_one_timestep_calc_conv,
    'sfcwind_conv_comp': process_one_timestep_calc_conv_components,
    'mse_e': process_one_timestep_calc_mse_e,
    'mse_sfc': process_one_timestep_calc_mse_sfc,
    'mse_sfc_ifs': process_one_timestep_calc_mse_sfc_ifs,
    'sfc_rho': process_one_timestep_calc_sfc_density,
    'sfc_bf': process_one_timestep_calc_sfc_bf,
    'clwvi': process_one_timestep_calc_clwvi,
}


# ------------------------------------------------------------------------------
# Main execution function to calc an additional quantity
# ------------------------------------------------------
def calc_quantity(ovar: str, vars_needed: list[str]):
    exp, start_date, end_date, granularity, odir, n_jobs = _get_arguments()
    analysis_times = [
        np.datetime64(t) for t in date_range(
            np.datetime64(start_date), np.datetime64(end_date), freq='MS',
            )
        ]
    data = read_in_hp_data(exp, VARS[ovar]['dim'], granularity)
    if ovar == "mse_e":
        altitude = np.array(
            [73727.2891, 71235.4219, 68814.0938, 66443.7891, 64140.6133,
                61902.7656, 59728.5625, 57616.4141, 55560.3828, 53551.6094,
                51589.1094, 49671.9727, 47803.7930, 45991.2344, 44233.1914,
                42528.6211, 40876.5273, 39275.9688, 37726.0352, 36225.8750,
                34774.6602, 33371.6172, 32015.9883, 30707.0684, 29444.1738,
                28226.6543, 27053.8906, 25927.4180, 24851.4746, 23829.5391,
                22864.3750, 21955.9531, 21100.9395, 20296.1895, 19538.7520,
                18825.8438, 18154.8477, 17523.2988, 16928.8789, 16369.4053,
                15842.8232, 15347.1982, 14880.7109, 14441.6494, 14022.5205,
                13616.2744, 13216.2744, 12816.2744, 12416.2744, 12016.2744,
                11616.2744, 11216.2744, 10816.2744, 10416.2744, 10016.2744,
                9616.2744,  9216.2744,  8816.2744,  8416.2744,  8016.2739,
                7616.2739,  7216.2739,  6816.2739,  6416.2739,  6016.2739,
                5616.2739,  5220.4321,  4835.6538,  4464.6704,  4107.4575,
                3764.0017,  3434.3030,  3118.3750,  2816.2468,  2527.9646,
                2253.5935,  1993.2206,  1746.9575,  1514.9450,  1297.3583,
                1094.4139,   906.3797,   733.5876,   576.4535,   435.5065,
                311.4361,   205.1747,   118.0616,    52.2459,    12.5000,
            ]
        )
        altitude = altitude[[int(idx-1) for idx in data['height'].values]]
        data = data.assign_coords(zg=('height', altitude))

    # MAIN LOGICAL LOOP
    for i in range (len(analysis_times)-1):
        # time settings
        start_t = analysis_times[i]
        end_t = analysis_times[i+1]
        time_window = (start_t, end_t - np.timedelta64(1,'ns'))
        file_dstring = \
            f"{dtutil.np_datetime2file_datestr(start_t)}-" + \
            f"{dtutil.np_datetime2file_datestr(end_t)}"
        logging.info(f"Processing {start_t} to {end_t}")
        
        # Set filenames and check whether output file already exists
        if ovar == 'sfcwind_conv_comp':
            ofile_ua = f"{odir}/uas_conv_latlon/" + \
                f"{exp}_tropical_uas_conv_{file_dstring}.nc"
            ofile_va = f"{odir}/vas_conv_latlon/" + \
                f"{exp}_tropical_vas_conv_{file_dstring}.nc"
            if os.path.exists(ofile_ua) and os.path.exists(ofile_va):
                logging.info(f"Skipping {ofile_ua}, {ofile_va}, already exist.")
                continue
        elif ovar == 'mse_sfc_ifs':
            ofile = f"{odir}/mse_sfc_latlon/" + \
                f"{exp}_tropical_mse_sfc_{file_dstring}.nc"
            if os.path.exists(ofile):
                logging.info(f"Skipping {ofile}, already exists.")
                continue
        else:
            ofile = f"{odir}/{ovar}_latlon/" + \
                f"{exp}_tropical_{ovar}_{file_dstring}.nc"
            if os.path.exists(ofile):
                logging.info(f"Skipping {ofile}, already exists.")
                continue

        # Procesing: sfcwind_conv needs to be calculated on latlon, all other on hp
        if ovar in ['sfcwind_conv', 'sfcwind_conv_comp']:
            latlon_infiles = {
                var: f"{odir}/{var}_latlon/{exp}_tropical_{var}_{file_dstring}.nc"
                for var in vars_needed
                }

            if all([os.path.exists(latlon_infiles[var]) for var in vars_needed]):
                logging.info("Read in pre-remapped data")
                data_sample_latlon = xr.open_mfdataset(
                    [latlon_infiles[var] for var in vars_needed], parallel=True,
                    ).squeeze().compute()
                
            else:
                logging.info("Read in and remap raw data")
                data_sample = data[vars_needed].sel(time=slice(*time_window)).\
                    where(ocean(data))
                data_sample = data_sample.map(
                    lambda da: da.astype(np.float32) if da.dtype == np.float64 else da
                    ).compute()
                data_sample_latlon = Parallel(n_jobs=n_jobs)(
                    delayed(process_one_timestep_remap)(
                        data_sample, time, TARGET_LATLON,
                        ) for time in range(data_sample.sizes["time"])
                    )
                data_sample_latlon = xr.concat(data_sample_latlon, dim="time")

            # Calculate additional quantity
            ovar_latlon = Parallel(n_jobs=n_jobs)(
                delayed(FUNC_REGISTRY[ovar])(data_sample_latlon, time)
                for time in range(data_sample_latlon.sizes["time"])
                )
            ovar_latlon = xr.concat(ovar_latlon, dim="time")

        else:
            logging.info("Read in and remap raw data")
            data_sample = data[vars_needed].sel(time=slice(*time_window)).\
                where(ocean(data))
            data_sample = data_sample.map(
                lambda da: da.astype(np.float32) if da.dtype == np.float64 else da
                ).compute()
            
            ovar_hp = Parallel(n_jobs=n_jobs)(
                delayed(FUNC_REGISTRY[ovar])(data_sample, time)
                for time in range(data_sample.sizes["time"])
                )
            ovar_hp = xr.concat(ovar_hp, dim="time")
            
            ovar_latlon = Parallel(n_jobs=n_jobs)(
                delayed(process_one_timestep_remap)(
                    ovar_hp, time, TARGET_LATLON,
                    ) for time in range(ovar_hp.sizes["time"])
                )
            ovar_latlon = xr.concat(ovar_latlon, dim="time")
        
        # Save latlon as netCDF file
        ovar_latlon = ovar_latlon.drop(['crs', 'cell'], errors="ignore")
        ovar_latlon.coords["time"] = \
            ovar_latlon.time.assign_attrs(_FillValue=-1.)
        
        if ovar == 'sfcwind_conv_comp':
            uas_conv = ovar_latlon['conv_ua'].\
                rename('uas_conv').assign_attrs(VARS['uas_conv']['attrs'])
            vas_conv = ovar_latlon['conv_va'].\
                rename('vas_conv').assign_attrs(VARS['vas_conv']['attrs'])
            uas_conv.astype(np.float32).to_netcdf(ofile_ua)
            vas_conv.astype(np.float32).to_netcdf(ofile_va)

        else:
            ovar_latlon = ovar_latlon.\
                rename(ovar).assign_attrs(VARS[ovar]['attrs'])
            ovar_latlon.astype(np.float32).to_netcdf(ofile)
        logging.info("  Finished remapping.")
        
        # Clean up
        if not ovar in ['sfcwind_conv', 'sfcwind_conv_comp']:
            del data_sample, ovar_hp
        else:
            del data_sample_latlon
            if not all(
                [os.path.exists(latlon_infiles[var]) for var in vars_needed]
                ):
                del data_sample
        if ovar == 'sfcwind_conv_comp':
            del uas_conv, vas_conv
        del ovar_latlon
        gc.collect()


def _get_arguments():
    if len(sys.argv) < 7:
        print(
            "Usage: python script.py <exp> <start_day> <end_day> " +
            "<granularity> <outdir> <n_jobs>"
            )
        sys.exit(1)
    return sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], \
        sys.argv[6]


# ------------------------------------------------------------------------------
# Functions to read in data
# -------------------------
def read_in_hp_data(
        exp: str,
        dim: str,
        granularity: str,
        ) -> xr.Dataset:
    print(exp)
    if exp == "ngc5004":
        cat = intake.open_catalog(CAT["ICON"])
        data = cat.ICON["ngc5004"](time=granularity).to_dask().squeeze()
        data['ofs'] = _read_lsm(ofs_source="ngc5004", zoom=9).chunk('auto')
        if dim == '3d':
            data = xr.merge([
                d.rename({'height_2':'height'}) if 'height_2' in d.dims else d
                for d in data.data_vars.values()
                ]).assign_coords(height=data.coords['height'])
            data = data.sel(height=slice(63, 90))

    elif exp in IFS_EXPS:
        cat = intake.open_catalog(CAT["IFS"])
        if exp == "ifs_tco3999_rcbmf":
            data = cat.EU[exp](zoom=11, time="PT1H", chunks='auto')
        else:
            data = cat.EU[exp](
                zoom=11, time="PT1H", dim=dim.upper(), chunks='auto',
                )
        data = data.to_dask().pipe(_rename_ifs_vars)
        data = hp_basic.coarsen_hp_grid_xr(
            hp_basic.rechunk_along_griddim(data), z_out=9,
            )
        data = data.pipe(egh.attach_coords)
        if granularity == "P1D":
            data = data.resample(time="1D").mean()
        data['ofs'] = _read_lsm(ofs_source="ngc5004", zoom=9).chunk('auto')
        if dim == '3d':
            data = data.sel(level=slice(290, 1010))

    else:
        raise ValueError("Please provide a valid experiment!")
    
    return data


def _read_lsm(
        ofs_source: str='ngc5004',
        zoom: int=9,
        remap: bool=False,
        ) -> xr.DataArray:
    if ofs_source=='ngc5004':
        inpath = Path('/home/m/m300738/project_TRR181L4/data/ngc5004_pp')
        ofs_hp = xr.open_dataset(
            str(inpath/Path(f'ocean_fraction_surface_hpz{zoom}.nc'))
            ).pipe(egh.attach_coords)
        ofs_hp = ofs_hp['ocean_fraction_surface'].squeeze()

    else:
        raise ValueError("Please provide a valid 'ofs_source'!")

    if not remap:
        return ofs_hp.drop('healpix')
    else:
        # Nearest-neighbour remapping to lat-lon-grid
        lats = TARGET_LATLON['lats']
        lons = TARGET_LATLON['lons']
        supersampling = TARGET_LATLON['supersampling']
        return hp_basic.remap_nn_hp2latlon(ofs_hp, lats, lons, supersampling)
    

# ------------------------------------------------------------------------------
# Functions for data manipulation
# -------------------------------
def adjust_unit(data: xr.DataArray, exp: str, var: str) -> xr.DataArray:
    if exp == "ngc5004":
        if var == 'pr': data = data * 86400.
    elif exp in IFS_EXPS:
        if var == 'pr': data = data * 24000.
        if var in ['rlut', 'hfss', 'hfls']: data = data / 3600.
        if var == 'rlut': data = data * -1.
    return data


def _rename_ifs_vars(data: xr.Dataset) -> xr.Dataset:
    gridn = hp_basic.guess_gridn(data)
    if gridn != "cell":
        data = data.rename_dims({gridn: "cell"})

    existing = set(data.data_vars)
    renames = {k: v for k, v in IFS2ICON_RENAME_MAP.items() if k in existing}
    if renames:
        data = data.rename(renames)

    return data


def ocean(ds: xr.Dataset) -> xr.DataArray:
    return ds.ofs == 1