#!/usr/bin/env python
# coding: utf-8
'''
This is a program that will be deployed as a Streamlit app. 
The goal is to read a data file and allow the user to adjust the amount of smoothing
then extract the trend.
'''
# %% Import require modules
import numpy as np
import pandas as pd
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

# Note that window_length and poly_order are optional parameters
# If not provided, the defaults defined in the function will be used
def return_trend(x, y, window_length=11, poly_order=2):
    '''
    return_trend() applies a Savitsky-Golay smoothing filter to data
    Depends on the scipy module.
    
    Required input parameters:
    x: xdata
    y: ydata
    
    Optional input parameters:
    window_lenth: number of points to window over. Increased by one if not odd.
    poly_order: order of the polynomial to fit in the window. Defaults to 2.
    
    Returns:
    y_filt: The smoothed version of y.
    '''
    from scipy.signal import savgol_filter
    
    # If the window is even, increase by one
    if window_length % 2 == 0:
        window_length += 1
    
    # Apply filter
    y_filt = savgol_filter(y, window_length, poly_order)
    
    return y_filt

#%%
data_file = 'Pine_2010.xlsx'
df = pd.read_excel(data_file)

# STREAMLIT SIDEBAR
df['cdatetime_est'].dt.tz_localize('UTC')
df.set_index(df["cdatetime_est"], inplace=True)
dfl = df.dropna().copy()
explanation = '''
Data are smoothed using a 
Savitsky-Golay filter, which 
fits a polynomial to data over a
sliding window. Using the 
slider and radio buttons below 
you can adjust the window length 
and polynomial order. The longer 
the window the more the smooth. 
The lower the polynomial order,
the more the smoothing.
'''

col = "conductance"
st.sidebar.title("Parameter Selection")
cols = df.columns[1:]
col = st.sidebar.radio("Choose column to plot", cols)
st.sidebar.text(explanation)

# Set window length
window_max = int(len(df)/10)
window_default = int(len(df)/100)
window_length = st.sidebar.slider('Npts in smoothing window', 3, window_max, window_default)

# Select polynomial order in sidebar
poly_order = st.sidebar.radio("Select Window Polynomial Order", [1, 2, 3, 4], 1)
y_filt = return_trend(dfl['cdatetime_est'], dfl[col], window_length=window_length, poly_order=poly_order )

# STREAMLIT MAIN WINDOW
st.title('Extracting a Trend')
fig = make_subplots(rows=2, cols=1, shared_xaxes=True)
fig.add_trace(go.Scatter(x=dfl.index, y=dfl[col], name="Unfiltered"), row=1, col=1)
fig.add_trace(go.Scatter(x=dfl.index, y=y_filt, name="Filtered"), row=2, col=1)
fig.update_yaxes(title=col, row=1)
fig.update_yaxes(title=col, row=2)

st.subheader('Raw and Smoothed Data')
st.plotly_chart(fig)
st.subheader('First 20 rows of data')
st.write(dfl.head(20))

#df_logger.to_excel('Pine_2010filtered.xlsx')
