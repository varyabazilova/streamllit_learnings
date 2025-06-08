import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("File X and File Y Processing App")

# Split screen into two columns
col1, col2 = st.columns(2)

# --- LEFT: Load and plot File X ---
with col1:
    st.header("File X")
    file_x = st.file_uploader("Upload File X", type=["csv"], key="file_x")

    if file_x:
        df_x = pd.read_csv(file_x)
        st.subheader("Preview of File X")
        st.dataframe(df_x)

        st.subheader("Plot of File X")
        st.line_chart(df_x)

# --- RIGHT: Load, correct, and append File Y ---
with col2:
    st.header("File Y")
    file_y = st.file_uploader("Upload File Y", type=["csv"], key="file_y")

    if file_y:
        df_y = pd.read_csv(file_y)
        st.subheader("Preview of File Y")
        st.dataframe(df_y)

        # --- Apply some corrections (example: fill NA) ---
        st.subheader("Apply Corrections")
        correction = st.radio("Correction to apply", ["Fill NA with 0", "Drop NA rows"])
        if correction == "Fill NA with 0":
            df_y_corrected = df_y.fillna(0)
        else:
            df_y_corrected = df_y.dropna()

        st.dataframe(df_y_corrected)

        # --- Append File Y to File X and show result ---
        if file_x:
            st.subheader("Appended DataFrame")
            df_combined = pd.concat([df_x, df_y_corrected], ignore_index=True)
            st.dataframe(df_combined)

            st.subheader("Plot of Combined Data")
            st.line_chart(df_combined)
        else:
            st.warning("Please upload File X first to append File Y.")
