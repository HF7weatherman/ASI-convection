import gc
import logging
import os
import psutil
import sys
import warnings

import numpy as np
import xarray as xr

from pandas import date_range
from joblib import Parallel, delayed

import hfutils.datetime_utils as dtutil

from preprocessing import read_in_hp_data, process_one_timestep_remap, adjust_unit, ocean
from preprocessing import TARGET_LATLON
from variables import VARS

# Configure warnings and loggings
warnings.filterwarnings(action='ignore')
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

# ------------------------------------------------------------------------------
# Define helper functions
# -----------------------
def _get_arguments():
    if len(sys.argv) < 8:
        print(
            "Usage: python script.py <exp> <var> <start_day> <end_day> " +
            "<granularity> <outdir> <n_jobs>"
            )
        sys.exit(1)
    return sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], \
        sys.argv[6], sys.argv[7]


# ------------------------------------------------------------------------------
# Define main functions
# ---------------------
def main():
    exp, var, start_date, end_date, granularity, odir, n_jobs = _get_arguments()
    analysis_times = [
        np.datetime64(t) for t in date_range(
            np.datetime64(start_date), np.datetime64(end_date), freq='MS',
            )
        ]
    data = read_in_hp_data(exp, VARS[var]['dim'], granularity)
        
    # MAIN LOGICAL LOOP
    for i in range (len(analysis_times)-1):
        # time settings
        start_t = analysis_times[i]
        end_t = analysis_times[i+1]
        time_window = (start_t, end_t - np.timedelta64(1, 'ns'))
        file_dstring = \
            f"{dtutil.np_datetime2file_datestr(start_t)}-" + \
            f"{dtutil.np_datetime2file_datestr(end_t)}"
        logging.info(f"Processing {start_t} to {end_t}")

        # Set output file and check its existence
        ofile=f"{odir}/{exp}_tropical_{var}_{file_dstring}.nc"
        if os.path.exists(ofile):
            logging.info(f"  Skipping {ofile}, already exists.")
            continue
        
        # Select and preprocess data for the current time range
        data_sample = data[var].sel(time=slice(*time_window)).where(ocean(data))
        data_sample = adjust_unit(data_sample, exp, var)
        data_sample = data_sample.astype(
            np.float32 if data_sample.dtype == np.float64 else data_sample.dtype
            ).compute()
        logging.info("  Finished computing of data sample, ready to remap.")

        data_sample_latlon = Parallel(n_jobs=n_jobs)(
            delayed(process_one_timestep_remap)(
                data_sample, time, TARGET_LATLON
                ) for time in range(data_sample.sizes["time"])
            )
        data_sample_latlon = xr.concat(data_sample_latlon, dim="time")

        # Save latlon as netCDF file
        data_sample_latlon = data_sample_latlon.assign_attrs(VARS[var]['attrs'])
        data_sample_latlon.coords["time"] = \
            data_sample_latlon.time.assign_attrs(_FillValue=-1.)
        data_sample_latlon = data_sample_latlon.drop(
            ['crs', 'cell'], errors="ignore",
            )
        data_sample_latlon.to_netcdf(ofile)
        logging.info("  Finished remapping.")

        # Get memory info
        mem = psutil.virtual_memory()
        used_mem_gb = (mem.total - mem.available) / (1024 ** 3)
        free_mem_gb = mem.available / (1024 ** 3)

        print(f"  Used memory: {used_mem_gb:.2f} GB")
        print(f"  Free memory: {free_mem_gb:.2f} GB")

        # Clean up
        del data_sample, data_sample_latlon
        gc.collect()


if __name__ == "__main__":
    main()