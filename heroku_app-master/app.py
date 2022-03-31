import os
import streamlit as st

import numpy as np
from PIL import  Image

# Custom imports 
from multipage import MultiPage
from pages import data_upload,page2,multiimage,zoom
st.set_page_config(
     page_title="Automated Microscopy analysis",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded")


# hide_streamlit_style = """
#             <style>

#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             .css-1wrcr25 {margin-top: -95px;}
#             .css-zbg2rx {height: 130vh;line-height: 0px;padding-top: 142px;padding-bottom: 61px;padding-left: 13px;padding-right: 13px;}
#             .css-k8dovx {gap: 8px;}
#             .st-d7 {padding-top: 0px;}
#             .css-qrbaxs {font-size: 13px;}
#             .css-5thqtp {gap: 10px}
#             p {padding-top: 7px;font-weight: 900;}
#             .st-d6 {background :linear-gradient(to right, rgb(255, 0, 0) 0%, rgb(255, 0, 0) 0%, rgba(151, 166, 195, 0.25) 0%, rgba(151, 166, 195, 0.25) 100%);}
#             .css-1v3fvcr {overflow: hidden;}
#             .st-cl {padding-left: 27px;}
#             .st-dr {margin-right: 0px}
#             .css-fg4pbf {margin-top: -66px;}
#             .css-zbg2rx {height: 130vh;padding-top: 140px;}
#             .css-fg4pbf {margin-top: -66px;}
#             .css-zbg2rx {height: 130vh;}
#             .st-d6 {background: white}
#             .css-qrbaxs{padding-bottom: 18px;}
#             .css-qrbaxs {line-height: 12px;}
#             img {margin-top: 18px;}
#             .st-cl {padding-left: 0px;}
#             .css-qrbaxs {padding-bottom: 0px;}
#             .st-dk {padding-top: 6.33333px;}
#             .css-qrbaxs {padding-bottom: 0px;}
#             .st-cq {height: 3px;}
#             .css-1djdyxw {color: #011638;font-weight: bolder;font-size: large;}
#             </style>
#             """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)
# hide_streamlit_style="""
#                <style>
#                .css-xq1lnh-EmotionIconBase {margin-top: -40px;}
#                .css-18e3th9 {margin-top: -110px;}
#                .css-zbg2rx {margin-top: -22px;padding-bottom: 46px}
#                </style>"""


hide_streamlit_style = """
                    <style>
                    .css-18e3th9 {margin-top: -120px;}
                    .css-1gx893w {margin-top: -55px}
                    .css-1djdyxw {font-size: large;font-weight: bold;}
                    p {font-weight: bold}
                    .css-1cpxqw2 {font-weight: bold;}
                    small {font-weight: lighter;}
                    h2 {margin-bottom: -45px;font-family: Bold Fraktur;color: #FD5F08}
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    </style>"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.write('<style>div.row-widget.stRadio>div{flex-direction:row;}</style>', unsafe_allow_html=True)
# st.markdown("""
#         <style>
#                body{
#                     padding-top: 0rem;
#                     padding-bottom: 10rem;
#                     padding-left: 5rem;
#                     padding-right: 5rem;
#                 }
#                .css-1d391kg {
#                     padding-top: 3.5rem;
#                     padding-right: 1rem;
#                     padding-bottom: 3.5rem;
#                     padding-left: 1rem;
#                 }
#         </style>
#         """, unsafe_allow_html=True)

# Create an instance of the app 
app = MultiPage()

# Title of the main page
# st.header('Welcome to ImageIn')
# if st.button("Reset Settings"):
#     st.session_state['red'] = 0.5
#     st.session_state['green']=8.0
#     st.session_state['blue']=8.0
#     st.session_state["disk_radius"]=15








# if st.button("Reset"):
#     L=["0.5\n","0.5\n","0.5"]
#     file1 = open("./pages/new.txt","r+")
#     file1.truncate()
#     file1.writelines(L)
#     file1.close()

# Add all your application here
app.add_page("Single image view          ", data_upload.app)

app.add_page("Multi image view           ",multiimage.app)
app.add_page("Compare view   ", page2.app)
app.add_page("Zoom view", zoom.app)
# app.add_page("Change Metadata", metadata.app)
# app.add_page("Machine Learning", machine_learning.app)
# app.add_page("Data Analysis",data_visualize.app)
# app.add_page("Y-Parameter Optimization",redundant.app)

# The main app
app.run()

