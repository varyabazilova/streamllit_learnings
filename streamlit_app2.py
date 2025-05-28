import streamlit as st

st.header('st.cat')

st.image("./cat.jpeg")

if st.button('Say hello'):
     st.write('Why hello there')
else:
     st.write('Goodbye')