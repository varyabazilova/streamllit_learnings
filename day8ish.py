import streamlit as st
import pandas as pd
import numpy as np
import altair as alt


st.header('Line chart')

chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)




c = (
   alt.Chart(chart_data)
   .mark_point()
   .encode(x="a", y="b", size="c", color="c", tooltip=["a", "b", "c"])
)

st.altair_chart(c)


# import streamlit as st

# st.header('st.selectbox')

# option = st.selectbox(
#      'What is your favorite color?',
#      ('Blue', 'Red', 'Green'))

# st.write('Your favorite color is ', option)


# import streamlit as st

st.header('st.selectbox')

option = st.selectbox(
     'What is your favorite color?',
     ('Blue', 'Red', 'Green'))

# Define a color map for the options
color_map = {
    'Yellow':'yellow',
    'Blue': 'blue',
    'Red': 'red',
    'Green': 'green'
}

# Get the corresponding color
selected_color = color_map[option]

# Display the text with colored output
st.markdown(f'Your favorite color is <span style="color:{selected_color}">{option}</span>', unsafe_allow_html=True)




import streamlit as st

st.header('st.checkbox')

st.write ('What would you like to order?')

icecream = st.checkbox('Ice cream')
coffee = st.checkbox('Coffee')
cola = st.checkbox('Cola')

if icecream:
     st.write("Great! Here's some more 🍦")

if coffee: 
     st.write("Okay, here's some coffee ☕")

if cola:
     st.write("Here you go 🥤")