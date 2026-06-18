#!/bin/bash

# user settings
EXP="ngc5004"
VARLIST="ua va ta hus wa clw cli pfull uas vas sfcwind pr ps ts rlut prw hfss hfls cllvi clivi tas hus2m"
START_DATE="2020-01-01T00:00:00Z"
END_DATE="2023-01-01T00:00:00Z"
GRANULARITY="P1D"
N_JOBS=32

BASEDIR=/home/m/m300738/project_TRR181L4
RUNFILE=${BASEDIR}/scripts/remap_var.py

# Run the jobs
for VAR in ${VARLIST}; do
    OUTDIR=${BASEDIR}/data/${EXP}_pp/${GRANULARITY}/${VAR}_latlon
    mkdir -p ${OUTDIR}
    sbatch <<EOF
#!/bin/bash
#SBATCH --account=mh0731
#SBATCH --partition=compute
#SBATCH --constraint=256G
#SBATCH --mem=0
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1
#SBATCH --time=08:00:00
#SBATCH --job-name="remap_var"
#SBATCH --output=LOG/remap_var.%j.out
#SBATCH --error=LOG/remap_var.%j.out
#SBATCH --export=ALL

source ~/.bashrc
micromamba activate TRR181L4

export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

python3 "${RUNFILE}" "${EXP}" "${VAR}" "${START_DATE}" "${END_DATE}" "${GRANULARITY}" "${OUTDIR}" "${N_JOBS}"
EOF
done
