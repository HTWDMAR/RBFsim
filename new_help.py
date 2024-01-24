import streamlit as st
import numpy as np
import streamlit.components.v1 as components
from PIL import Image

def app():
    st.title(":red[Help Page]")
    #st.divider()
    e1, e2, e3 = st.tabs(["**Software Manual**", "**Literature Manual**", "**Download Literature Manual**"])
    with e1:
        
        st.subheader(":blue[How to use the software]")
        #st.divider()
        with st.expander(":red[**Home Page**]") :
            #st.subheader(":red[Home Page]")
            st.write("- :blue[This is the First Page that is visible when you open the _RBF-sim_ app, the page gives a brief introduction about RBF and the major contributors in the _RBF-sim_ app devlopment.]")
            col1, col2, col3,col4 ,col5,col6= st.columns(6)
            with col1 :
                
                image=Image.open('user_manual/home.png')
                st.image(image,width=400,caption='Home Page')
            with col2 :
                st.write('')

            with col3 :
                st.write('')   
            with col4 :
                st.write('')
            with col5 :
                image=Image.open('user_manual/sidebar.png')
                st.image(image,width=200,caption='Side Bar')
            st.write("- :blue[The figure above shows a snippet of the home page, one of the main naviagation tools for the app is the Sidebar marked by Box 1 in red, where a list of diffrent pages is shown, the sidebar can be used to switch between diffrent pages by selecting selecting the page you want to switch to.]")
            
            with col6 :
                st.write('')
        with st.expander(":red[**Data Collection Page**]") :
            st.write("- :blue[This is the second page to the app, when you switch to the data collection page you are by default taken to the data entry for the aquifier,the following is a snippet of the page you would be redirected to:]")
            c1,c2,c3,c4,c5,c6 = st.columns(6)
            with c2 :
                st.write('')
            with c1 :
                image=Image.open('user_manual/data_input_1.png')
                st.image(image,width=600,caption='Data Input Page')


            with c3 :
                st.write('')
            with c4 :
                st.write('')
            with c5 :
                st.write('')
            with c6 :
                st.write('')
            st.write("- :blue[The tabs marked by Box 1 in blue in the image above  can help you switch view between data entry for aquifier, well and clogging factor.]")
            st.write("- :blue[In the data entry page, if you are visiting for the first time, the data entry mode would be set to New Data by default, if you wish to change this you can click on the Box No.2 marked in green.]")
            st.write("- :blue[The desired data can be entered into the number boxes as shown by purple arrow marks in the figure, the question mark symbol can be used as help for certain parameter data entry range, a simillar design is followed by the well and the clogging factor tabs.]")
            st.write("- :blue[To enter data into the model press add data button shown by Box 3 in orange, simillar goes to update and delete data for wells and clogging facttor.]")
            st.write("- :blue[To view the data you have entered into the model you can click on the view data option shown by Box 4 in yellow, where all the data entries would be shown in order.]")
            st.write("- :blue[Once you have added primary data, next time when you go to the data entry page you would be directly redirected in the update mode by default, if you want to add new data make sure to change the data entry mode]")
            st.write("- :blue[The last tab on the data collection page, marked by red arrow is for Data Backup/ Retrival the page is shown by the figure below:]") 
            c1,c2,c3,c4,c5,c6 = st.columns(6)
            with c2 :
                st.write('')
            with c1 :
                image=Image.open('user_manual/data_input_2.png')
                st.image(image,width=600,caption='Data Backup Page')


            with c3 :
                st.write('')
            with c4 :
                st.write('')
            with c5 :
                st.write('')
            with c6 :
                st.write('')
            st.write("- :blue[The data backup page shown above allows you to backup the data you have entered into a model, in CSV or xls format by simplly clicking download data button.]") ## add image here
            st.write("- :blue[The data retrival page allows you to upload a previously backed-up file, from this action you can retrive the data you had previously entered into the model.]")
            c1,c2,c3,c4,c5,c6 = st.columns(6)
            with c2 :
                st.write('')
            with c1 :
                image=Image.open('user_manual/data_input_3.png')
                st.image(image,width=600,caption='Data Retrival Page')


            with c3 :
                st.write('')
            with c4 :
                st.write('')
            with c5 :
                st.write('')
            with c6 :
                st.write('')

        with st.expander(":red[**Results Page**]") :
             st.write("- :blue[On the results page you are first show a counter plot of the flow around the well, you will also have an option to view a 3D plot of the same by clicking Box 1 marked in green. As shown by figure below]")
             c1,c2,c3,c4,c5,c6 = st.columns(6)
             with c2 :
                st.write('')
             with c1 :
                image = Image.open("user_manual/results.png") 
                st.image(image,width=600,caption='Data Retrival Page')


             with c3 :
                st.write('')
             with c4 :
                st.write('')
             with c5 :
                st.write('')
             with c6 :
                st.write('')
             st.write("- :blue[You will also have an option to view Bank filtrate contribution and Time of travel by clicking theier respective buttons, as marked in the figure above with Box 2 and Box 3 in blue ]")
             st.write("") 

        with st.expander(":red[**Parameter Estimation**]") :
            st.write("- :blue[This page can be used to estimate diifrent parameters to be entered into the model, the figure below shows the diffrent tabs available for diffrent parameters highlighted by the green color box]") 
            c1,c2,c3,c4,c5,c6 = st.columns(6)
            with c2 :
                st.write('')
            with c1 :
                image = Image.open("user_manual/para_est.png") 
                st.image(image,width=600,caption='Data Retrival Page')


            with c3 :
                st.write('')
            with c4 :
                st.write('')
            with c5 :
                st.write('')
            with c6 :
                st.write('')
        
        st.subheader(":blue[FAQ's]")
                
            

    with e2:
        

        pdf_display = F'<iframe src="https://docs.google.com/document/d/e/2PACX-1vT66rJLgxpupEcVXS3Tw10CnXUihvxlJjFa-oCGaSYsoavIyYwIiRlulaV88OtloEZtnkmRlkOhIHQu/pub?embedded=true" width="700" height="1000" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    
    with e3:
        with open("Manual/RBFsim User Manual_03.09.2022.pdf", "rb") as pdf_file:
            PDFbyte = pdf_file.read()

        st.download_button(label="Download Literature Manual",
                    data=PDFbyte,
                    file_name="RBFSim-Literature-Manual.pdf",
                    mime='application/octet-stream')

        
