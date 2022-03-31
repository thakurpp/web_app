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
    title = st.sidebar.text_input('', placeholder="Paste image folder path here")
    st.session_state['title']=title
    print(title)
    
    def file_selector(folder_path='.'):
        filenames = os.listdir(folder_path)
        new_filenames=[]
        for x in filenames:
            if x.endswith(".tiff"):
                new_filenames.append(x)

        selected_filename = st.sidebar.selectbox('Select image', new_filenames)
        st.sidebar.markdown("Manual Enhance")
        return os.path.join(folder_path, selected_filename)


    folder_path= None

    folder_path =title
    if folder_path:
        filename = file_selector(folder_path)
    else:
        filename= None
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
        0.5, 25.00 , value = st.session_state['red'], on_change = redchangeValue,key="red_slider")

    factor_green = st.sidebar.slider(
        '🟢 Green Channel',
        0.5, 25.00,value= st.session_state['green'],on_change = greenchangeValue,key="green_slider")

    factor_blue = st.sidebar.slider(
        '🔵 Blue Channel',
        0.5, 25.00,value = st.session_state['blue'],on_change = bluechangeValue,key="blue_slider")

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
    if filename:
        @st.cache(show_spinner=True, suppress_st_warning=True )
        def readImage(path,x,radius=15):
            img = io.imread(path)
            img = cv2.resize(img, (500, 500),
                    interpolation = cv2.INTER_NEAREST)
            
            if img.shape[2] == 4:
                R,G,B,A = cv2.split(img)
            else:
                R,G,B = cv2.split(img)
            R= rescale_intensity(R, out_range=(0,255)).astype(np.uint8)
            G= rescale_intensity(G , out_range=(0,255)).astype(np.uint8)
            B = rescale_intensity(B , out_range=(0,255)).astype(np.uint8)
            img = cv2.merge((R,G,B))
            blur = cv2.GaussianBlur(img,(x,x),0)
            R,G,B = cv2.split(blur)
            radius = radius
            str_el = disk(radius)

            return R,G,B,str_el,img


        @st.cache(show_spinner=True, suppress_st_warning=True)
        def readChannel(R,str_el,factor = 1 ):
            scikit_tophat = white_tophat(R, str_el)
            scikit_tophat = Image.fromarray(scikit_tophat)
            enhancer = ImageEnhance.Contrast(scikit_tophat)
            factor = factor
            im_output = enhancer.enhance(factor)

            return im_output


        @st.cache(show_spinner=True, suppress_st_warning=True)
        def mergeAll( im_output_R , im_output_G  ,im_output_B ):
            im1 = Image.merge('RGB', (im_output_R ,im_output_G, im_output_B))
            return im1

      


        R,G,B,str_el,img_original = readImage(filename,x=filter_size,radius=disk_radius)

        st.session_state["RAW_r"]=R
        st.session_state["RAW_r"]=G
        st.session_state["RAW_r"]=B
        st.session_state["str_el"]=str_el

     


        def displayChannel(res,channel,col,width):

            image = np.asarray(res)
            if channel == 0:
                image[:, :, 1] = 0
                image[:, :, 2] = 0
            
            elif channel == 1:
                image[:, :, 0] = 0
                image[:, :, 2] = 0
                
            elif channel == 2:
                image[:, :, 0] = 0
                image[:, :, 1] = 0
                
            elif channel == 3:
                image[:,:,2] = 0
            elif channel == 4:
                image[:,:,1] = 0
            elif channel == 5:
                image[:,:,0]=0
        
            image = Image.fromarray(image)
       
            
            col.image(image,width=width)

        
        col1,col2,x,y,w= st.columns(5)

        
        

        col3,col4,col5,f = st.columns([3,1,1,0.5])

        



        # imageLocation = st.empty()

        # imageLocation.image(old_image)
        # if st.checkbox('New Layer'):
        #     imageLocation.image(new_image)
        im_output_R = readChannel(R,str_el,factor_red)
        im_output_G = readChannel(G,str_el,factor_green)
        im_output_B = readChannel(B,str_el,factor_blue)
        res_auto = mergeAll( im_output_R , im_output_G  ,im_output_B )

    # col3.image(img_original,use_column_width='always')

        imageLocation = col3.empty()
        imageLocation.image(img_original,width=480)
    
        # if col1.button("View Original"):
        #     imageLocation.image(img_original)

        
        
        # val = col1.slider("",0,1)
        if col1.checkbox("AUTO ENHANCE"):
        # if val==1:
            imageLocation.image(res_auto,width=480)
            # st_cropper(res_auto, realtime_update=True, box_color='#0000FF',
            #                          aspect_ratio=(1,1))
            displayChannel(res_auto,0,col4,140)
            displayChannel(res_auto,1,col4,140)
            displayChannel(res_auto,2,col4,140)

            red = col5.checkbox("RED")
            col5.image('image.png')
            green = col5.checkbox("GREEN")
            col5.image('image.png')
            blue = col5.checkbox("BLUE")
            col5.image('image.png')
        
            # st_cropper(res_auto, realtime_update=True, box_color='#0000FF',
            #                         aspect_ratio=aspect_ratio)
            if red:
                displayChannel(res_auto,0,imageLocation,480)
            if green:
                displayChannel(res_auto,1,imageLocation,480)
            if blue:
                displayChannel(res_auto,2,imageLocation,480)
            if red and green:
                displayChannel(res_auto,3,imageLocation,480)
            if red and blue:
                displayChannel(res_auto,4,imageLocation,480)
            if green and blue:
                displayChannel(res_auto,5,imageLocation,480)

            if red and green and blue:
                imageLocation.image(res_auto,width=480)
            
            
            if w.button("SAVE"):
                res_auto.save("D:/ENHANCEDIMAGES/"+filename.replace(folder_path,"")[:-5]+"_enhanced.png")
                f= open("D:/ENHANCEDIMAGES/"+filename.replace(folder_path,"")[:-5]+"_feature.txt","a+")
                current_time = str(datetime.datetime.now()).split(" ")

                

                L = [f"--------------------SETTINGS APPLIED ON {current_time[0]} AT {current_time[1]}----------------\n","Red :"+ str(factor_red)+"\n","Green :"+str(factor_green)+"\n","Blue:"+str(factor_blue)+"\n","Disk Radius :"+str(disk_radius)+"\n","Blur :"+str(filter_size)+"\n"]
                f.writelines(L)
                f.close()


        # if col5.checkbox("RED",key="red") and col5.checkbox("GREEN",key="gren"):
        #     displayChannel(res_auto,3,imageLocation)





    

    # if col2.checkbox("")





   
    # with col3.empty():

    #     # if col1.button("View Original Image"):
    #     #     col3.image(img_original,use_column_width='always')
 
        
    #     if col2.button("Auto Enhance"):

    #         # R,G,B,str_el,img = readImage(filename,x=filter_size,radius=disk_radius)

    #         col3.image(res_auto,use_column_width='always')
    #         displayChannel(res_auto,0,col4)
    #         displayChannel(res_auto,1,col4)
    #         displayChannel(res_auto,2,col4)



        # if x.button("Reset to Original"):
        #     col3.image(img_original,use_column_width='always')


        # if res:



            
        

    
        # if col2.button("Reset to Original"):
        #     col3.image(img,use_column_width='always')




       

    






        
        #res.save('result.png')
        st.session_state['key1'] = img_original
        st.session_state['key2'] = res_auto


    




    
