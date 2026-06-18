VARS = {
    'ts': {
        'dim': '2d',
        'attrs': {
            'standard_name': 'ts',
            'units': 'K',
            'short_name': '',
            'long_name': 'surface temperature',
            },
        'label': 'SST / $^{\circ}$C',
        },
    'ts_abs_grad': {
        'label': '|SST gradient| / K$\,$(100$\,$km$^{-1}$)',
        },
    'ts_laplacian': {
        'label': 'SST Laplacian / K$\,$(100$\,$km$^{-2}$)',
        },
    'tas': {
        'dim': '2d',
        'attrs': {
            'standard_name': 'tas',
            'units': 'K',
            'short_name': '',
            'long_name': 'temperature in 2m',
            },
        },
    'uas': {
        'dim': '2d',
        'attrs': {
            'standard_name': 'uas',
            'units': 'm s-1',
            'short_name': 'zonal wind',
            'long_name': 'zonal wind in 10m',
            },
        },
    'vas': {
        'dim': '2d',
        'attrs': {
            'standard_name': 'vas',
            'units': 'm s-1',
            'short_name': 'meridional wind',
            'long_name': 'meridional wind in 10m',
            },
        },
    'pr': {
        'dim': '2d',
        'attrs': {
            'standard_name': 'pr',
            'units': 'mm day-1',
            'short_name': 'precipitation rate',
            'long_name': 'precipitation rate',
            },
        'label': 'precip. rate / mm$\,$day$^{-1}$',
        },
    'prw': {
        'dim': '2d',
        'attrs': {
            'standard_name': 'prw',
            'units': 'kg m-2',
            'short_name': 'precipitable water',
            'long_name': 'water vapor path',
            },
        },
    'hfls': {
        'dim': '2d',
        'attrs': {
            'standard_name': 'hfls',
            'units': 'W m-2',
            'short_name': 'latent heat flux',
            'long_name': 'latent heat flux',
            },
        'label': 'latent heat flux / W$\,$m$^{-2}$',
        },
    'hfss': {
        'dim': '2d',
        'attrs': {
            'standard_name': 'hfss',
            'units': 'W m-2',
            'short_name': 'sensible heat flux',
            'long_name': 'sensible heat flux',
            },
        },
    'hus2m': {
        'dim': '2d',
        'attrs': {
            'standard_name': 'hus2m',
            'units': 'kg kg-1',
            'short_name': 'surface specific humidity',
            'long_name': 'specific humidity in 2m',
            },
        },
    'rlut': {
        'dim': '2d',
        'attrs': {
            'standard_name': 'rlut',
            'units': 'W m-2',
            'short_name': 'toa outgoing lw flux',
            'long_name': 'toa outgoing longwave radiation',
            },
        'label': 'TOA OLR / W$\,$m$^{-2}$',
        },
    'cllvi': {
        'dim': '2d',
        'attrs': {
            'standard_name': 'cllvi',
            'units': 'kg m-2',
            'short_name': 'cloud liquid water path',
            'long_name': 'cloud liquid water path',
            },
        },
    'clivi': {
        'dim': '2d',
        'attrs': {
            'standard_name': 'clivi',
            'units': 'kg m-2',
            'short_name': 'cloud ice path',
            'long_name': 'cloud ice path',
            },
        },
    'clwvi': {
        'dim': '2d',
        'attrs': {
            'standard_name': 'clwvi',
            'units': 'kg m-2',
            'short_name': 'cloud water path',
            'long_name': 'cloud water path',
            },
        },
    'sfcwind': {
        'dim': '2d',
        'attrs': {
            'standard_name': 'sfcwind',
            'units': 'm s-1',
            'short_name': 'surface windspeed',
            'long_name': 'windspeed at 10m',
            },
        'label': 'absolute sfc. wind speed / m$\,$s$^{-1}$',
        },
    'sfcwind_conv':{
        'dim': '2d',
        'attrs': {
            'standard_name': 'sfcwind_conv',
            'units': 's-1',
            'short_name': 'surface wind convergence',
            'long_name': 'wind convergence in 10m',
            },
        'label': 'sfc. wind convergence / s$^{-1}$',
        },
    'sfcwind_conv_comp':{
        'dim': '2d',
        },
    'uas_conv':{
        'dim': '2d',
        'attrs': {
            'standard_name': 'uas_conv',
            'units': 's-1',
            'short_name': 'zonal wind convergence',
            'long_name': 'zonal wind convergence in 10m',
            },
        'label': 'zonal sfc. wind convergence / s$^{-1}$',
        },
    'vas_conv':{
        'dim': '2d',
        'attrs': {
            'standard_name': 'vas_conv',
            'units': 's-1',
            'short_name': 'meridional wind convergence',
            'long_name': 'meridional wind convergence in 10m',
            },
        'label': 'meridional sfc. wind convergence / s$^{-1}$',
        },
    'sfc_rho': {
        'dim': '2d',
        'attrs': {
            'standard_name': 'sfc_density',
            'units': 'kg m-3',
            'short_name': 'surface density',
            'long_name': 'surface density',
            },
        },
    'sfc_bf': {
        'dim': '2d',
        'attrs': {
            'standard_name': 'sfc_bf',
            'units': 'm2 s-3',
            'short_name': 'surface buoyancy flux',
            'long_name': 'surface buoyancy flux',
            },
        },
    'ps': {
        'dim': '2d',
        'attrs': {
            'standard_name': 'ps',
            'units': 'Pa',
            'short_name': 'surface pressure',
            'long_name': 'surface pressure',
            },
        },
    'ta': {
        'dim': '3d',
        'attrs': {
            'standard_name': 'ta',
            'units': 'K',
            'short_name': 'temperature',
            'long_name': 'air temperature',
            },
        },
    'ua': {
        'dim': '3d',
        'attrs': {
            'standard_name': 'ua',
            'units': 'm s-1',
            'short_name': 'zonal wind',
            'long_name': 'zonal wind',
            },
        },
    'va': {
        'dim': '3d',
        'attrs': {
            'standard_name': 'va',
            'units': 'm s-1',
            'short_name': 'meridional wind',
            'long_name': 'meridional wind',
            },
        },
    'hus': {
        'dim': '3d',
        'attrs': {
            'standard_name': 'hus',
            'units': 'kg kg-1',
            'short_name': 'specific humidity',
            'long_name': 'specific humidity',
            },
        },
    'clw': {
        'dim': '3d',
        'attrs': {
            'standard_name': 'clw',
            'units': 'kg kg-1',
            'short_name': 'specific cloud water content',
            'long_name': 'specific cloud water content',
            },
        },
    'cli': {
        'dim': '3d',
        'attrs': {
            'standard_name': 'cli',
            'units': 'kg kg-1',
            'short_name': 'specific cloud ice content',
            'long_name': 'specific cloud ice content',
            },
        },
    'wa': {
        'dim': '3d',
        'attrs': {
            'standard_name': 'wa',
            'units': 'm s-1',
            'short_name': 'vertical velocity',
            'long_name': 'upward air velocity',
            },
        },
    'wap': {
        'dim': '3d',
        'attrs': {
            'standard_name': 'wap',
            'units': 'Pa s-1',
            'short_name': 'vertical pressure velocity',
            'long_name': 'upward air velocity',
            },
        },
    'rho': {
        'dim': '3d',
        'attrs': {
            'standard_name': 'rho',
            'units': 'kg m-3',
            'short_name': 'density',
            'long_name': 'air density',
            },
        },
    'pfull': {
        'dim': '3d',
        'attrs': {
            'standard_name': 'pfull',
            'units': 'Pa',
            'short_name': 'air pressure',
            'long_name': 'air pressure at full levels',
            },
        },
    'mse_e': {
        'dim': '3d',
        'attrs': {
            'standard_name': 'mse_e',
            'units': 'J kg-1',
            'short_name': 'moist static energy',
            'long_name': 'equivalent moist static energy',
            },
        },
    'mse_sfc': {
        'dim': '2d',
        'attrs': {
            'standard_name': 'mse_sfc',
            'units': 'J kg-1',
            'short_name': 'moist static energy',
            'long_name': 'surface moist static energy',
            },
        },
    'mse_sfc_ifs': {
        'dim': '2d',
        'attrs': {
            'standard_name': 'mse_sfc',
            'units': 'J kg-1',
            'short_name': 'moist static energy',
            'long_name': 'surface moist static energy',
            },
        },
    }
