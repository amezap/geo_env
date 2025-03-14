import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import os

# Ruta a la carpeta con los archivos netCDF
data_path = r"C:\Users\aleja\geo_env\7\datos7\Precipitation"

# Lista para almacenar los datos mensuales de precipitación
all_years_precip_monthly = []

# Leer datos de todos los años
for year in range(2000, 2021):
    file_path = os.path.join(data_path, f"era5_OLR_{year}_total_precipitation.nc")
    
    try:
        ds = xr.open_dataset(file_path)
        # Asegurarse de que 'valid_time' esté en formato datetime
        ds['valid_time'] = pd.to_datetime(ds['valid_time'].values)

        # Leer la variable de precipitación
        tp = ds['tp']

        # Resampleo mensual y convertir de metros a mm (1 m = 1000 mm)
        precip_monthly = tp.resample(valid_time='ME').sum() * 1000
        precip_monthly2 = precip_monthly / 100
        
        # Añadir los datos mensuales a la lista
        all_years_precip_monthly.append(precip_monthly2)

    except FileNotFoundError:
        print(f"Archivo para el año {year} no encontrado.")
    except Exception as e:
        print(f"Error al procesar el archivo para el año {year}: {e}")

# Concatenar todos los datos mensuales en un solo DataFrame
if all_years_precip_monthly:
    df_precip = xr.concat(all_years_precip_monthly, dim='valid_time').to_dataframe().reset_index()

    # Filtrar entre 2000 y 2020
    df_precip = df_precip[(df_precip['valid_time'].dt.year >= 2000) & 
                          (df_precip['valid_time'].dt.year <= 2020)]

    # Crear el gráfico
    fig, ax = plt.subplots(figsize=(16, 6))

    # Línea de precipitación mensual
    ax.plot(df_precip['valid_time'], df_precip['tp'], label='Monthly Precipitation', color='blue')

    # Etiquetas y formato
    ax.set_title('Monthly Precipitation (2000-2020)', fontsize=16)
    ax.set_xlabel('Date', fontsize=12)  # Mostrar fechas en el eje X
    ax.set_ylabel('Precipitation (mm)', fontsize=12)
    ax.legend()
    ax.grid(True)

    # Formato del eje X para mostrar fechas como Año-Mes
    ax.xaxis.set_major_locator(plt.MaxNLocator(12))
    ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)

    # Mostrar el gráfico
    #plt.show()

else:
    print("No se encontraron datos válidos para el rango de años especificado.")

############# end precipitation part 
# Ruta a la carpeta con los archivos netCDF para evaporación
data_path = r"C:\Users\aleja\geo_env\7\datos7\Total_Evaporation"

# Lista para almacenar los datos mensuales de evaporación
all_years_evap_monthly = []

# Leer datos de todos los años
for year in range(2000, 2021):
    file_path = os.path.join(data_path, f"era5_OLR_{year}_total_evaporation.nc")
    
    try:
        ds = xr.open_dataset(file_path)
        # Asegurarse de que 'valid_time' esté en formato datetime
        ds['valid_time'] = pd.to_datetime(ds['valid_time'].values)

        # Leer la variable de evaporación (nombre corregido)
        ev = ds['e']

        # Resampleo mensual y convertir de metros a mm (1 m = 1000 mm)
        evap_monthly = ev.resample(valid_time='ME').sum() * -1000
        
        # Dividir entre 100 para ajustar escala (de mm a cm)
        #evap_monthly = evap_monthly / 100
        
        # Añadir los datos mensuales a la lista
        all_years_evap_monthly.append(evap_monthly)

    except FileNotFoundError:
        print(f"Archivo para el año {year} no encontrado.")
    except Exception as e:
        print(f"Error al procesar el archivo para el año {year}: {e}")

# Concatenar todos los datos mensuales en un solo DataFrame
if all_years_evap_monthly:
    df_evap = xr.concat(all_years_evap_monthly, dim='valid_time').to_dataframe().reset_index()

    # Filtrar entre 2000 y 2020
    df_evap = df_evap[(df_evap['valid_time'].dt.year >= 2000) & 
                      (df_evap['valid_time'].dt.year <= 2020)]

    # Crear el gráfico
    fig, ax = plt.subplots(figsize=(16, 6))

    # Línea de evaporación mensual
    ax.plot(df_evap['valid_time'], df_evap['e'], label='Monthly Total Evaporation', color='green')

    # Etiquetas y formato
    ax.set_title('Monthly Total Evaporation (2000-2020)', fontsize=16)
    ax.set_xlabel('Date', fontsize=12)  # Mostrar fechas en el eje X
    ax.set_ylabel('Evaporation (mm)', fontsize=12)  # Nueva unidad en centímetros
    ax.legend()
    ax.grid(True)

    # Formato del eje X para mostrar fechas como Año-Mes
    ax.xaxis.set_major_locator(plt.MaxNLocator(12))
    ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)

    # Mostrar el gráfico
    #plt.show()

else:
    print("No se encontraron datos válidos para el rango de años especificado.")
########end 7.2
# Ruta a la carpeta con los archivos netCDF para runoff
data_path = r"C:\Users\aleja\geo_env\7\datos7\Runoff"

# Lista para almacenar los datos mensuales de runoff
all_years_runoff_monthly = []

# Leer datos de todos los años
for year in range(2000, 2021):
    file_path = os.path.join(data_path, f"ambientera5_OLR_{year}_total_runoff.nc")
    
    try:
        ds = xr.open_dataset(file_path)
        # Asegurarse de que 'valid_time' esté en formato datetime
        ds['valid_time'] = pd.to_datetime(ds['valid_time'].values)

        # Leer la variable de runoff (nombre correcto)
        ro = ds['ro']

        # Resampleo mensual y convertir de metros a mm (1 m = 1000 mm)
        runoff_monthly = ro.resample(valid_time='ME').sum() * 1000
        
        # Dividir entre 100 para ajustar escala (de mm a cm)
        runoff_monthly = runoff_monthly / 100
        
        # Añadir los datos mensuales a la lista
        all_years_runoff_monthly.append(runoff_monthly)

    except FileNotFoundError:
        print(f"Archivo para el año {year} no encontrado.")
    except Exception as e:
        print(f"Error al procesar el archivo para el año {year}: {e}")

# Concatenar todos los datos mensuales en un solo DataFrame
if all_years_runoff_monthly:
    df_runoff = xr.concat(all_years_runoff_monthly, dim='valid_time').to_dataframe().reset_index()

    # Filtrar entre 2000 y 2020
    df_runoff = df_runoff[(df_runoff['valid_time'].dt.year >= 2000) & 
                          (df_runoff['valid_time'].dt.year <= 2020)]

    # Crear el gráfico
    fig, ax = plt.subplots(figsize=(16, 6))

    # Línea de runoff mensual
    ax.plot(df_runoff['valid_time'], df_runoff['ro'], label='Monthly Total Runoff', color='purple')

    # Etiquetas y formato
    ax.set_title('Monthly Total Runoff (2000-2020)', fontsize=16)
    ax.set_xlabel('Date', fontsize=12)  # Mostrar fechas en el eje X
    ax.set_ylabel('Runoff (mm)', fontsize=12)  # Nueva unidad en centímetros
    ax.legend()
    ax.grid(True)

    # Formato del eje X para mostrar fechas como Año-Mes
    ax.xaxis.set_major_locator(plt.MaxNLocator(12))
    ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)

    # Mostrar el gráfico
    #plt.show()

else:
    print("No se encontraron datos válidos para el rango de años especificado.")



###########################endend 7.3

# Calcular la diferencia: Precipitación - (Evaporación + Runoff)
df_diff = df_precip.set_index('valid_time')['tp'] - (df_evap.set_index('valid_time')['e'] + df_runoff.set_index('valid_time')['ro'])

# Crear el gráfico de la diferencia
fig, ax = plt.subplots(figsize=(16, 6))

ax.plot(df_diff.index, df_diff, label='P - (E + R)', color='orange')

# Etiquetas y formato
ax.set_title('Difference of Precipitation - (Evaporation + Runoff) (2000-2020)', fontsize=16)
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Difference (mm)', fontsize=12)
ax.legend()
ax.grid(True)

# Formato del eje X para mostrar fechas como Año-Mes
ax.xaxis.set_major_locator(plt.MaxNLocator(12))
ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m'))
plt.xticks(rotation=45)

# Mostrar el gráfico
plt.show()