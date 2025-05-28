import streamlit as st
import pandas as pd
import altair as alt

st.title('CSV Uploader and Plotter')

uploaded_file = st.file_uploader("Choose a CSV file")

# Separator selection
sep_option = st.selectbox(
    'Select the separator used in the file:',
    options=[', (comma)', '; (semicolon)', '\\t (tab)', '| (pipe)'],
    index=0
)
sep_dict = {
    ', (comma)': ',',
    '; (semicolon)': ';',
    '\\t (tab)': '\t',
    '| (pipe)': '|'
}
sep = sep_dict[sep_option]

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, sep=sep)
    st.subheader('DataFrame')
    st.write(df)

    st.subheader('Descriptive Statistics')
    st.write(df.describe())

    # Let user choose X and Y columns
    all_columns = df.columns.tolist()
    x_axis = st.selectbox('Select X-axis column:', all_columns, index=0)
    y_axis = st.selectbox('Select Y-axis column:', all_columns, index=1)

    x_type = infer_type(df[x_axis])
    y_type = infer_type(df[y_axis])

    # Create chart with explicit types
    c = alt.Chart(df).mark_point().encode(
        x=alt.X(x_axis, type=x_type),
        y=alt.Y(y_axis, type=y_type),
        tooltip=list(df.columns)
    )

    st.altair_chart(c, use_container_width=True)
else:
    st.info('☝️ Upload a CSV file')
