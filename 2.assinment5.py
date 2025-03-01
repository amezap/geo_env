import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import os
import geopandas as gpd

# Part 2: Data Visualization and Inspection
#dset = xr.open_dataset(r'C:\Users\aleja\geo_env\file-5\GRIDSAT-B1.2009.11.25.06.v02r01.nc')
#R = np.array(dset.variables['irwin_cdr']).squeeze()
#IR = np.flipud(IR)
#IR = IR * 0.01 + 200
#IR = IR - 273.15
#plt.figure(1)
#plt.imshow(IR, extent=[-180.035, 180.035, -70.035, 70.035], aspect='auto')
#cbar = plt.colorbar()
#cbar.set_label('Brightness temperature (degrees Celsius)')
#jeddah_lat = 21.5
#jeddah_lon = 39.2
#plt.scatter(jeddah_lon, jeddah_lat, color='red', marker='o', label='Jeddah')
#plt.legend()
#plt.show()

#Part 2: Data Visualization and Inspection (Question 12): 

archivo1 = r'C:\Users\aleja\geo_env\file-5\GRIDSAT-B1.2009.11.25.00.v02r01.nc'
archivo2 = r'C:\Users\aleja\geo_env\file-5\GRIDSAT-B1.2009.11.25.03.v02r01.nc'
archivo3 = r'C:\Users\aleja\geo_env\file-5\GRIDSAT-B1.2009.11.25.06.v02r01.nc'
archivo4 = r'C:\Users\aleja\geo_env\file-5\GRIDSAT-B1.2009.11.25.09.v02r01.nc'
archivo5 = r'C:\Users\aleja\geo_env\file-5\GRIDSAT-B1.2009.11.25.12.v02r01.nc'

dset1 = xr.open_dataset(archivo1)
dset2 = xr.open_dataset(archivo2)
dset3 = xr.open_dataset(archivo3)
dset4 = xr.open_dataset(archivo4)
dset5 = xr.open_dataset(archivo5)

jeddah_lat = 21.5
jeddah_lon = 39.2

# get minimun temperature one dataset
def get_min_temp(dset):
    lat_idx = np.abs(dset['lat'] - jeddah_lat).argmin()
    lon_idx = np.abs(dset['lon'] - jeddah_lon).argmin()
    temp = dset['irwin_cdr'][:, lat_idx, lon_idx] * 0.01 + 200 - 273.15  # Convert to °C
    return temp.min().values

# Get minimun temperature each dataset
temps_min = {
    "00 UTC": get_min_temp(dset1),
    "03 UTC": get_min_temp(dset2),
    "06 UTC": get_min_temp(dset3),
    "09 UTC": get_min_temp(dset4),
    "12 UTC": get_min_temp(dset5)
}

# Find hour with minimun temperature
hora_min = min(temps_min, key=temps_min.get)

print(f" {hora_min} with {temps_min[hora_min]:.2f} °C")


#Part 3: Rainfall Estimation
folderPath = r'C:\Users\aleja\geo_env\file-5'  
files = os.listdir(folderPath)
cumulate = None

for i in files:
    dset = xr.open_dataset(fr'C:\Users\aleja\geo_env\file-5\{i}')
    jeddah_ir = dset['irwin_cdr'].sel(lat=slice(18, 28), lon=slice(35,45)).squeeze()
    jeddah_ir = np.flipud(jeddah_ir)
    jeddah_ir = jeddah_ir * 0.01 + 200
    temp = -3.6382 * 0.01 * xr.apply_ufunc(np.power, jeddah_ir, 1.2)
    rainfall = 3 * (1.1183 * 10**11 * xr.apply_ufunc(np.exp, temp))
    print(f'The maximum rainfall in {i} is {rainfall.max()} mm')

    if cumulate is None:
        cumulate = rainfall
    else:
        cumulate = cumulate + rainfall

plt.figure(1)
plt.imshow(cumulate, extent=[35, 45, 18, 28], aspect='equal') 
x_label = 'Longitude'
y_label = 'Latitude'
plt.xlabel(x_label)
plt.ylabel(y_label)
cbar = plt.colorbar()
cbar.set_label('Cumulate Rainfall (mm)')
jeddah_lat = 21.5
jeddah_lon = 39.2
plt.scatter(jeddah_lon, jeddah_lat, color='red', marker='o', label='Jeddah')
plt.show()