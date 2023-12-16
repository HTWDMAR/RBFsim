import streamlit as st
import time
import numpy as np
import pandas as pd
from streamlit.elements.plotly_chart import SHARING_MODES
import sympy
from sympy.core.symbol import symbols
from sympy.solvers.diophantine.diophantine import descent, length
from sympy.solvers.solvers import solve
#from db_fxns import create_table,add_data,view_all_data,view_unique_data,get_id,edit_well_id,delete_id
#from db_fxns_aq import create_table_aq,view_all_data_aq,add_data_aq,view_unique_data_aq,get_id_aq,edit_aq_id, delete_id_aq
#from db_fxns_aq import view_all_data_clg
import base64
import pathlib
import matplotlib.pyplot as plt
from matplotlib import cm, colors
from matplotlib.patches import Rectangle
from matplotlib.ticker import StrMethodFormatter
import model_pro
import contrib
from PIL import Image
from plot import *


def app():
    st.sidebar.divider()
    st.title(":red[Results and visualizations]")
    
    st.markdown("---")

    if 'aq_ls' and 'we_ls' and 'cf_ls' not in st.session_state:
        st.subheader(":blue[Please Input Data for the simulation]")
    #st.write("Using Previous Database Data")
    #st.write(st.session_state.aq_ls)
    if 'aq_ls' and 'we_ls' and 'cf_ls' in st.session_state :
        #st.write("off we go now")
        #st.write(len(st.session_state.aq_ls))

        if len(st.session_state.aq_ls)==0 and len(st.session_state.we_ls) == 0 :
            st.subheader(":blue[Please Input required data for the simulation]")
        if len(st.session_state.aq_ls) and (st.session_state.we_ls) !=0 :
            results_aq = st.session_state.aq_ls
            results = st.session_state.we_ls
            results_clg = st.session_state.cf_ls

            

            
            #with st.expander("View All Data"):
                #df_clg = pd.DataFrame(results_clg, columns=['Layer ID', 'K Value', 'D Value'])
                #st.dataframe(df_clg)
            
            # st.sidebar.markdown('---')
            # st.sidebar.markdown(""" **Stored Values:** """)

            # st.sidebar.markdown('---')



            # menu = ["Wells", "Rivers", "No Flow"]
            # choice = st.sidebar.selectbox("Please Select Boundary Condition", menu)
            aem_model = model_pro.Model(k=results_aq[0][4], H=results_aq[0][1], h0=results_aq[0][5], Qo_x=results_aq[0][2])
            ################################## Check AEM Model
            if len(results_clg) == 0:
                st.info("No Clogging Factor is Added!")
            else:
                aem_model.calc_clogging(results_clg[0][1], results_clg[0][2])
            
            if len(results) == 0:
                st.error("Please add at least one Well")
            else:
                for j in range(6):
                    if j == len(results):
                        for i in range(j):
                            well = model_pro.Well(aem_model, Q=results[i][1], rw=0.2, x=results[i][2], y=results[i][3])
            
                c1, c2 = st.columns(2)

                # ------------------------------------------------------------------Stream / Potential Lines for Multiple Wells-----------------------------    
                with c1:
                    if len(results)>(1):
                        st.subheader(":blue[Wells in Flow Field:]")
                    else:
                        st.subheader(":blue[Well in Flow Field:]")
                    try:

                        plot1 = plotting(0, 100, -20, 150, 100)
                        b, fig1 = plot1.plot2d(aem_model, levels=8, sharey=False, quiver=False, streams=True, figsize=(18, 12))
                        st.pyplot(fig1)                        
                    except Exception as e:
                        print('error occurred:', e)
                    

                with c2:
                    st.write('')
                    st.write('')
                    display_3d_plot = st.checkbox(":blue[Display 3D Plot]")
                    
                    

                    # Check if the checkbox is checked
                    if display_3d_plot:
                        # Assuming `aem_model` is defined somewhere in your code
                        b2, fig2 = plot1.plot3d(aem_model)
                        st.pyplot(fig2)
                st.divider()
                c1,c2=st.columns(2)
                with c1:# ------------------------------------------------------------------CR, TT, RL for One Well ------------------------------------------------
                    if len(results) > 1:
                        st.sidebar.markdown("---")
                        st.sidebar.info("After entering one well, The options will be available here.")
                    else:
                        solv = contrib.river_length(aem_model)
                        
                        length, riv_coords, capture_fraction = solv.solve_river_length()
                        tt, ys, avgtt, mintt, traj_array = solv.time_travel(results_aq[0][3], delta_s=0.4, calculate_trajectory=True)
                        # st.write(riv_coords)   ########### Changed here to modify capture length 
                        ############### Removing Negative Values 
                        riv_coords = [max(0., x) for x in riv_coords]
                        length=sum(riv_coords)
                        
                        #st.sidebar.markdown("---")
                        st.sidebar.title(":red[Contribution Portion:]")
                        if st.sidebar.checkbox("Bank Filtrate Portion"):
                            st.subheader(":blue[Bank Filterate Portion:]")
                            plot = plotting(0, 100, -20, 150, 100, riv_coords)
                            b, fig = plot.plot2d(aem_model, sharey=False, traj_array=traj_array, levels=8, quiver=False, streams=True)
                            st.pyplot(fig)
                            bf_ratio = capture_fraction * 100
                            bf_ratio_rounded = int(bf_ratio)
                            st.sidebar.metric(label=":blue[Bank Filtrate Portion:]", value="{} %".format(bf_ratio_rounded))

                            riv_length_rounded = int(length)
                            st.sidebar.metric(label=":blue[River Capture Length:]", value="{} m".format(riv_length_rounded))


                            riv_0 = riv_coords[0]
                            riv_1 = riv_coords[1]
                            if riv_0 != 0:
                                riv_0_rounded = riv_0.round(decimals=0)
                            else:
                                riv_0_rounded = int(riv_0)
                            riv_1_rounded = int(riv_1)

                            st.sidebar.metric(
                                label=":blue[Capture Length Location on Y-Axis:]",
                                value="{} m & {} m".format(riv_0_rounded, riv_1_rounded)
                            )
                with c2:
                    st.write('')
                


                # ----------------------------------------------------------------------------Travel Time---------------------------------------------------------------------------
                if len(results) > 1:
                    st.error(" ** Note: ** Enter Exactly One Well to get the solution for Bank Filtrate Portion, Capture Length and Time of Travel.")
                else:
                    st.sidebar.markdown("---")
                    st.sidebar.title(":red[Time of Travel:]")
                    if st.sidebar.checkbox("Time of Travel"):
                        
                        st.subheader(":blue[Time of Travel:]")
                        plot2 = plotting(0, 100, -20, 150, 100, riv_coords)
                        c, fig2 = plot2.plot2d(aem_model, tt=tt, ys=ys, traj_array=traj_array, levels=8, sharey=True, quiver=False, streams=True, figsize=(18, 12))
                        st.pyplot(fig2)

                        avg_tt_rounded = int(avgtt)
                        min_tt_rounded = int(mintt)

                        st.sidebar.metric(label=":blue[Average Travel Time:]", value="{} days".format(avg_tt_rounded))
                        st.sidebar.metric(label=":blue[Minimum Travel Time:]", value="{} days".format(min_tt_rounded))

                        st.markdown("---")

                # ------------------------------------------------------------------------------Download Files----------------------------------------------------------------------------------------
                plot3 = plotting(0, 100, -20, 150, 100)

                h0, psi0 = plot3.fix_to_mesh(aem_model)
                dfh = pd.DataFrame(data=h0)
                df_psi = pd.DataFrame(data=psi0)
                dfh_rounded = dfh.round(decimals=3)
                df_psi_rounded = df_psi.round(decimals=3)
                csv = dfh_rounded.to_csv(sep="\t", index=False)
                csv_psi = df_psi_rounded.to_csv(sep="\t", index=False)

                st.sidebar.markdown("---")
                st.sidebar.title("Download \u03C8 & Head:")
                st.sidebar.download_button(label="Download H in CSV", data=csv, mime="csv")
                st.sidebar.download_button(label="Download \u03C8 in CSV", data=csv_psi, mime="csv")

            st.sidebar.markdown("---")
