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
from scipy.signal import savgol_filter
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
# %%Read the data
pine_file = '../../raw_data/Pine_2010.xlsx'
df = pd.read_excel(pine_file)

# %%
# Set the date to be the time series index instead of just numbering the points
df.set_index(df["cdatetime_est"], inplace=True)
df_logger = df.dropna().copy()
fig = px.line(df_logger, x="cdatetime_est", y=["temp", "conductance"])
fig.show()

# In[11]:




# Smooth data over a moving window of a week
pts_per_day = 24 * 2 #since the sample interval is 30 min

# Set window to be a week
window_length = 7 * pts_per_day + 1 # window length must be odd number

poly_order = 2

x = df_logger['cdatetime_est']
y = df_logger['temp']
y_fit = savgol_filter(y, window_length, poly_order)


fig, ax = plt.subplots(figsize=(15,5))
ax.plot(x, y)
ax.plot(x, y_fit, 'r')
ax.set_ylabel('Temperature (deg C)')
ax.set_title('Smoothing over a week')


# In[12]:


from scipy.signal import savgol_filter

# Smooth data over a moving window of a month
window_length = 30 * pts_per_day + 1 # window length must be odd number
y_fit = savgol_filter(y, window_length, poly_order)

fig, ax = plt.subplots(figsize=(15,5))
ax.plot(x, y)
ax.plot(x, y_fit, 'r')
ax.set_ylabel('Temperature (deg C)')
ax.set_title('Smoothing over a month')


# Before we try the same thing with conductance data, let's put basic steps into a function so we don't have to repeat code.

# In[13]:


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
    
    # Plot the before and after
    fig, ax = plt.subplots(figsize=(15,5))
    ax.plot(x, y)
    ax.plot(x, y_filt, 'r')
    
    return y_filt


# In[14]:


y_filt = return_trend(df_logger['cdatetime_est'], df_logger['conductance'], 7 * pts_per_day, poly_order=2 )


# In[15]:


y_filt = return_trend(df_logger['cdatetime_est'], df_logger['conductance'], 30 * pts_per_day )


# Of course, you can just plot the trend returned by the function.

# In[16]:


fig, ax = plt.subplots(figsize=(15,5))
ax.plot(df_logger['cdatetime_est'], y_filt, 'r')


# <a id='save_data'></a>

# ## Save the results to a file

# You can add also add the filtered data to your dataframe.

# In[17]:


df_logger['conductance_filt'] = y_filt
df_logger.head()


# Then write the dataframe to an excel file. By default it will be written to your current directory, but you can edit the path.

# In[18]:


df_logger.to_excel('Pine_2010filtered.xlsx')


# <a id='final_thoughts'></a>

# ## Final Thoughts
# 
# If is important to realize that filtering with a window of a week does not mean that there variations with
# a shorter period are removed, only muted. 
# 
# You can change the amount of smothing by altering the window width or the order of the polynomial being fit.
# A higher order polynoial will smooth less.  Try it and see.  In general, keep the order of the polynomial low
# or the fit will go wonky.
# 
# Below are examples of polynomial fits of first, second and third order for the same window.

# In[19]:


y_filt = return_trend(df_logger['cdatetime_est'], df_logger['conductance'], 30 * pts_per_day, poly_order=1 )


# In[20]:


y_filt = return_trend(df_logger['cdatetime_est'], df_logger['conductance'], 30 * pts_per_day, poly_order=2 )


# In[21]:


y_filt = return_trend(df_logger['cdatetime_est'], df_logger['conductance'], 7 * pts_per_day, poly_order=3 )

