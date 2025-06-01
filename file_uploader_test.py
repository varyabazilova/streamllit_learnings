import streamlit as st
import pandas as pd
import altair as alt

st.title('CSV File Uploader and Plotter')

st.subheader('Upload a CSV File')
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

# Allow user to select the separator
sep_option = st.selectbox(
    'Select the separator used in the file:',
    options=['Comma (,)', 'Semicolon (;)', 'Tab (\\t)', 'Pipe (|)']
)

# Map from selected label to actual separator
sep_lookup = {
    'Comma (,)': ',',
    'Semicolon (;)': ';',
    'Tab (\\t)': '\t',
    'Pipe (|)': '|'
}
sep = sep_lookup[sep_option]

# Helper to infer Altair data types
def infer_type(series):
    if pd.api.types.is_numeric_dtype(series):
        return 'quantitative'
    elif pd.api.types.is_datetime64_any_dtype(series):
        return 'temporal'
    else:
        return 'nominal'

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, sep=sep, na_values=["", " ", "NA", "N/A", "-", "--"])
        st.subheader('DataFrame Preview')
        st.write(df)

        st.subheader('Descriptive Statistics')
        st.write(df.describe())
        
        alt.Chart(df).mark_point().encode(
            x='Lat',
            y='Lon'
)

    except Exception as e:
        st.error(f"Error reading the file: {e}")
else:
    st.info('☝️ Upload a CSV file to begin')
