import numpy as np
import altair as alt
import pandas as pd
import streamlit as st

st.header('st.write')

# Example 1

st.write('Hello, *World!* :sunglasses:')

# Example 2

st.write(1234)

# Example 3

df = pd.DataFrame({
     'first column': [1, 2, 3, 4],
     'second column': [10, 20, 30, 40]
     })
# st.write(df)

# Example 4

st.write('Below is a DataFrame:', df, 'Above is a dataframe.')

# Example 5

df2 = pd.DataFrame(
     np.random.randn(200, 4),
     columns=['col1', 'col2', 'col3', 'col4'])
st.write(df2)

c = alt.Chart(df2).mark_circle().encode(
     x='col1', y='col2', size='col3', color='col4')#, tooltip=['a', 'b', 'c'])
st.write(c)


# example from varya

# import dataframe 
