from netCDF4 import Dataset, MFDataset, num2date
import pandas as pd
import numpy as np
import metpy.calc as calc
#from metpy.calc import most_unstable_cape_cin, most_unstable_parcel,pressure_to_height_std,parcel_profile_with_lcl
import metpy.calc as mpcalc
from metpy.units import units
import metpy.constants as mpconsts
import matplotlib.pyplot as plt

fid = Dataset("/global/homes/z/zhangtao/CPS_trigger/data/goamazon/continuous_at_goamazon.nc")

t = fid.variables['T'][:] #K
print(t.shape)
lev = fid.variables['lev'][:] #mba
print(lev.shape)
q = fid.variables['q'][:] / 1000.0 #g/kg
print(q.shape)

epsilon = 0.622
e = lev * q / (q + epsilon)

Td = (243.5 * np.log(e/6.112)) / (17.67 - np.log(e/6.112)) + 273.15

cape = np.zeros([t.shape[0]])
cin = np.zeros([t.shape[0]])
mx = np.zeros([t.shape[0]])
tmp = np.zeros([t.shape[0]])
print(cape.shape)
print(cape[1])


for i in range(100):
    #lev1 = lev[5:42].tolist() * units.hPa
    #t1 = t[0,5:42].tolist() * units.kelvin
    #Td1 = Td[0,5:42].tolist() * units.kelvin

    lev1 = lev[5:].tolist() * units.hPa
    t1 = t[i,5:].tolist() * units.kelvin
    Td1 = Td[i,5:].tolist() * units.kelvin
    
    a,b = calc.most_unstable_cape_cin(lev1, t1, Td1)
    cape[i] = a.magnitude
    cin[i] = b.magnitude


np.savetxt("cape_metpy.txt", cape)
