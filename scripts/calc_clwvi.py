import logging
import warnings
from preprocessing import calc_quantity

# Configure warnings and loggings
warnings.filterwarnings(action='ignore')
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

VARS_NEEDED_CLWVI = ['cllvi', 'clivi']

def main():
    calc_quantity('clwvi', VARS_NEEDED_CLWVI)

if __name__ == "__main__":
    main()
