# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 20:18:08 2022

@author: User
"""
import numpy as np
import h5py

fname_meta = [1268746, 1268748, 1268764,  1268765, 1268769,  1268771,1268774] #names of the metafiles for the recording

title_meta = ['Pt03_lf_meta', 'Pt03_ap_meta', 'Pt01_ap_meta','Pt01_lf_meta','Pt02_ap_meta','Pt02_lf_meta','README'] #original names of the metafiles to use in the h5 format
fname = ['1268767','1268768','1268766','1268772','1268770','1268773','1268763','1268747','1268745']#files in /hmnpix folder that was shown earlier
title = ['Pt01_ap','Pt01_lf','Pt01_aligned','Pt02_ap','Pt02_lf','Pt02_aligned','Pt03_ap','Pt03_lf','Pt03_aligned'] #original names of the recording files to use in the h5 format
f_shape = [(385,50029384),(385,4169116),(384,30120002),(385,52398986), (385,4366584),(384,38700002),(385,35176734),(385,2931396),(384,35160000)]#shaes of all recording data, lost when first recreated from bin
chunksize = [(384,6000), (384,6000),(384,6000),(384,6000),(384,6000),(384,6000),(384,6000),(384,6000),(384,6000)] #original chunksize
chunksize2 = (3,12000) #second chunk size
chunksize3 = (3,240000) #third chunk size, hint: reason it is 3 is because it would take too much time to load
grain_chunk = (1,4800000) #grain chunk size, one channel
h5file = h5py.File('humnpix_r_grain.h5','w') #create h5file
h5group = h5file.create_group('humnpix') #create group
for j in range(len(fname_meta)): #loop for metadata
    bdata_meta = np.memmap(str(fname_meta[j])) #load .meta files
    h5dset_meta = h5group.create_dataset(name = title_meta[j], compression='gzip', scaleoffset=True, shuffle=True, data=bdata_meta) #create dataset for each meta file
for i in range(len(fname)): #loop for recording data
    bdata = np.memmap(fname[i]) #load recording data
    bbda = np.reshape(bdata,f_shape[i]) #reshape data
    h5dset = h5group.create_dataset(name =title[i], dtype=np.uint16, chunks=grain_chunk, compression='gzip', scaleoffset=True, shuffle=True, data=bbda[0:3,:]) #create dataset for each AP/LFP file
    print(title[i])
h5file.close()