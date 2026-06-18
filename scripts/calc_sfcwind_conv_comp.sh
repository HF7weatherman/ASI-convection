#!/bin/bash

# user settings
EXP="ifs_tco3999-ng5_rcbmf"
START_DATE="2020-01-01T00:00:00Z"
END_DATE="2021-03-01T00:00:00Z"
GRANULARITY="P1D"
N_JOBS=32

BASEDIR=/home/m/m300738/project_TRR181L4
RUNFILE=${BASEDIR}/scripts/calc_sfcwind_conv_comp.py

# Run the jobs
OUTDIR=${BASEDIR}/data/${EXP}_pp/${GRANULARITY}
mkdir -p ${OUTDIR}/uas_conv_latlon
mkdir -p ${OUTDIR}/vas_conv_latlon
sbatch <<EOF
#!/bin/bash
#SBATCH --account=bm1500
#SBATCH --partition=compute
#SBATCH --constraint=512G
#SBATCH --mem=0
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1
#SBATCH --time=02:00:00
#SBATCH --job-name="calc_sfcwind_conv_comp"
#SBATCH --output=LOG/calc_sfcwind_conv_comp.%j.out
#SBATCH --error=LOG/calc_sfcwind_conv_comp.%j.out
#SBATCH --export=ALL

source ~/.bashrc
micromamba activate TRR181L4

export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

python3 "${RUNFILE}" "${EXP}" "${START_DATE}" "${END_DATE}" "${GRANULARITY}" "${OUTDIR}" "${N_JOBS}"
EOF
