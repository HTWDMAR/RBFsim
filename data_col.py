#Core Package
import streamlit as st
#DataFrame Package
import pandas as pd
#Math Package
import numpy as np
#Graph Package
#import matplotlib as mt
#Time
import time
#Database Functions
#from db_fxns import create_table,add_data,view_all_data,view_unique_data,get_id,edit_well_id,delete_id
#from db_fxns_aq import create_table_aq,view_all_data_aq,add_data_aq,view_unique_data_aq,get_id_aq,edit_aq_id, delete_id_aq
#from db_fxns_aq import create_table_clg,view_all_data_clg,add_data_clg,view_unique_data_clg,get_id_clg,edit_id_clg,delete_id_clg

#-------------------------------------------------------------------------------NavBar-Ends------------------------------------------------------------------------------------------------------------
def app():
    st.sidebar.divider()
    #j=100
    if 'aq_ls' not in st.session_state :
        
        st.session_state.aq_ls=[]
        st.session_state.we_ls=[]
        st.session_state.cf_ls=[]
        #### Add an if 
    #st.session_state.j=j
    st.title(':red[Data Input Interface]')
    #st.divider()
    #st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    
    aq_dc,well_dc,clo_dc,updown = st.tabs(["**Aquifer**", "**Well**","**Clogging Factor**","**View/Upload/Download Data**"])
    st.write("")
    with aq_dc :
        col1, col2 = st.columns(2)
    #if input_options == "Aquifer":
        with col1 :
            st.subheader(':blue[Aquifer]')
        with col2:
            #menu_aq = ["New Data", "Update Data", "Delete Data"]
            #choice_aq = st.selectbox("Please Select Action (Aquifer)", menu_aq)

        
            if len(st.session_state.aq_ls) == 0 :
                #choice_aq="Update Data"    ####### add if for updating data 
                menu_aq = ["New Data", "Update Data", "Delete Data"]
                choice_aq = st.selectbox("Select Action (Aquifier)", menu_aq)
            if len(st.session_state.aq_ls) != 0 :
                #choice_aq="Update Data"    ####### add if for updating data 
                menu_aq = ["Update Data","New Data",  "Delete Data"]
                choice_aq = st.selectbox("Select Action (Aquifier)", menu_aq)
        
        #create_table_aq()
        st.divider()
#-------------------------------------------------------------Create_aq-------------------------------------------------------------------------------------------------------------------
        if choice_aq == "New Data":
            #st.markdown(""" #### Please Enter the Required Values in Table: """)
            st.subheader(":blue[Add Values]")
            #st.sidebar.markdown('* **Acquifer Data Input:**')
            col1, col2, col3 = st.columns(3)
            with col1:
                #aq_id = st.number_input('Aquifer ID[n]', 1,1,1)
                aq_id=1
                thk_aq = st.number_input('Thickness of the Aquifer (m)', 1.,200.,20.)
                baseflow = st.number_input('Base Flow (m\u00B2/day):', 0., 1000.,1.)
            with col2:
                
                ref_head = st.number_input('Reference Head (m)', 1.,200.,9.5)
                porosity = st.number_input('Porosity:', 0.1,0.4,0.25,help='< 0.5')
            with col3:
                
                hyd_con = st.number_input('Hydraulic Conductivity (m/day)', 1., 1000., 10., help='Range : 1 - 1000')
            
            if st.button("Add Values for Aquifier"):
                #add_data_aq(aq_id, thk_aq, baseflow, porosity, hyd_con, ref_head)   ########### Need to add st.session state out here if want to use new format
                st.session_state.aq_ls.append([aq_id, thk_aq, baseflow, porosity, hyd_con, ref_head])
                st.success("Values added Successfully")                
#-------------------------------------------------------------Read_aq-----------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------Update_aq--------------------------------------------------------------------------------------------------------------------                    
        elif choice_aq == "Update Data":
            if len(st.session_state.aq_ls)== 0 :
                st.write("Enter Data, Current Data set Empty")
                df3_aq = pd.DataFrame(st.session_state.aq_ls, columns=['Aquifer ID', 'Thickness', 'Base Flow', 'Porosity', 'Hydraulic Conductivity', 'Reference Head'])
                st.dataframe(df3_aq)
            if len(st.session_state.aq_ls)!= 0 :
                st.subheader("Edit/Update Values")
                #results_aq = view_all_data_aq()
                #st.write(results_aq)
                with st.expander("View All Data"):
                    df_aq = pd.DataFrame(st.session_state.aq_ls, columns=['Aquifer ID', 'Thickness', 'Base Flow', 'Porosity', 'Hydraulic Conductivity', 'Reference Head'])
                    st.dataframe(df_aq)

                list_of_data_aq = [i[0] for i in st.session_state.aq_ls]                  #### Need to read aq_dat and give flxibility to modify
                selected_data_aq = st.selectbox("Aquifer ID to Edit", list_of_data_aq)   ##### Need to modify this section

                selected_result_aq = [sublist for sublist in st.session_state.aq_ls if sublist[0] == selected_data_aq]
                #st.write(selected_result_aq)
                
                if selected_result_aq:
                    aq_id = selected_result_aq[0][0]
                    thk_aq = selected_result_aq[0][1]
                    baseflow = selected_result_aq[0][2]
                    porosity = selected_result_aq[0][3]
                    hyd_con = selected_result_aq[0][4]
                    ref_head = selected_result_aq[0][5]

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        #new_aq_id = st.number_input("Aquifer ID:", aq_id)
                        new_aq_id=1
                        new_thk_aq = st.number_input("Thickness of the Aquifer (m):",1.,200., float(thk_aq))
                        new_baseflow = st.number_input("Base Flow (m\u00B2/day):",0.,1000., float(baseflow))
                    with col2:
                        
                        new_ref_head = st.number_input("Reference Head (m):", 1., 500., float(ref_head))
                        new_porosity = st.number_input("Porosity:",0., 1., float(porosity),help='< 0.5')
                    with col3:
                        
                        
                        new_hyd_con = st.number_input("Hydraulic Conductivity (m/day):",1., 1000., float(hyd_con),help='Range : 1 - 1000')
                    
                    if st.button("Update Values for Aquifier"):
                        
                        j=[] ##### Using this method since only 1 aquifier is being added for this code 
                        j.append([new_aq_id, new_thk_aq, new_baseflow, new_porosity, new_hyd_con, new_ref_head])
                        
                        st.session_state.aq_ls=j
                        st.success("Values added Successfully")
                        
                        

                #results2_aq = view_all_data_aq()
                with st.expander("Updated Data"):
                    df2_aq = pd.DataFrame(st.session_state.aq_ls, columns=['Aquifer ID', 'Thickness', 'Base Flow', 'Porosity', 'Hydraulic Conductivity', 'Reference Head'])
                    st.dataframe(df2_aq)

#----------------------------------------------------------------------Delete_aq-------------------------------------------------------------------------------------------------
        elif choice_aq == "Delete Data":
            if len(st.session_state.aq_ls)== 0 :
                st.write("Enter Data, Current Data set Empty")
                df3_aq = pd.DataFrame(st.session_state.aq_ls, columns=['Aquifer ID', 'Thickness', 'Base Flow', 'Porosity', 'Hydraulic Conductivity', 'Reference Head'])
                st.dataframe(df3_aq)
            if len(st.session_state.aq_ls)!= 0 :
                st.subheader("Delete Values")
                #results_aq = view_all_data_aq()
                #st.write(results_aq)
                with st.expander("View All Data"):
                    df_aq = pd.DataFrame(st.session_state.aq_ls, columns=['Aquifer ID', 'Thickness', 'Base Flow', 'Porosity', 'Hydraulic Conductivity', 'Reference Head'])
                    st.dataframe(df_aq)

                list_of_data_aq = [i[0] for i in st.session_state.aq_ls]      
                selected_data_aq = st.selectbox("Aquifer ID to Edit", list_of_data_aq)
                st.warning("The Aquifer ID {} will be Deleted".format(selected_data_aq))
                if st.button("Delete Values for Aquifer"):
                    #delete_id_aq(selected_data_aq)
                    st.session_state.aq_ls = [sublist for sublist in st.session_state.aq_ls if sublist[0] != selected_data_aq]
                    st.success("Aquifer ID is Deleted Successfully")

                #results3_aq = view_all_data_aq()
                with st.expander("Current Data"):
                    df3_aq = pd.DataFrame(st.session_state.aq_ls, columns=['Aquifer ID', 'Thickness', 'Base Flow', 'Porosity', 'Hydraulic Conductivity', 'Reference Head'])
                    st.dataframe(df3_aq)

        st.divider()
        #st.subheader(":blue[View Values]")
        #results_aq = view_all_data_aq()
        ################ Displaying Data
        col1, col2 = st.columns(2)
        with col1 :
            st.subheader(":blue[View All Data]")
        with col2:
            st.write('')
            if st.checkbox("Display Current Aquifier Data"):
            #st.write(results_aq)
        #with st.expander("View All Data"):
                df_aq = pd.DataFrame(st.session_state.aq_ls, columns=['Aquifer ID', 'Thickness', 'Base Flow', 'Porosity', 'Hydraulic Conductivity', 'Reference Head'])
                st.dataframe(df_aq)
                #df_aq = pd.DataFrame(results_aq, columns=['Aquifer ID', 'Thickness', 'Base Flow', 'Porosity', 'Hydraulic Conductivity', 'Reference Head'])
                if st.download_button(key="aquifier_download", label='Download Table', data=df_aq.to_csv(),mime='text/csv'):
                    st.success("Your File Successfully Downloaded")
        st.divider()
        #st.session_state.aq_ls=aq_ls
#---------------------------------------------------------------------Aquifer Finish-------------------------------------------------------------------------------------    
    #st.session_state.aq_ls=aq_ls
    
    
    
    with well_dc :
        #st.write(st.session_state.aq_ls)
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(':blue[Well]')
            
    #if input_options == "Aquifer":
        with col2 :
            st.write('')
            if len(st.session_state.we_ls)==0 :
                menu_well = ["New Data","Update Data", "Delete Data"]
                choice_well = st.selectbox("Select Action (Well)", menu_well)
            if len(st.session_state.we_ls)!=0 :
                menu_well = ["Update Data", "New Data","Delete Data"]
                choice_well = st.selectbox("Select Action (Well)", menu_well)
        st.divider()




#----------------------------------------------------------------------Create_Well----------------------------------------------------------------------------------------                   
        if choice_well == "New Data":
            #st.header(""" **Please Enter the Required Values in Table:** """)
            st.subheader(":blue[Add Values]")

            #Layout of the Main_Page
            col1, col2 = st.columns(2)
            with col1:
                well_id = int(st.number_input("Well ID (n)", 1, 10, 1))
                #----------limit pump_rate input upto 50 for 2D and 3D plot runtime error-----------------
                pump_rate = st.number_input("Pumping / Recharge Rate in (m³/day):", -5000., 5000., 1000., 1.,help='-ve Pumping, +ve Recharge')
                #st.warning('Please keep the Pumping Rate < 50 to generate 3D plot.', icon="⚠️")
            with col2:
                x_coo = st.number_input("X-Coordinate of Well (m)", 1, 199, 30)
                y_coo = st.number_input("Y-Coordinate of Well (m)", 100, 899, 200)

            if st.button("Add Values for Well"):
                st.session_state.we_ls.append([well_id, pump_rate, x_coo, y_coo])
                st.success("Successfully Added Values for Well: {}".format(well_id))   
#---------------------------------------------------------------------Read_Well-----------------------------------------------------------------------------------            
#---------------------------------------------------------------------Update_Well--------------------------------------------------------------------------------
        elif choice_well == "Update Data":
            if len(st.session_state.we_ls)== 0 :
                st.write("Enter Data, Current Data set Empty")
                df = pd.DataFrame(st.session_state.we_ls, columns=['Well ID', 'Pumping Rate', 'X-Coordinates', 'Y-Coordinates'])
                st.dataframe(df)
            if len(st.session_state.we_ls)!= 0 :
                st.subheader("Edit/Update Values")
                #results = view_all_data()
                with st.expander("Current Data"):
                    df = pd.DataFrame(st.session_state.we_ls, columns=['Well ID', 'Pumping Rate', 'X-Coordinates', 'Y-Coordinates'])
                    st.dataframe(df)

                list_of_data = [i[0] for i in st.session_state.we_ls]  
                selected_data = st.selectbox("Well ID to Edit", list_of_data)
                selected_result = [sublist for sublist in st.session_state.we_ls if sublist[0] == selected_data]
                
                #st.write(selected_result)
                if selected_result:
                    well_id = selected_result[0][0]
                    pump_rate = selected_result[0][1]
                    x_coo = selected_result[0][2]
                    y_coo = selected_result[0][3]


                    col1, col2 = st.columns(2)
                    with col1:
                        new_well_id = int(st.number_input("Well ID (n)", well_id))
                        #----------limit pump_rate input upto 50 for 2D and 3D plot runtime error-----------------
                        new_pump_rate = st.number_input("Pumping / Recharge Rate in (m\u00B3/day):", -5000., 5000., float(pump_rate),help='-ve Pumping, +ve Recharge')
                        #st.warning('Please keep the Pumping Rate < 50 to generate 3D plot.', icon="⚠️")
                    with col2:
                        new_x_coo = st.number_input("X-Coordinate (m)", 1., 199., float(x_coo))
                        new_y_coo = st.number_input("Y-Coordinate (m)", 100.,899., float(y_coo))

                    if st.button("Update Values for Well"):
                        st.session_state.we_ls = [sublist for sublist in st.session_state.we_ls if sublist[0] != selected_data]
                        #st.write(st.session_state.we_ls)
                        st.session_state.we_ls.append([new_well_id,new_pump_rate,new_x_coo,new_y_coo])
                        st.success("Successfully Updated :: {} To :: {}".format(well_id, new_well_id))
                        #st.session_state.we_ls = [sublist for sublist in st.session_state.we_ls if sublist != selected_result]

                #results2 = view_all_data()
                with st.expander("Updated Data"):
                    df2 = pd.DataFrame(st.session_state.we_ls, columns=['Well ID', 'Pumping Rate', 'X-Coordinates', 'Y-Coordinates'])
                    st.dataframe(df2)
#---------------------------------------------------------------------------------Delete_Well--------------------------------------------------------------------------

        elif choice_well == "Delete Data":
            if len(st.session_state.we_ls)== 0 :
                st.write("Enter Data, Current Data set Empty")
                df = pd.DataFrame(st.session_state.we_ls, columns=['Well ID', 'Pumping Rate', 'X-Coordinates', 'Y-Coordinates'])
                st.dataframe(df)
            if len(st.session_state.we_ls)!= 0 :
                st.subheader("Delete Values")
                #results = view_all_data()
                with st.expander("Current Data"):
                    df = pd.DataFrame(st.session_state.we_ls, columns=['Well ID', 'Pumping Rate', 'X-Coordinates', 'Y-Coordinates'])
                    st.dataframe(df)

                list_of_data = [i[0] for i in st.session_state.we_ls]
                selected_data = st.selectbox("Well ID to Delete", list_of_data)
                st.warning("The Well ID {} will be Deleted".format(selected_data))
                if st.button("Delete Values for Well"):
                    #delete_id(selected_data)
                    st.session_state.we_ls = [sublist for sublist in st.session_state.we_ls if sublist[0] != selected_data]
                    st.success("Well ID is Deleted Successfully")

            #results3 = view_all_data()
                with st.expander("Current Data"):
                    df3 = pd.DataFrame(st.session_state.we_ls, columns=['Well ID', 'Pumping Rate', 'X-Coordinates', 'Y-Coordinates'])
                    st.dataframe(df3)
        #st.subheader(":blue[View Values]")
       # results = view_all_data()
        st.divider()
            #st.write(results)
        ############## Displaying Data
        col1, col2 = st.columns(2)
        with col1 :
            st.subheader(":blue[View All Data]")
        with col2:
            st.write('')
            if st.checkbox("Display Current Well Data"):
                df = pd.DataFrame(st.session_state.we_ls, columns=['Well ID', 'Pumping Rate', 'X-Coordinates', 'Y-Coordinates'])
                st.dataframe(df)
                #df = pd.DataFrame(results, columns=['Well ID', 'Pumping Rate', 'X-Coordinates', 'Y-Coordinates'])
                if st.download_button(key="well_download", label='Download Table', data=df.to_csv(),mime='text/csv'):
                    st.success("Your File was Successfully Downloaded")
        st.divider()
        #st.session_state.we_ls=we_ls
    #st.session_state.we_ls=we_ls
#-----------------------------------------------------------------------------------Well Finish------------------------------------------------------------------------    
    
    

    #menu_clg = ["Create", "Read", "Update", "Delete"]
    #choice_clg = st.sidebar.selectbox("Please Select Action", menu_clg)


    with clo_dc :
        #st.markdown("""---""")
        #st.sidebar.markdown("---")
        #cf_ls
        col1, col2 = st.columns(2)
        with col1:
            
            st.subheader(':blue[Clogging Factor]')
        with col2:
                
            #if st.checkbox("Activate Clogging Factor"):
                menu_clg = ["New Data", "Update Data", "Delete Data"]
                choice_clg = st.selectbox("Select Action (Clogging Factor)", menu_clg)
                if len(st.session_state.cf_ls)!=0:
                        choice_clg="Update Data" 
        st.divider()
        st.subheader(":blue[Add Values]")
        col1,col2=st.columns(2)
        
        
                #create_table_clg()
        if choice_clg == "New Data":
                    with col1:
                        #clg_id = st.number_input("Colmation Layer ID (n):", 1.,1.,1.)
                        clg_id=1
                        kd = st.number_input("Hydraulic Condutivity of Layer (m/day):", 0.01, 10., 0.1)
                    with col2:
                        dc = st.number_input("Thickness of Clogged Layer (cm):", 0., 50.,1.)
                        dc=dc/100
                    if st.button("Add Values for Clogging Factor"):
                        st.session_state.cf_ls.append([clg_id, kd, dc])
                        st.success("Colmation Layer {} Added".format(clg_id))

                    #st.sidebar.info("In Progress")

        elif choice_clg == "Update Data":
                    if len(st.session_state.cf_ls)== 0 :
                        st.write("Enter Data, Current Data set Empty")
                        df_clg = pd.DataFrame(st.session_state.cf_ls, columns=['Layer ID', 'K Value', 'D Value'])
                        st.dataframe(df_clg)
                    if len(st.session_state.cf_ls)!=0 :
                        #results_clg = view_all_data_clg()
                        with st.expander("Current Data"):
                            df_clg = pd.DataFrame(st.session_state.cf_ls, columns=['Layer ID', 'K Value', 'D Value'])
                            st.dataframe(df_clg)

                        list_of_data_clg = [i[0] for i in st.session_state.cf_ls]
                        selected_data_clg = st.selectbox("Layer ID to Edit:", list_of_data_clg)
                        selected_result_clg = [sublist for sublist in st.session_state.cf_ls if sublist[0] == selected_data_clg]
                        
                        #selected_result_clg = get_id_clg(selected_data_clg)

                        if selected_result_clg:
                            clg_id = selected_result_clg[0][0]
                            kd = selected_result_clg[0][1]
                            dc = selected_result_clg[0][2]
                            
                            with col1:
                                #new_clg_id = st.number_input("Colmation Layer ID (n):", 1.,1., float(clg_id))
                                new_kd = st.number_input("Hydraulic Condutivity of Layer (m/day):", 0.01, 10., float(kd))
                                new_clg_id=1
                            with col2:
                                #new_kd = st.number_input("Hydraulic Condutivity of Layer (m/day):", 0., 1000., float(kd))
                                new_dc = st.number_input("Thickness of Layer (m):", 0., 50., float(dc))

                            if st.button("Update Values."):
                                st.session_state.cf_ls=[]
                                j=[]
                                j.append([new_clg_id,new_kd,new_dc])
                                st.session_state.cf_ls=j
                                st.success("Successfully Updated :: {} To :: {}".format(clg_id, new_clg_id))
                                #st.session_state.cf_ls = [sublist for sublist in st.session_state.cf_ls if sublist != selected_result_clg]


                        #results4 = view_all_data_clg()
                        with st.expander("Updated Data"):
                            df4 = pd.DataFrame(st.session_state.cf_ls, columns=['Layer ID', 'K Value', 'D Value'])
                            st.dataframe(df4)


        elif choice_clg == "Delete Data":
                    if len(st.session_state.cf_ls)== 0 :
                        st.write("Enter Data, Current Data set Empty")
                        df_clg = pd.DataFrame(st.session_state.cf_ls, columns=['Layer ID', 'K Value', 'D Value'])
                        st.dataframe(df_clg)
                    if len(st.session_state.cf_ls) !=0 :
                    #results_clg = view_all_data_clg()
                        with st.expander("Current Data"):
                            df_clg = pd.DataFrame(st.session_state.cf_ls, columns=['Layer ID', 'K Value', 'D Value'])
                            st.dataframe(df_clg)
                        list_of_data_clg = [i[0] for i in st.session_state.cf_ls]
                        selected_data_clg = st.sidebar.selectbox("Layer ID to Edit", list_of_data_clg)
                        st.warning("The Layer ID {} will be Deleted".format(selected_data_clg))
                        if st.button("Delete Values for Clogging"):
                            #delete_id_clg(selected_data_clg)
                            st.session_state.cf_ls = [sublist for sublist in st.session_state.cf_ls if sublist[0] != selected_data_clg]
                            st.success("Layer ID is Deleted Successfully")
                #results_clg = view_all_data_clg()
        st.divider()
                ##################### Displaying Data
        col1, col2 = st.columns(2)
        with col1 :
                st.subheader(":blue[View All Data]")
        with col2:
                st.write('')
                if st.checkbox("Display Current Clogging Data"):
                #with st.expander("View All Data"):
                    df_clg = pd.DataFrame(st.session_state.cf_ls, columns=['Layer ID', 'K Value', 'D Value'])
                    st.dataframe(df_clg)
        st.divider()
                #st.session_state.cf_ls=cf_ls
            #st.session_state.cf_ls=cf_ls

        #st.sidebar.markdown("---")

    

    with updown :

        st.header(":blue[Data Retrival and Backup]")

        view,retri,back=st.tabs(["**View Data**","**Upload Data**","**Download Data**"])
        with view:
            if not bool(st.session_state.aq_ls) and not bool(st.session_state.we_ls) and not bool(st.session_state.cf_ls):

                st.info("No data added yet!")
            else:
                if st.session_state.aq_ls:
                    df3_aq = pd.DataFrame(st.session_state.aq_ls, columns=['Aquifer ID', 'Thickness', 'Base Flow', 'Porosity', 'Hydraulic Conductivity', 'Reference Head'])
                    st.dataframe(df3_aq)
                if st.session_state.we_ls:
                    df = pd.DataFrame(st.session_state.we_ls, columns=['Well ID', 'Pumping Rate', 'X-Coordinates', 'Y-Coordinates'])
                    st.dataframe(df)
                if st.session_state.cf_ls:
                    df_clg = pd.DataFrame(st.session_state.cf_ls, columns=['Layer ID', 'K Value', 'D Value'])
                    st.dataframe(df_clg)

        with retri :
            # Upload the file (CSV or Excel)
            uploaded_file = st.file_uploader("**Upload a CSV or Excel file**", type=["csv", "xlsx"])

            if uploaded_file is not None:
                # Determine file format and read the uploaded file into a DataFrame
                if uploaded_file.name.endswith('csv'):
                    df = pd.read_csv(uploaded_file)
                elif uploaded_file.name.endswith('xlsx'):
                    df = pd.read_excel(uploaded_file)

                # Divide the DataFrame based on the column headers
                aquifer_data = df[['Aquifer ID', 'Thickness', 'Base Flow', 'Porosity', 'Hydraulic Conductivity', 'Refernce Head']]
                well_data = df[['Well ID', 'Pumping Rate', 'X-Coordinates', 'Y-Coordinates']]
                clogging_factor_data = df[['Layer ID', 'K Value', 'D Value']]

                # Display the parts
                st.write(":blue[Aquifer Data]")
                st.dataframe(aquifer_data)

                st.write(":blue[Well Data]")
                st.dataframe(well_data)

                st.write(":blue[Clogging Factor Data]")
                st.dataframe(clogging_factor_data)

                # Convert to lists and store in session_state
                st.session_state.aq_ls = aquifer_data.values.tolist()
                st.session_state.we_ls = well_data.values.tolist()
                st.session_state.cf_ls = clogging_factor_data.values.tolist()

        with back :
            #st.subheader(":blue[Data Backup]")
            #st.write(":[Click ]")
            df3_aq = pd.DataFrame(st.session_state.aq_ls, columns=['Aquifer ID', 'Thickness', 'Base Flow', 'Porosity', 'Hydraulic Conductivity', 'Refernce Head'])
            #st.dataframe(df3_aq)

            df = pd.DataFrame(st.session_state.we_ls, columns=['Well ID', 'Pumping Rate', 'X-Coordinates', 'Y-Coordinates'])
            #st.dataframe(df)


            df_clg = pd.DataFrame(st.session_state.cf_ls, columns=['Layer ID', 'K Value', 'D Value'])
            #st.dataframe(df_clg)

            merged_df = df3_aq.merge(df, left_on='Aquifer ID', right_on='Well ID', how='inner')
            merged_df = merged_df.merge(df_clg, left_on='Aquifer ID', right_on='Layer ID', how='inner')
            merged_df.to_csv('RBF_sim_input', index=False)
            merged_df.to_csv('RBF_sim_input', index=False)
            merged_df.to_excel('RBF_sim_input.xlsx', index=False)
            format_option = st.radio("**Select format:**", ["CSV", "Excel"])
            if format_option == "CSV":
                with open('RBF_sim_input.csv', 'rb') as f_csv:
                    data = f_csv.read()
                file_name = 'RBF_sim_input.csv'
                mime_type = 'text/csv'
            else:
                with open('RBF_sim_input.xlsx', 'rb') as f_xlsx:
                    data = f_xlsx.read()
                file_name = 'RBF_sim_input.xlsx'
                mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

            # Download button
            st.download_button(label=f'Download {format_option}', data=data, file_name=file_name, key='merged_data', mime=mime_type)

            # Display the merged dataframe
            # st.dataframe(merged_df)






