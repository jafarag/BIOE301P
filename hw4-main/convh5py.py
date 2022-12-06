import os
import numpy as np
import h5py
from pynwb import NWBFile, TimeSeries, get_manager, NWBHDF5IO, validate

#scr = os.environ['SCRATCH']
DATA_RAW= os.environ['DATA_RAW']
DATASET_ID = os.environ['SLURM_ARRAY_TASK_ID']
DATA_DERIV = os.environ['DATA_DERIV']
print(DATA_RAW)
os.chdir(DATA_RAW)
print(os.listdir())
#print(DATASET_ID)
#print(str(DATASET_ID))
sesname = 'Reggie_ses' + str(DATASET_ID) + '.bin'
print(sesname)
raw_io = NWBHDF5IO(sesname, 'r')
nwb_in = raw_io.read()
nwb_proc = nwb_in.copy()
m1_1 = nwb_proc.processing['ecephys']['LFP']['M1_1'].data
grain_chunk = (100000,1)
os.chdir(DATA_DERIV)
sesnameh5 = 'Reggie_ses'+ str(DATASET_ID) +'.h5'
print(sesnameh5)
sesh5file = h5py.File(sesnameh5,'w') #create h5file
sesh5group = sesh5file.create_group('ses') #create group
h5dset = sesh5group.create_dataset(name = 'LFP_M1', dtype=np.uint16, chunks=grain_chunk, compression='gzip', scaleoffset=True, shuffle=True, data=m1_1) #create dataset for each AP/LFP file
sesh5file.close()

