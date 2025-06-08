import streamlit as st
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

from PIL import Image



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


# def making plots as a function
def plot_selected_columns(df, label_prefix="column", key_prefix=""):
    """Interactive column selector and plotter for a given dataframe.

    Parameters:
    - df: pandas.DataFrame
    - label_prefix: str, text for checkbox labels (e.g. 'old', 'new')
    - key_prefix: str, unique key to separate Streamlit widget states
    """
    selected_cols = []

    st.write(f"Select {label_prefix} columns to plot:")
    for col in df.columns:
        # Use a unique key for each checkbox to avoid state conflicts
        if st.checkbox(f"{label_prefix} '{col}'", value=False, key=f"{key_prefix}_{col}"):
            selected_cols.append(col)
    
    if selected_cols:
        df_numeric = df[selected_cols].apply(lambda x: pd.to_numeric(x, errors='coerce'))

        with st.container():
            fig, axs = plt.subplots(len(selected_cols), 1, figsize=(10, 3 * len(selected_cols)), sharex=True)

            if len(selected_cols) == 1:
                axs = [axs]

            for ax, col in zip(axs, selected_cols):
                ax.plot(df.index, df_numeric[col])
                ax.set_title(col)
                ax.grid(True)

            plt.tight_layout()
            st.pyplot(fig)
    else:
        st.info("Please select at least one column to plot.")




# Split screen into two columns

# it tibet: 
# upload csv filw with the data
# check if the column names match 
# if column names match - change them
# 

st.set_page_config(layout="wide")
st.header('TIBET AWS DATA PROCESSING')
st.header('   ')

# st.title("File X and File Y Processing App")

# Split screen into two columns
col1, col2 = st.columns(2)

# --- LEFT: Load and plot File X ---
with col1:
    st.header("Previous file from Tibet AWS")
    old_file = st.file_uploader("upload previous .csv file from Tibet AWS", key="old_file")

    if old_file:
        # df_old = pd.read_csv(old_file)
        df_old = pd.read_csv(old_file)#, skiprows = 1).iloc[2:]

        image_path = '/Users/varyabazilova/Desktop/streamit_things/field_data_processing/yak.png'
        image = Image.open(image_path)
        yak_image = image.resize((284, 206))
        # Display the resized image
        st.image(yak_image, caption="Tibetian Yak looking good")#, use_column_width=False)

        st.subheader("Preview of old file")
        st.dataframe(df_old.head())


        option = st.selectbox(
            'Do you want to plot the data?',
            ('Nei', 'Yes, plot previous data')
        )
        if option == 'Yes':
            # plot the selected columns
            st.subheader("Exmine plot for the previous data:")
            plot_selected_columns(df_old, label_prefix="previous", key_prefix="previous")
    

with col2:
    st.header("new file to process and append:")
    uploaded_file = st.file_uploader("Upload a raw ''CR1000_Measured_values.dat'' file for processing")

    if uploaded_file is not None:
        new_data = pd.read_csv(uploaded_file, skiprows = 1).iloc[2:]
        st.image('/Users/varyabazilova/Desktop/streamit_things/field_data_processing/Tinkerbell magic wand gif.gif', caption="Processing data, renaming columns, doing corrections..",)

        new_data_renamed = rename_columns(new_data, column_mapping)
        new_data_renamed_corr = apply_corrections(new_data_renamed)
        
        new_data_renamed_corr = convert_to_float(new_data_renamed_corr, exclude_columns=['DATE', 'TIME'])
        st.subheader('Preview of corrected file:')
        st.write(new_data_renamed_corr.head())
        


        option = st.selectbox(
            'Do you want to plot the data?',
            ('Nei', 'Yes, plot new data')
        )
        if option == 'Yes':
            # plot the selected columns
            st.subheader("Exmine plot for the previous data:")
            plot_selected_columns(df_old, label_prefix="new", key_prefix="new")
        

        
# Show full-width combined panel only if both files are present
if old_file and uploaded_file:
    with st.container():
        st.header("Combined Output Panel")

        # # Optional: make sure df_old gets same treatment as new data
        # df_old_renamed = rename_columns(df_old, column_mapping)
        # df_old_corrected = apply_corrections(df_old_renamed)
        # df_old_corrected = convert_to_float(df_old_corrected, exclude_columns=['DATE', 'TIME'])

        df_combined = pd.concat([df_old, new_data_renamed_corr], ignore_index=True)

        st.subheader("Appended DataFrame")
        st.dataframe(df_combined)

        st.subheader("Plot of Combined Data")
        st.line_chart(df_combined)
else:
    st.info("Please upload previous data and new data to view combined output.")