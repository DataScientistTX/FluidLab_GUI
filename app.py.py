# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 13:01:07 2021

@author: sercan
"""
#Libraries and settings
import streamlit as st
import time
import matplotlib.pyplot as plt
import numpy as np
from collections import deque

#Set the "wide" layout
st.set_page_config(layout='wide')

#Settings for Matplotlib figures
font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 3}

plt.rc('font', **font)

#Set the title of the dashboard        
st.title("Manual Controls")

#Creating 5 columns for the layout
col1, col2, col3, col4, col5 = st.beta_columns(5)

#Define a button response function, TODO:update the result of functions--------
def button_response(col,text):
    with col:
        result = st.button(text)
    if result:
        st.write(text)

#Create various buttons with their responses-----------------------------------
button_response(col1, "3-way valve - On")
button_response(col1, "3-way valve - Off")

button_response(col2, "Water - On")
button_response(col2, "Water - Off")

button_response(col3, "Pump-on")
button_response(col3, "Pump-off")

button_response(col4,"Auto Mud Test - Start")
button_response(col4, "Auto Mud Test - Stop")

#Create a slider for the 5th column, to enter pump speed-----------------------
with col5:
    result = st.slider("Pump speed - Manual Entry",  
                       min_value = 0, value = 0, max_value = 60, step=1)
if result:
    st.write("Pump-on with pump speed {}".format(result))

#Side bars for the frequency steps of automated mud tests----------------------
for i in range(10):
    globals()['pumpspeed_{}'.format(i)] = st.sidebar.slider(
        'Step {}'.format(i+1), 
        min_value = 0, value = 50-i*5, max_value = 50, step=1)


#TODO: Correct the visuals with real-time data-streams from sensors------------
with st.beta_expander("Pressure Data"):
    fig, ax = plt.subplots(3,3, figsize=(3,3))
    max_samples = 100
    max_x = max_samples
    max_rand = 100
    
    x = np.arange(0, max_x)
    y = deque(np.zeros(max_samples), max_samples)

    line1, = ax[0, 0].plot(x, np.array(y))
    ax[0, 0].set_ylim(0, max_rand)
    
    line2, = ax[0, 1].plot(x, np.array(y))
    ax[0, 1].set_ylim(0, max_rand)
    
    line3, = ax[0, 2].plot(x, np.array(y))
    ax[0, 2].set_ylim(0, max_rand)
    
    line4, = ax[1, 0].plot(x, np.array(y))
    ax[1, 0].set_ylim(0, max_rand)
    
    line5, = ax[1, 1].plot(x, np.array(y))
    ax[1, 1].set_ylim(0, max_rand)
    
    line6, = ax[1, 2].plot(x, np.array(y))
    ax[1, 2].set_ylim(0, max_rand)
    
    line7, = ax[2, 0].plot(x, np.array(y))
    ax[2, 0].set_ylim(0, max_rand)

    line8, = ax[2, 1].plot(x, np.array(y))
    ax[2, 1].set_ylim(0, max_rand)
    
    line9, = ax[2, 2].plot(x, np.array(y))
    ax[2, 2].set_ylim(0, max_rand)
    
    the_plot = st.pyplot(plt)
    
    def animate():  # update the y values (every 1000ms)
        line1.set_ydata(np.array(y))
        line2.set_ydata(np.array(y))
        line3.set_ydata(np.array(y))
        line4.set_ydata(np.array(y))
        line5.set_ydata(np.array(y))
        line6.set_ydata(np.array(y))
        line7.set_ydata(np.array(y))
        line8.set_ydata(np.array(y))
        line9.set_ydata(np.array(y))
        
        the_plot.pyplot(plt)
        y.append(np.random.randint(max_x)) #append y with a random integer between 0 to 100
    
    for i in range(200):
        animate()
        time.sleep(0.01)