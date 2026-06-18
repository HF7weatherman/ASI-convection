import logging
import warnings
from preprocessing import calc_quantity

# Configure warnings and loggings
warnings.filterwarnings(action='ignore')
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

VARS_NEEDED = ['ta', 'hus', 'clw', 'cli', 'zg']

def main():
    calc_quantity('mse_e', VARS_NEEDED)

if __name__ == "__main__":
    main()