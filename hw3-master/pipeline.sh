#!/bin/bash

source /farmshare/home/classes/bioe/301p/bash_profile

export DATA_RAW="$SCRATCH/data_raw"
export DATA_DERIV="$SCRATCH/data_deriv"
export PART_ID="1"
echo "PartID"


cd $HOME/hw3 
JOB_1=$(sbatch --export=ALL --parsable -c 1 --mem-per-cpu 1G -t 0:10:0  --wrap "./wget_file.sh")
echo "Job1 done"
JOB_2=$(sbatch --export=ALL --array=1,2 --parsable -d afterok:$JOB_1 -c 2 --mem-per-cpu 1G -t 0:30:0 --wrap "$CESP convh5py.py")
echo "Job2 done"
JOB_3A=$(sbatch --export=ALL,PART_ID="1" --array=1-96 --parsable -d afterok:$JOB_2 -c 2 --mem-per-cpu 1G -t 0:30:0  --wrap "$CESP analysis_scat.py")
echo "z"
JOB_3B=$(sbatch --export=ALL,PART_ID="2" --array=1,96 --parsable -d afterok:$JOB_2 -c 2 --mem-per-cpu 1G -t 0:30:0  --wrap "$CESP analysis_scat.py")
echo "y"
JOB_4A=$(sbatch --export=ALL,PART_ID="1" --array=96 --parsable -d afterok:$JOB_3A -c 2 --mem-per-cpu 1G -t 0:30:0  --wrap "$CESP analysis_gath.py")
echo "x"
JOB_4B=$(sbatch --export=ALL,PART_ID="2" --array=96 --parsable -d afterok:$JOB_3B -c 2 --mem-per-cpu 1G -t 0:30:0  --wrap "$CESP analysis_gath.py")
echo "w"
JOB_5=$(sbatch  --export=ALL --parsable -d afterok:$JOB_4A,$JOB_4B -c 2 --mem-per-cpu 1G -t 0:30:0  --wrap "$CESP visualize_conquer.py")
echo "v"
JOB_6=$(sbatch   --export=ALL --parsable -d afterok:$JOB_5 --wrap "$CESP rclone.py")
