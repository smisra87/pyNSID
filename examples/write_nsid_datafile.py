"""
================================================================================
01. Writing a sid Dataset to file in NSID format
================================================================================

**Gerd Duscher**

08/24/2020

**this file shows how to store quickly store a sid Dataset to NSID format**
"""
########################################################################################################################
# Introduction
# -------------
# Saving a data and their metadata to file in a comprehensive way after aquisition, as intermediate or final results
# is at the core of any data analysis.
# The NSID data format is an attempt to meet those requirement as painless and universal as possible.
# In the following, we will create a sid.Dataset from a numpy array, which we will store as NSID format in its HDF5 file
########################################################################################################################

# Import numpy and h5py as the basis for the following operation
import numpy as np
import h5py

# All data analysis in pycroscopy is based on sid.Datasets
import sidpy as sid

# Utilize the NSID package for writing
import sys
sys.path.append('../pyNSID/')
import pyNSID as nsid

########################################################################################################################
# Making a sid Dataset (which is based on dask) is described in the sid Documentation
# Here, we just make a basic sid.Dataset from a numpy array

data_set = sid.Dataset.from_array(np.zeros([4, 5, 10]), name='zeros')
print(data_set)

########################################################################################################################
# Creating a HDF5 file and groups using h5py is described in the h5py_primer in this directory

h5_file = h5py.File("zeros.hf5")
if 'Measurement_000' in h5_file:
    del h5_file['Measurement_000/Channel_000']
h5_group = h5_file.create_group('Measurement_000/Channel_000')
########################################################################################################################

########################################################################################################################
# Write this sid.Dataset to file with one simple command
# We use the sid hdf_uilities to look at the created h5py file structure
#
# Please note that the NSID dataset has the dimensions (a,b,c) attached as attributes,
# which are accessible through "h5_dataset.dims". Look at hf5py for more information.
#
# The HDF55 group "original_metadata" contains contain all the information of the original file as a dictionary type
# in the attributes original_metadata.attrs (here empty)

h5_dataset = nsid.write_nsid_dataset(data_set, h5_group, main_data_name='zeros')

sid.hdf.hdf_utils.print_tree(h5_file)

print(h5_dataset.dims)
print(h5_dataset.name)
########################################################################################################################


########################################################################################################################
# Read NSID Dataset into sid.Dataset with a simple command

sid_dataset = nsid.read_nsid_dataset(h5_group['zeros'])
print(sid_dataset.a)
########################################################################################################################