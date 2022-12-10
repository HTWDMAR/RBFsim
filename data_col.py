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
from db_fxns import create_table,add_data,view_all_data,view_unique_data,get_id,edit_well_id,delete_id
from db_fxns_aq import create_table_aq,view_all_data_aq,add_data_aq,view_unique_data_aq,get_id_aq,edit_aq_id, delete_id_aq
from db_fxns_aq import create_table_clg,view_all_data_clg,add_data_clg,view_unique_data_clg,get_id_clg,edit_id_clg,delete_id_clg

#-------------------------------------------------------------------------------NavBar-Ends------------------------------------------------------------------------------------------------------------
def app():
    st.title('Data Input Interface:')
    st.markdown("---")
    #st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        options = ['Aquifer', 'Wells']
        #text = st.markdown(""" #### Select Options   """)
        input_options = st.radio('Please Select Option:', options)
    st.markdown("""---""")
    if input_options == "Aquifer":
        with col2:
            menu_aq = ["Create", "Read", "Update", "Delete"]
            choice_aq = st.selectbox("Please Select Action (Aquifer)", menu_aq)
        create_table_aq()
#-------------------------------------------------------------Create_aq-------------------------------------------------------------------------------------------------------------------
        if choice_aq == "Create":
            #st.markdown(""" #### Please Enter the Required Values in Table: """)
            st.subheader("Add Values")
            #st.sidebar.markdown('* **Acquifer Data Input:**')
            col1, col2, col3 = st.columns(3)
            with col1:
                aq_id = st.number_input('Aquifer ID[n]', 1,1,1)
                thk_aq = st.number_input('Thickness of the Aquifer[m]', 1.,500.,20.)
            with col2:
                baseflow = st.number_input('Base Flow in x-Direction [m\u00B2/day]:', -10000., 10000.,0.1)
                ref_head = st.number_input('Refernce Head[m]', 1.,200.,9.5)
            with col3:
                porosity = st.number_input('Porosity:', 0.00,1.00,0.01)
                hyd_con = st.number_input('Hydraulic Conductivity [m/day]', 0.1, 1000., 0.1)
            
            if st.button("Add Values"):
                add_data_aq(aq_id, thk_aq, baseflow, porosity, hyd_con, ref_head)
                st.success("Values added Successfully")                
#-------------------------------------------------------------Read_aq-----------------------------------------------------------------------------------------------------------------------
        elif choice_aq == "Read":
            st.subheader("View Values")
            results_aq = view_all_data_aq()
            #st.write(results_aq)
            with st.expander("View All Data"):
                df_aq = pd.DataFrame(results_aq, columns=['Aquifer ID', 'Thickness', 'Base Flow', 'Porosity', 'Hydraulic Conductivity', 'Refernce Head'])
                st.dataframe(df_aq)
            if st.download_button(label='Download Table', data=df_aq.to_csv(),mime='text/csv'):
                st.success("Your File Successfully Downloaded")
#--------------------------------------------------------------Update_aq--------------------------------------------------------------------------------------------------------------------                    
        elif choice_aq == "Update":
            st.subheader("Edit/Update Values")
            results_aq = view_all_data_aq()
            #st.write(results_aq)
            with st.expander("View All Data"):
                df_aq = pd.DataFrame(results_aq, columns=['Aquifer ID', 'Thickness', 'Base Flow', 'Porosity', 'Hydraulic Conductivity', 'Refernce Head'])
                st.dataframe(df_aq)

            list_of_data_aq = [i[0] for i in view_unique_data_aq()]
            selected_data_aq = st.selectbox("Aquifer ID to Edit", list_of_data_aq)

            selected_result_aq = get_id_aq(selected_data_aq)
            #st.write(selected_result)
            if selected_result_aq:
                aq_id = selected_result_aq[0][0]
                thk_aq = selected_result_aq[0][1]
                baseflow = selected_result_aq[0][2]
                porosity = selected_result_aq[0][3]
                hyd_con = selected_result_aq[0][4]
                ref_head = selected_result_aq[0][5]

                col1, col2, col3 = st.columns(3)
                with col1:
                    new_aq_id = st.number_input("Aquifer ID:", aq_id)
                    new_thk_aq = st.number_input("Thickness of the Aquifer [m]:",1.,500., float(thk_aq))
                with col2:
                    new_baseflow = st.number_input("Base Flow [m\u00B2/day]:",-100.,100., float(baseflow))
                    new_ref_head = st.number_input("Refernce Head [m]:", 1., 500., float(ref_head))
                with col3:
                    new_porosity = st.number_input("Porosity:",0., 1., float(porosity))
                    new_hyd_con = st.number_input("Hydraulic Conductivity [m/day]:",1., 1000., float(hyd_con))
                
                if st.button("Update Values"):
                    edit_aq_id(new_aq_id, new_thk_aq, new_baseflow, new_porosity, new_hyd_con, new_ref_head, aq_id, thk_aq, baseflow, porosity, hyd_con, ref_head)
                    st.success("Values added Successfully")

            

            results2_aq = view_all_data_aq()
            with st.expander("Updated Data"):
                df2_aq = pd.DataFrame(results2_aq, columns=['Aquifer ID', 'Thickness', 'Base Flow', 'Porosity', 'Hydraulic Conductivity', 'Refernce Head'])
                st.dataframe(df2_aq)

#----------------------------------------------------------------------Delete_aq-------------------------------------------------------------------------------------------------
        elif choice_aq == "Delete":
            st.subheader("Delete Values")
            results_aq = view_all_data_aq()
            #st.write(results_aq)
            with st.expander("View All Data"):
                df_aq = pd.DataFrame(results_aq, columns=['Aquifer ID', 'Thickness', 'Base Flow', 'Porosity', 'Hydraulic Conductivity', 'Refernce Head'])
                st.dataframe(df_aq)

            list_of_data_aq = [i[0] for i in view_unique_data_aq()]
            selected_data_aq = st.selectbox("Aquifer ID to Edit", list_of_data_aq)
            st.warning("The Aquifer ID {} will be Deleted".format(selected_data_aq))
            if st.button("Delete Values"):
                delete_id_aq(selected_data_aq)
                st.success("Aquifer ID is Deleted Successfully")

            results3_aq = view_all_data_aq()
            with st.expander("Current Data"):
                df3_aq = pd.DataFrame(results3_aq, columns=['Aquifer ID', 'Thickness', 'Base Flow', 'Porosity', 'Hydraulic Conductivity', 'Refernce Head'])
                st.dataframe(df3_aq)    
#---------------------------------------------------------------------Aquifer Finish-------------------------------------------------------------------------------------    
    
    
    
    
    
    if input_options == "Wells":
        with col2:
            menu_well = ["Create", "Read", "Update", "Delete"]
            choice_well = st.selectbox("Please Select Action (Wells)", menu_well)
        create_table()
#-------------------------------------------------------------------Upload-----------------------------------------------------------------------------------------------        
        '''if choice_well == "Upload":
            st.subheader("Upload File")
            data_file = st.file_uploader("Upload CSV", type=["csv"])
            if data_file is not None:
                st.write(type(data_file))
                df = pd.read_csv(data_file, engine='python')
                st.dataframe(df.head(1))'''




#----------------------------------------------------------------------Create_Well----------------------------------------------------------------------------------------                   
        if choice_well == "Create":
            #st.header(""" **Please Enter the Required Values in Table:** """)
            st.subheader("Add Values")

            #Layout of the Main_Page
            col1, col2 = st.columns(2)
            with col1:
                well_id = st.number_input("Well ID[n]", 1, 10, 1)
                pump_rate = st.number_input("Pumping / Recharge Rate in [m\u00B3/day]:",-10000.,10000.,1.,0.1)
            with col2:
                x_coo = st.number_input("X-Coordinates[m]", 1., 199.)
                y_coo = st.number_input("Y-Coordinates[m]", 1., 199.)

            if st.button("Add Values"):
                add_data(well_id, pump_rate, x_coo, y_coo)
                st.success("Successfully Added Values for Well: {}".format(well_id))   
#---------------------------------------------------------------------Read_Well-----------------------------------------------------------------------------------

        elif choice_well == "Read":
            st.subheader("View Values")
            results = view_all_data()
            #st.write(results)
            with st.expander("View All Data"):
                df = pd.DataFrame(results, columns=['Well ID', 'Pumping Rate', 'X-Coordinates', 'Y-Coordinates'])
                st.dataframe(df)
            if st.download_button(label='Download Table', data=df.to_csv(),mime='text/csv'):
                st.success("Your File Successfully Downloaded")             
#---------------------------------------------------------------------Update_Well--------------------------------------------------------------------------------
        elif choice_well == "Update":
            st.subheader("Edit/Update Values")
            results = view_all_data()
            with st.expander("Current Data"):
                df = pd.DataFrame(results, columns=['Well ID', 'Pumping Rate', 'X-Coordinates', 'Y-Coordinates'])
                st.dataframe(df)

            list_of_data = [i[0] for i in view_unique_data()]
            selected_data = st.selectbox("Well ID to Edit", list_of_data)

            selected_result = get_id(selected_data)
            #st.write(selected_result)
            if selected_result:
                well_id = selected_result[0][0]
                pump_rate = selected_result[0][1]
                x_coo = selected_result[0][2]
                y_coo = selected_result[0][3]


                col1, col2 = st.columns(2)
                with col1:
                    new_well_id = st.number_input("Well ID[n]", well_id)
                    new_pump_rate = st.number_input("Pumping / Recharge Rate in [m\u00B3/day]:", -10000., 10000., float(pump_rate))
                with col2:
                    new_x_coo = st.number_input("X-Coordinates[m]", 1., 199., float(x_coo))
                    new_y_coo = st.number_input("Y-Coordinates[m]", 1.,199., float(y_coo))

                if st.button("Update Values"):
                    edit_well_id(new_well_id,new_pump_rate,new_x_coo,new_y_coo, well_id, pump_rate, x_coo, y_coo)
                    st.success("Successfully Updated :: {} To :: {}".format(well_id, new_well_id))

            results2 = view_all_data()
            with st.expander("Updated Data"):
                df2 = pd.DataFrame(results2, columns=['Well ID', 'Pumping Rate', 'X-Coordinates', 'Y-Coordinates'])
                st.dataframe(df2)
#---------------------------------------------------------------------------------Delete_Well--------------------------------------------------------------------------

        elif choice_well == "Delete":
            st.subheader("Delete Values")
            results = view_all_data()
            with st.expander("Current Data"):
                df = pd.DataFrame(results, columns=['Well ID', 'Pumping Rate', 'X-Coordinates', 'Y-Coordinates'])
                st.dataframe(df)

            list_of_data = [i[0] for i in view_unique_data()]
            selected_data = st.selectbox("Well ID to Delete", list_of_data)
            st.warning("The Well ID {} will be Deleted".format(selected_data))
            if st.button("Delete Values"):
                delete_id(selected_data)
                st.success("Well ID is Deleted Successfully")

            results3 = view_all_data()
            with st.expander("Current Data"):
                df3 = pd.DataFrame(results3, columns=['Well ID', 'Pumping Rate', 'X-Coordinates', 'Y-Coordinates'])
                st.dataframe(df3)    
#-----------------------------------------------------------------------------------Well Finish------------------------------------------------------------------------    
    
    

    #menu_clg = ["Create", "Read", "Update", "Delete"]
    #choice_clg = st.sidebar.selectbox("Please Select Action", menu_clg)



    st.markdown("""---""")
    st.sidebar.markdown("---")
    st.sidebar.title("Clogging Factor:")
    if st.sidebar.checkbox("Clogging Factor"):
        menu_clg = ["Create", "Read", "Update", "Delete"]
        choice_clg = st.sidebar.selectbox("Please Select Action", menu_clg)
        create_table_clg()
        if choice_clg == "Create":
            clg_id = st.sidebar.number_input("Colmation Layer ID [n]:", 1.,1.,1.)
            kd = st.sidebar.number_input("Hydraulic Condutivity of Layer [m/day]:", 0., 1000., 0.)
            dc = st.sidebar.number_input("Thickness of Layer [m]:", 0., 1000.,0.)
        
            if st.sidebar.button("Add Values."):
                add_data_clg(clg_id, kd, dc)
                st.sidebar.success("Colmation Layer {} Added".format(clg_id))

        elif choice_clg == "Read":
            results_clg = view_all_data_clg()
            with st.sidebar.expander("View All Data"):
                df_clg = pd.DataFrame(results_clg, columns=['Layer ID', 'K Value', 'D Value'])
                st.dataframe(df_clg)
            #st.sidebar.info("In Progress")

        elif choice_clg == "Update":
            results_clg = view_all_data_clg()
            with st.sidebar.expander("Current Data"):
                df_clg = pd.DataFrame(results_clg, columns=['Layer ID', 'K Value', 'D Value'])
                st.dataframe(df_clg)

            list_of_data_clg = [i[0] for i in view_unique_data_clg()]
            selected_data_clg = st.sidebar.selectbox("Layer ID to Edit:", list_of_data_clg)
            
            selected_result_clg = get_id_clg(selected_data_clg)

            if selected_result_clg:
                clg_id = selected_result_clg[0][0]
                kd = selected_result_clg[0][1]
                dc = selected_result_clg[0][2]
                

                new_clg_id = st.sidebar.number_input("Colmation Layer ID [n]:", 1.,1., float(clg_id))
                new_kd = st.sidebar.number_input("Hydraulic Condutivity of Layer [m/day]:", 0., 1000., float(kd))
                new_dc = st.sidebar.number_input("Thickness of Layer [m]:", 0., 1000., float(dc))

                if st.sidebar.button("Update Values."):
                    edit_id_clg(new_clg_id,new_kd,new_dc, clg_id, kd, dc)
                    st.sidebar.success("Successfully Updated :: {} To :: {}".format(clg_id, new_clg_id))


            results4 = view_all_data_clg()
            with st.sidebar.expander("Updated Data"):
                df4 = pd.DataFrame(results4, columns=['Layer ID', 'K Value', 'D Value'])
                st.dataframe(df4)


        elif choice_clg == "Delete":
            results_clg = view_all_data_clg()
            with st.sidebar.expander("Current Data"):
                df_clg = pd.DataFrame(results_clg, columns=['Layer ID', 'K Value', 'D Value'])
                st.dataframe(df_clg)
            list_of_data_clg = [i[0] for i in view_unique_data_clg()]
            selected_data_clg = st.sidebar.selectbox("Layer ID to Edit", list_of_data_clg)
            st.sidebar.warning("The Layer ID {} will be Deleted".format(selected_data_clg))
            if st.sidebar.button("Delete Values."):
                delete_id_clg(selected_data_clg)
                st.sidebar.success("Layer ID is Deleted Successfully")

    st.sidebar.markdown("---")
