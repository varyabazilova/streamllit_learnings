import streamlit as st
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt




# option = st.selectbox(
#      'What data are you processing?',
#      ('Blue', 'Red', 'Green'))




# preambule with things and functions 
# rename
column_mapping = {'RH_prec_Avg': 'RH',  #Mean air relative humidity, %
                  'Air_temperature_dgC_Avg': 'TAIR', # Mean air temperature, degrees Celsius
                  'Baro_mBar_Avg': 'PRES', # Mean atmospheric pressure, mbar
                  'Wind_speed_ms_WVT': 'WSPD', # Mean wind speed, m/s

                  'WindDir_Dgr_WVT': 'WINDDIR', # Vector mean wind direction, degrees
                  
                  # radiation 
                  # short
                  'CNR4_Radiation_short_up_Avg': 'KINC', # Mean outgoing shortwave radiation CNR4, W/m2
                  'CNR4_Radiation_short_dn_Avg': 'KUPW', # Mean incoming shortwave radiation CNR4, W/m2
                  # long
                  'CNR4_Radiation_long_up_Avg': 'LINC_raw', # Mean raw outgoing longwave radiation CNR4, W/m2
                  'CNR4_Radiation_long_dn_Avg': 'LUPW_raw', # Mean raw incoming longwave radiation CNR4, W/m2
                  
                  # 'Accumulated_RT_NRT_mm_Tot': 'BCON', # Mean bucket content, mm
                  # 'Bucket_RT_mm': 'PVOL',  # Measured instantaneous precipitation, mm
                  
                  'Accumulated_RT_NRT_mm_Tot': 'PVOL',  # Measured instantaneous precipitation, mm
                  'Bucket_RT_mm':'BCON', # Mean bucket content, mm 
                                   
                  'Pluvio_Status': 'PSTAT', #Status of the pluviometer
                  'Battery_Vdc_Min' : 'BVOL', #battery voltage, V
                  'CNR4_Temperature_C_Avg': 'TCNR4', # Mean CNR4 inside temperature, degrees Celsius
                                   
                  'Measured_distance_m_Max': 'SR50_raw', # Raw distance to the surface (SR50A sensor), m
                  'Quality_Measured_distance_Avg': 'SR50QUAL', # Quality measurement of the distance to the surface (SR50A sensor), NA
                  'Wind_U_Avg': 'WIND_U', # Additional wind measurement, NA
                  'Wind_V_Avg': 'WIND_V' }#, Additional wind measurement, NA

def rename_columns(raw, column_mapping):
    # rename
    renamed = raw.rename(columns=column_mapping)
    #format time step
    renamed['DATE'] = pd.to_datetime(renamed['TIMESTAMP']).dt.date
    renamed['TIME'] = pd.to_datetime(renamed['TIMESTAMP']).dt.time
    renamed = renamed.drop(['TIMESTAMP', 'RECORD'], axis = 1)
    
    return renamed


def apply_corrections(renamed): 
    ''' this function applies corrections ot the (i) radiation and (ii) SR50 data'''
    # radiation 
    renamed['LUPW_corr'] = renamed.LUPW_raw.astype(float) + 0.00000005670373*((renamed.TCNR4.astype(float) +273.15)**4)
    renamed['LINC_corr'] = renamed.LINC_raw.astype(float) + 0.00000005670373*((renamed.TCNR4.astype(float) +273.15)**4)
    # SR 
    renamed['SR50_corr'] = renamed.SR50_raw.astype(float) * renamed.TAIR.astype(float).apply(lambda x: math.sqrt((x + 273.15) / 273.15))
    
    return renamed

def convert_to_float(corrected, exclude_columns=[]):
    ''' this function assignes the float() type to all the observations
    you can excluse DATE, TIME '''
    # Exclude specified columns from conversion
    columns_to_convert = [col for col in corrected.columns if col not in exclude_columns]
    
    # Apply .astype(float) only to selected columns
    corrected[columns_to_convert] = corrected[columns_to_convert].astype(float)
    
    return corrected




# Upload file
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Data Preview:", df.head())

    # Create a checkbox for each column
    st.subheader("Select columns:")
    selected_cols = []
    for col in df.columns:
        if st.checkbox(f"Include '{col}'", value=True):
            selected_cols.append(col)

    st.write("You selected these columns:")
    st.write(selected_cols)
    st.write("Filtered DataFrame:")
    st.write(df[selected_cols])