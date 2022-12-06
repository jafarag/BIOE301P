import os

DATA_RAW = os.environ['DATA_RAW']
DATASET_ID = os.environ['SLURM_ARRAY_TASK_ID']
DATA_DERIV = os.environ['DATA_DERIV']
SES_ID = os.environ['PART_ID']
HOME = os.environ['HOME']
import h5py
import numpy as np

f = h5py.File(DATA_DERIV+'/Reggie_ses'+SES_ID+'.h5', 'r')
m1_1 = f['ses']['LFP_M1']
print(DATASET_ID)
m1_fft= np.log(np.real(np.fft.fft(m1_1[:,int(DATASET_ID)-1])))
dset = str(int(DATASET_ID)-1)
np.save(HOME+'/hw4/ses'+SES_ID+'/ch'+dset+'.npy',m1_fft[:27811])

