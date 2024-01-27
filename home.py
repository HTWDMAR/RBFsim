import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.special
import os
import csv
import streamlit as st 
from PIL import Image
from io import BytesIO
import io
import base64
import pandas as pd





def app():
    




    st.title(":red[River Bank Filtration Tool: **_RBFsim_**]")
    st.sidebar.markdown("---")
    st.divider()
 
    col1, col2, col3,col4,col5,col6 = st.columns(6)
    with col1:
        st.write('')
    with col2:
        image=Image.open('homefigure.jpg')
        st.image(image,width=500,caption='River Bank Filtration (Thomas Grischek)')
    with col3:
        st.write('')
    with col4:
        st.write('')
    with col5:
        st.write('')
    with col6:
        st.write('')
    st.write("")
    st.write("")


    st.markdown("""
    
- :blue[Riverbank Filtration (RBF) is an eco-friendly alternative to direct groundwater (GW) extraction for drinking water production.]

- :blue[RBF involves natural infiltration of surface water (SW) into the aquifer.]

- :blue[In the aquifer, SW undergoes filtration, sorption, and biodegradation processes.]

- :blue[These processes reduce the need for costly further water treatment.]

- :blue[Successful RBF implementation has been seen in countries like Germany.]

- :blue[Development and sustainability of RBF systems require careful planning.]

- :blue[Key considerations include:]

  - :blue[__Aquifer-well interactions:__ optimizing well design and aquifer characteristics.]
  
  - :blue[__Groundwater-surface water interactions__: managing seasonal variations and surface water quality.]

- :blue[These factors are crucial for RBF's effectiveness and long-term viability.]

""")


    
######################## Info          

    with st.expander(":red[App Devloper Info]"):
   
        st.info("""
The authors of the **_RBFsim_** are not liable for any error that may result from the application of this software. 
For comments and suggestions, pls. email at: [RBFsim22@gmail.com](mailto:RBFsim22@gmail.com)

The codes in this site are **CC BY 4.0** licensed. The license wording can be found [here](https://creativecommons.org/licenses/by/4.0/).
Basically, for using code from here- the original authors should be credited.

Following authors are credited for this version [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6482752.svg)](https://doi.org/10.5281/zenodo.6482752) of the code (names not in any order):

1. **P. K. Yadav** - for conceptualization and basic code development
2. **M. Tufail** - Main code development for online implementation
3. **V. Cantarella** - Offline code and verification               
4. **A. Villa** - offline code and case studies
5. **M Gomez** - offline code and case studies
6. Tassilo Reuschling - First offline code development
7. Prof. Dr. T. Grischek - Supervisory support on contents
8. Vibhu Batheja - GUI, Deployment and Verification
9. Anton Kohler - Model Verification
10. Pratistha Kansakar - Report creation and optimization



**References**

- Coming up

     """,icon="ℹ️")



    
