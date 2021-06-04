import streamlit as st
import time
import numpy as np
from collections import deque
import SessionState
import functions 
import pandas as pd
import altair as alt 

st.set_page_config(layout='wide')

font = {'family' : 'normal',

        'weight' : 'normal',

        'size'   : 3}

#Set the title of the dashboard        

st.title("Fluid Lab GUI")
waterSlider, mudSlider, pumpSlider, dummy1,dummy2, pumpSpeedSlider= st.beta_columns(6)
water = waterSlider.select_slider("Water Valve", ["On", "Off"], value = "Off")

if water=="On":
    functions.waterOn()
else:
    functions.stopWater()
    
mud = mudSlider.select_slider("Mud Valve", ["On", "Off"], value = "Off")

if mud=="On":
    functions.mudOn()
else:
    functions.stopDump()

pump = pumpSlider.select_slider("Pump", ["On", "Off"], value = "On")

if pump=="On":
    functions.runPump()
else:
    functions.stopPump()

pumpSpeed = pumpspeed = pumpSpeedSlider.slider("Pump Speed", 0, 20000,15000,1000)

functions.setPumpSpeed(pumpSpeed)

xanthanSlider,bariteSlider, dummy, dummy2,bariteSpeedSlider = st.beta_columns(5)

xanthan = xanthanSlider.select_slider("Xanthan", ["On", "Off"])

barite = bariteSlider.select_slider("Barite", ["On", "Off"])

bariteSpeed = bariteSpeedSlider.slider("Barite Rate", 0, 100,0,1)

st.markdown("***")

aV ,aD = st.beta_columns(2)

autoViscosity=aV.checkbox("Automatic Viscosity")

autoDensity=aD.checkbox("Automatic Density")

st.markdown("***")

chart1 = st.empty()

chart2 = st.empty()

session = SessionState.get()

try:
    d=session.df==1
except:
    column_names = ["time", "P1", "P2", "delta", "Flowrate", "Temp", "Density"]
    session.df = pd.DataFrame(columns = column_names)
    session.startTime=time.time()

counttime= time.time()
while True:
    print(time.time()-counttime) # performance indicator
    counttime=time.time()

    displayRange=100  #how much history to display
    
    p1=functions.getP1()
    p2=functions.getP2()
    new_row = {"time":time.time()-session.startTime, "P1":p1, "P2":p2, "delta": p1-p2, "Flowrate": functions.getFlowrate(), "Temp": functions.getTemp(), "Density": functions.getDensity()}

    #append row to the dataframe
    session.df = session.df.append(new_row, ignore_index=True)

    Pchart=alt.Chart(session.df.tail(displayRange)).mark_line().encode(x="time",y="P1")
    P2chart=alt.Chart(session.df.tail(displayRange)).mark_line().encode(x="time",y="P2")
    deltachart=alt.Chart(session.df.tail(displayRange)).mark_line().encode(x="time",y="delta")
    chart1.altair_chart(Pchart|P2chart|deltachart,use_container_width=True)

    FRchart=alt.Chart(session.df.tail(displayRange)).mark_line().encode(x="time",y="Flowrate")
    Tempchart=alt.Chart(session.df.tail(displayRange)).mark_line().encode(x="time",y="Temp")
    Densitychart=alt.Chart(session.df.tail(displayRange)).mark_line().encode(x="time",y="Density")
    
    chart2.altair_chart(FRchart|Tempchart|Densitychart,use_container_width=True)

    



