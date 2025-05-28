# import streamlit as st
# import pandas as pd
# import altair as alt

# st.title('st.file_uploader')

# st.subheader('Input CSV')
# uploaded_file = st.file_uploader("Choose a CSV file")

# # Allow user to select the separator
# sep_option = st.selectbox(
#     'Select the separator used in the file:',
#     options=[', (comma)', '; (semicolon)', '\\t (tab)', '| (pipe)'],
#     index=0
# )

# # Map the human-readable option to actual separator
# sep_dict = {
#     ', (comma)': ',',
#     '; (semicolon)': ';',
#     '\\t (tab)': '\t',
#     '| (pipe)': '|'
# }
# sep = sep_dict[sep_option]

# if uploaded_file is not None:
#     df = pd.read_csv(uploaded_file, sep=sep)
#     st.subheader('DataFrame')
#     st.write(df)
#     st.subheader('Descriptive Statistics')
#     st.write(df.describe())

#     # Only show dropdowns if there are at least two columns
#     if len(df.columns) >= 2:
#         x_axis = st.selectbox('Select X axis', options=df.columns, index=0)
#         y_axis = st.selectbox('Select Y axis', options=df.columns, index=1)

#         # Create the Altair scatter plot
#         c = alt.Chart(df).mark_point().encode(
#             x=x_axis,
#             y=y_axis,
#             tooltip=list(df.columns)
#         )
#         st.altair_chart(c, use_container_width=True)
#     else:
#         st.warning("The uploaded CSV must have at least two columns to plot.")
# else:
#     st.info('☝️ Upload a CSV file')
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
        df = pd.read_csv(uploaded_file, sep=sep)
        st.subheader('DataFrame Preview')
        st.write(df)

        st.subheader('Descriptive Statistics')
        st.write(df.describe())

        if len(df.columns) >= 2:
            x_axis = st.selectbox('Select X axis', options=df.columns, index=0)
            y_axis = st.selectbox('Select Y axis', options=df.columns, index=1)

            x_type = infer_type(df[x_axis])
            y_type = infer_type(df[y_axis])

            chart = alt.Chart(df).mark_point().encode(
                x=alt.X(x_axis, type=x_type),
                y=alt.Y(y_axis, type=y_type),
                tooltip=list(df.columns)
            ).interactive()

            st.subheader('Scatter Plot')
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("The uploaded CSV must have at least two columns to plot.")
    except Exception as e:
        st.error(f"Error reading the file: {e}")
else:
    st.info('☝️ Upload a CSV file to begin')
