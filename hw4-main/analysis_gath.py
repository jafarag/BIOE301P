import os 

SES_ID = os.environ['PART_ID']
HOME = os.environ['HOME']

import numpy as np
if SES_ID == "1":
	fft_tot = np.zeros((24,27811))
else: 
	fft_tot = np.zeros((24,27811)) #14576897))
print('ok')
for i in range(24):
	print(i)
	num = int(i)
	os.chdir(HOME+'/hw4/ses'+SES_ID+'/')
	fft_tot[i,:] = np.load('ch'+str(num)+'.npy')
os.chdir(HOME+'/hw4/data')
np.save('ses'+SES_ID+'_log.npy',fft_tot)


