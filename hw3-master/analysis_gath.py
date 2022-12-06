scr = os.environ['SCRATCH']
DATA_RAW = os.environ['DATA_RAW']
DATASET_ID = os.environ['SLURM_ARRAY_TASK_ID']
DATA_DERIV = os.environ['DATA_DERIV']
SES_ID = os.environ['PART_ID']
HOME = os.environ['HOME']

import numpy as np

fft_tot = np.zeros(96)
for i in range(int(DATASET_ID)):
	fft_tot[i] = np.load(HOME+'/hw3/ses'+SES_ID+'/ch'+str(i)+'.npy')
np.save(HOME+'/hw3/ses'+SES_ID+'.npy')


