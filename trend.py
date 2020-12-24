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
pine_file = '../../raw_data/Pine_2010.xlsx'
df = pd.read_excel(pine_file)
df.set_index(df["cdatetime_est"], inplace=True)
dfl = df.dropna().copy()

# Smooth data over a moving window of a month
pts_per_day = 2 * 24
window_length = 30 * pts_per_day
col = 'conductance'
y_filt = return_trend(dfl['cdatetime_est'], dfl[col], window_length, poly_order=2 )


st.title('Extracting a Trend')
fig = make_subplots(rows=2, cols=1, shared_xaxes=True)
fig.add_trace(go.Scatter(x=dfl.index, y=dfl["conductance"], name="Unfiltered"), row=1, col=1)
fig.add_trace(go.Scatter(x=dfl.index, y=y_filt, name="Filtered"), row=2, col=1)
fig.update_yaxes(title=col, row=1)
fig.update_yaxes(title=col, row=2)
fig.show()

#df_logger.to_excel('Pine_2010filtered.xlsx')
