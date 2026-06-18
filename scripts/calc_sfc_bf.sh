#!/bin/bash

# user settings
EXP="ngc5004"
START_DATE="2020-01-01T00:00:00Z"
END_DATE="2021-07-01T00:00:00Z"
GRANULARITY="P1D"
N_JOBS=32

BASEDIR=/home/m/m300738/project_TRR181L4
RUNFILE=${BASEDIR}/scripts/calc_sfc_bf.py

# Run the jobs
OUTDIR=${BASEDIR}/data/${EXP}_pp/${GRANULARITY}
mkdir -p ${OUTDIR}/sfc_bf_latlon
sbatch <<EOF
#!/bin/bash
#SBATCH --account=mh0731
#SBATCH --partition=compute
#SBATCH --constraint=512G
#SBATCH --mem=0
#SBATCH --ntasks-per-node=128
#SBATCH --nodes=1
#SBATCH --time=08:00:00
#SBATCH --job-name="calc_sfc_bf"
#SBATCH --output=LOG/calc_sfc_bf.%j.out
#SBATCH --error=LOG/calc_sfc_bf.%j.out
#SBATCH --export=ALL

source ~/.bashrc
micromamba activate TRR181L4

python3 "${RUNFILE}" "${EXP}" "${START_DATE}" "${END_DATE}" "${GRANULARITY}" "${OUTDIR}" "${N_JOBS}"
EOF
