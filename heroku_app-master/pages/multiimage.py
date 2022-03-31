import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from skimage import io, morphology
import numpy as np
import skimage.feature as features
from scipy import ndimage
from skimage.morphology import white_tophat
from skimage.morphology import disk
import cv2
from PIL import Image, ImageEnhance
import imageio
from skimage.exposure import  rescale_intensity
from streamlit_cropper import st_cropper

import streamlit as st
import os
import datetime 





# @st.cache(suppress_st_warning=True)
def app():
    st.sidebar.markdown("<h2 align='center'>ZACHARISTS</h2>",unsafe_allow_html=True)
    title = st.sidebar.text_input( '',value=st.session_state['title'], placeholder="Paste image folder path here")
    def file_selector(folder_path='.'):
        filenames = os.listdir(folder_path)
        new_filenames=[]
        for x in filenames:
            if x.endswith(".tiff"):
                new_filenames.append(x)

        all_filename = [os.path.join(folder_path, file)  for file in new_filenames]

        return all_filename,new_filenames
    

    folder_path= None

    folder_path =title
    if folder_path:
        filename,new_filenames = file_selector(folder_path)
    else:
        filename,new_filenames= None,None
    # st.write('You selected `%s`' % filename)

    # file1 = open("./pages/new.txt","r+")
    # x,y,z=file1.readlines()
    # file1.close()
    # del file1
   
    # print(x)
    # print(y)
    # print(z)
    # print("DONE")
    def redchangeValue():
        st.session_state['red'] = st.session_state["red_slider"]
    def greenchangeValue():
        st.session_state['green'] =st.session_state["green_slider"]
    def bluechangeValue():
        st.session_state['blue'] = st.session_state["blue_slider"]
    def changeDiskRadius():
        st.session_state['disk_radius'] = st.session_state["dr"]




    factor_red = st.sidebar.slider(
        '🔴 Red Channel ',
        0.5, 25.0 , value = st.session_state['red'], on_change = redchangeValue,key="red_slider")

    factor_green = st.sidebar.slider(
        '🟢 Green Channel',
        0.5, 25.0,value= st.session_state['green'],on_change = greenchangeValue,key="green_slider")

    factor_blue = st.sidebar.slider(
        '🔵 Blue Channel',
        0.5, 25.0,value = st.session_state['blue'],on_change = bluechangeValue,key="blue_slider")

    st.sidebar.markdown("Advanced Settings")

    disk_radius = st.sidebar.slider(
        'Disk Radius',
        10, 25 , value = st.session_state['disk_radius'], on_change = changeDiskRadius,key="dr")

    filter_size = st.sidebar.selectbox(
        "Background Blur",
        ("Type 1", 'Type 2','Type 3','Type 4','Type 5','Type 6','Type 7')
    )

    dic ={"Type 1":5 , 
    "Type 2":7 ,
    "Type 3":9 ,
    "Type 4":11 ,
    "Type 5":13 ,
    "Type 6":15,
    "Type 7":17}







        

    # L = [str(factor_red)+"\n", str(factor_green)+"\n", str(factor_blue)] 

    # file1 = open("./pages/new.txt","r+")
    # file1.writelines(L)
    # file1.close()
    
    filter_size = dic[filter_size]


    display_image =[]
    # st.info('Select same strain images at a time for better enhancement results')
    st.markdown("<small><i>Select same strain images at a time for better enhancement results</i></small>",unsafe_allow_html=True)
    a,b,c,d = st.columns(4)
    if a.button("Enhance all images"):

    # L = [str(factor_red)+"\n", str(factor_green)+"\n", str(factor_blue)] 

    # file1 = open("./pages/new.txt","r+")
    # file1.writelines(L)
    # file1.close()
        with st.spinner("Enhancing"):
            for file,name in zip(filename,new_filenames):
                
                

                def readImage(path,radius=15):
                    img = io.imread(path)
                    img = cv2.resize(img, (1000, 1000),
                            interpolation = cv2.INTER_NEAREST)
                    
                    if img.shape[2] == 4:
                        R,G,B,A = cv2.split(img)
                    else:
                        R,G,B = cv2.split(img)
                    R= rescale_intensity(R, out_range=(0,255)).astype(np.uint8)
                    G= rescale_intensity(G , out_range=(0,255)).astype(np.uint8)
                    B = rescale_intensity(B , out_range=(0,255)).astype(np.uint8)
                    img = cv2.merge((R,G,B))
                    blur = cv2.GaussianBlur(img,(5,5),0)
                    R,G,B = cv2.split(blur)
                    radius = radius
                    str_el = disk(radius)

                    return R,G,B,str_el,img



                def readChannel(R,str_el,factor = 1 ):
                    scikit_tophat = white_tophat(R, str_el)
                    scikit_tophat = Image.fromarray(scikit_tophat)
                    enhancer = ImageEnhance.Contrast(scikit_tophat)
                    factor = factor
                    im_output = enhancer.enhance(factor)

                    return im_output



                def mergeAll( im_output_R , im_output_G  ,im_output_B ):
                    im1 = Image.merge('RGB', (im_output_R ,im_output_G, im_output_B))
                    return im1

            


                R,G,B,str_el,img = readImage(file,radius=disk_radius)

            
                im_output_R = readChannel(R,str_el,factor_red)
        
                im_output_G = readChannel(G,str_el,factor_green)

                im_output_B = readChannel(B,str_el,factor_blue)

                res = mergeAll( im_output_R , im_output_G  ,im_output_B )
                
                res.save("D:/ENHANCEDIMAGES/"+name[:-5]+"_enhanced.png")
            
                display_image.append(res.resize((500,500),Image.BICUBIC))
        
        # st.image(display_image[0])
        col1,col2,col3,col4 = st.columns(4)
        l=[col1,col2,col3,col4]

        i=0

        l_len = len(display_image)

        while len(display_image)>=i:

            
            if i<l_len:
                col1.image(display_image[i],caption=new_filenames[i])
            i=i+1
            if i<l_len:
                col2.image(display_image[i],caption=new_filenames[i],)
            i=i+1
            if i<l_len:
                col3.image(display_image[i],caption=new_filenames[i])
            i=i+1
            if i<l_len:
                col4.image(display_image[i],caption=new_filenames[i])
            i=i+1
            

            
        


        

        




    
