import logging
import warnings
from preprocessing import calc_quantity

# Configure warnings and loggings
warnings.filterwarnings(action='ignore')
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

VARS_NEEDED_BF = ['tas', 'hus2m', 'ps', 'hfss', 'hfls']

def main():
    calc_quantity('sfc_bf', VARS_NEEDED_BF)

if __name__ == "__main__":
    main()
