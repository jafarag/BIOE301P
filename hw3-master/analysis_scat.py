DATA_RAW = os.environ['DATA_RAW']
DATASET_ID = os.environ['SLURM_ARRAY_TASK_ID']
DATA_DERIV = os.environ['DATA_DERIV']
SES_ID = os.environ['PART_ID']
HOME = os.environ['HOME']
import h5py
import numpy as np

f = h5py.File('Reggie_ses'+SES_ID+'.h5', 'r')
m1_1 = f['ses1']['M1']
m1_fft= np.real(np.fft.fft(m1_1[:,DATASET_ID]))
np.save(HOME+'/hw3/ses'+SES_ID+'/ch'+DATASET_ID+'.npy')

