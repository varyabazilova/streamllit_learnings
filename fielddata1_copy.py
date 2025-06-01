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






# st.write ('What data are you processing??')

# tibetAWS = st.checkbox('tibet AWS')
# langtangAWS = st.checkbox('langtang AWS')

# if tibetAWS:
#      st.write("we will do some processing now!")
#      uploaded_file = st.file_uploader("upload a new file for processing")

#      if uploaded_file is not None:
        
#         new_data = pd.read_csv(uploaded_file, skiprows = 1).iloc[2:]
#         st.write('these are old column names:', new_data.columns)

#         # renamed = new_data.rename(columns=column_mapping)
#         # renamed['DATE'] = pd.to_datetime(renamed['TIMESTAMP']).dt.date
#         # renamed['TIME'] = pd.to_datetime(renamed['TIMESTAMP']).dt.time
#         # renamed = renamed.drop(['TIMESTAMP', 'RECORD'], axis = 1)
#         new_data_renamed = rename_columns(new_data, column_mapping)
#         new_data_renamed_corr = apply_corrections(new_data_renamed)
        
#         new_data_renamed_corr = convert_to_float(new_data_renamed_corr, exclude_columns=['DATE', 'TIME'])
#         st.write('here is the corrected file with renamed columns!!')
#         st.write(new_data_renamed_corr)

#         # plot the file 

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Plot All Selected Columns as Numeric")

# --- Upload File
uploaded_file = st.file_uploader("Upload your CSV file")#, type=["csv"])

if uploaded_file is not None:
    # --- Read CSV
    df = pd.read_csv(uploaded_file)
    st.subheader("Data Preview")
    st.write(df.head())

    # --- Show checkboxes for all columns
    st.subheader("Select columns to plot (forced to numeric):")
    selected_cols = []
    for col in df.columns:
        if st.checkbox(f"Include '{col}'", value=True):
            selected_cols.append(col)

    if selected_cols:
        # --- Force selected columns to numeric
        df_numeric = df[selected_cols].apply(lambda x: pd.to_numeric(x, errors='coerce'))

        # --- Plot
        fig, axs = plt.subplots(len(selected_cols), 1, figsize=(10, 3 * len(selected_cols)), sharex=True)

        if len(selected_cols) == 1:
            axs = [axs]  # Make iterable

        for ax, col in zip(axs, selected_cols):
            ax.plot(df.index, df_numeric[col])
            ax.set_title(col)
            ax.grid(True)

        plt.tight_layout()
        st.pyplot(fig)
     else:
        st.info("Please select at least one column to plot.")
