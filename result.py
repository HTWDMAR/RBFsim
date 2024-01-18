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
from contrib import river_length
from PIL import Image
from plot import *
from pdf_report import PDF
from datetime import date

def app():
	st.sidebar.divider()
	st.title(":red[Results and visualizations]")
	
	view_plots, report = st.tabs(["**View Results**", "**Download Report**"])
	if 'aq_ls' and 'we_ls' and 'cf_ls' not in st.session_state:        
		with view_plots:
			st.subheader(":blue[Please Input Data for the simulation]")
		with report:
			st.subheader(":blue[Please Input Data for the simulation]")
	#st.write("Using Previous Database Data")
	#st.write(st.session_state.aq_ls)
	if 'aq_ls' and 'we_ls' and 'cf_ls' in st.session_state :
		df_clg = pd.DataFrame(st.session_state.cf_ls, columns=['Layer ID', 'K Value (m/day)', 'D Value (m)'])
		value_list_dfs = {}
		modified_aq_ls = [[*inner[1:]] for inner in st.session_state.aq_ls]
		aq_ls_df = pd.DataFrame(modified_aq_ls, columns=['Thickness (m)', 'Base Flow (m\u00B2/day)', 'Porosity', 'Hydraulic Conductivity (m/day)', 'Reference Head (m)'])

		value_list_dfs["Aquifier Data"] = aq_ls_df
		we_ls_df = pd.DataFrame(st.session_state.we_ls, columns=['Well ID', 'Pumping Rate (m\u00B3/day)', 'X-Coordinates (m)', 'Y-Coordinates (m)'])
		value_list_dfs["Well Data"] = we_ls_df
		plots = {} 
		bf_dict = None #initialize variable for bank filtrate calculation results
		tt_dict = None #initialize variable for time travel calculation results
		#st.write("off we go now")
		#st.write(len(st.session_state.aq_ls))
		if len(st.session_state.aq_ls)==0 and len(st.session_state.we_ls) == 0 :
			with view_plots:
				st.subheader(":blue[Please Input required data for the simulation]")
			with report:
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
			with view_plots:
				if len(results_clg) == 0:
					st.info("No Clogging Factor is Added!")
				else:
					# modified_clg = [[*inner[1:]] for inner in results_clg]
					cf_df = pd.DataFrame(results_clg, columns=['Layer ID', 'Hydraulic Condutivity of Layer (m/day)', 'Thickness of Layer (m)'])
					value_list_dfs["Clogging Factor"] = cf_df
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
					c1, c2 = st.columns(2)

				# ------------------------------------------------------------------Stream / Potential Lines for Multiple Wells-----------------------------    
					with c1:
						if len(results)>(1):
							st.subheader(":blue[Wells in Flow Field:]")
						else:
							st.subheader(":blue[Well in Flow Field:]")
						plot1 = plotting(0, 100, -20, 150, 100)
						b, fig1 = plot1.plot2d(aem_model, levels=8, sharey=False, quiver=False, streams=True, figsize=(18, 12))
						plt.savefig(f'2D_plot.png', transparent=False, facecolor='white', bbox_inches="tight")
						plots["2D Plot"] = "./2D_plot.png"
						st.pyplot(fig1)                        
					

					with c2:
						st.write('')
						st.write('')
						display_3d_plot = st.checkbox(":blue[Display 3D Plot]")
					
					

					# Check if the checkbox is checked
						if display_3d_plot:
							# Assuming `aem_model` is defined somewhere in your code
							b2, fig2 = plot1.plot3d(aem_model)
							plt.savefig(f'3D_plot.png', transparent=False, facecolor='white', bbox_inches="tight")
							plots["3d Plot"]="./3D_plot.png"
							st.pyplot(fig2)

					st.divider()
				
					c1,c2=st.columns(2)
					solv = river_length(aem_model)
						
					length, riv_coords, capture_fraction = solv.solve_river_length()
					tt, ys, avgtt, mintt, traj_array = solv.time_travel(results_aq[0][3], delta_s=0.4, calculate_trajectory=True)
				########### Changed here to modify capture length 
				############### Removing Negative Values 
					riv_coords = [max(0., x) for x in riv_coords]
					length=sum(riv_coords)
					st.sidebar.title(":red[Contribution Portion:]")
					with c1:# ------------------------------------------------------------------CR, TT, RL for One Well ------------------------------------------------
						if len(results) > 1:
							st.sidebar.markdown("---")
							st.sidebar.info("After entering one well, The options will be available here.")
						else:
						
							if st.sidebar.checkbox("Bank Filtrate Portion"):
								st.subheader(":blue[Bank Filterate Portion:]")
								#---moved the following code block inside the if statement block
							
								#moved code block ends---
								#st.sidebar.markdown("---")
								plot = plotting(0, 100, -20, 150, 100, riv_coords)
								b, fig = plot.plot2d(aem_model, sharey=False, traj_array=traj_array, levels=8, quiver=False, streams=True)
								plt.savefig(f'Bank_filtrate_plot.png', transparent=False, facecolor='white', bbox_inches="tight")
								plots["Bank Filtrate Plot"]="./Bank_filtrate_plot.png"
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

								bf_dict = {'Bank Filtrate Portion (%)':f"{bf_ratio_rounded}", 'River Capture Length (m)':f"{riv_length_rounded}", 'Capture Length Location on Y-Axis (m)':f"{riv_0_rounded} & {riv_1_rounded}"}
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
							plt.savefig(f'Time_travel_plot.png', transparent=False, facecolor='white', bbox_inches="tight")
							plots["Time Travel Plot"] = "./Time_travel_plot.png"
							st.pyplot(fig2)

							avg_tt_rounded = int(avgtt)
							min_tt_rounded = int(mintt)

							st.sidebar.metric(label=":blue[Average Travel Time:]", value="{} days".format(avg_tt_rounded))
							st.sidebar.metric(label=":blue[Minimum Travel Time:]", value="{} days".format(min_tt_rounded))

							tt_dict = {'Average Travel Time (days)':f'{avg_tt_rounded}', 'Minimum Travel Time (days)':f'{min_tt_rounded}'}
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

					# input_values_df = pd.concat(value_list_dfs, axis = 1)
									
					

				st.sidebar.markdown("---")
				st.sidebar.title("Download \u03C8 & Head:")
				st.sidebar.download_button(label="Download H in CSV", data=csv, mime="csv")
				st.sidebar.download_button(label="Download \u03C8 in CSV", data=csv_psi, mime="csv")

			with report:
				st.header("Export Simulation Report to PDF")
				report_title = st.text_input("Enter Report Title:", max_chars=50)
				report_download = st.button(label="Export Report to PDF")
				if report_download:                  
					if report_title:
						download_report(report_title, value_list_dfs, plots, bf_dict, tt_dict)
					else:
						download_report("RBF-Sim", value_list_dfs, plots, bf_dict, tt_dict)
							
				
	
def create_download_link(val, filename):
	b64 = base64.b64encode(val)  # val looks like b'...'
	return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download PDF</a>'

def download_report(title, value_list_dfs, plots, bf_dict, tt_dict):
	pdf=PDF('P', 'mm')
	pdf.proj_title = title
	pdf.add_page(format='A4')    
	pdf.set_text_color(0, 51, 102)
	pdf.set_font('Arial', 'I', 9)
	pdf.cell(0, 8, f"Date:{date.today()}", align="R")
	pdf.set_text_color(0, 0, 0)
	pdf.ln(10)
		
	for key, values_df in value_list_dfs.items():
		pdf.set_font('Arial', 'B', 12)
		pdf.set_text_color(0, 51, 102)
		pdf.cell(0, 5, f"Input Data: {key}", ln = 2, align="L")
		pdf.set_text_color(0, 0, 0)
		pdf.ln(1)
		pdf.set_font('Arial', '', 10)
		left_margin = pdf.l_margin
		right_margin = pdf.r_margin
		with pdf.table(line_height=7, width=pdf.w - left_margin - right_margin, align='L') as table:
			headers = values_df.columns.tolist()
			rows = values_df.values.tolist()
			header_row = table.row()
			for header in headers:
				pdf.set_text_color(0, 51, 102)
				header_row.cell(header)    
				pdf.set_text_color(0, 0, 0)        
			for df_row in rows:
				row = table.row()
				for value in df_row:
					row.cell(str(value))
		pdf.ln(5)
		#---formatting for displaying plot images---
	row_count=0
	
	img_margin = 5
	#---if even number of images then allow 2 images per row else allow upto 3---
	if len(plots) == 1:
		img_per_row = 1    
		img_width = pdf.w / 1.75
	elif len(plots) % 2 != 0:
		row = len(plots) / 3
		img_per_row = 3
		img_width = (pdf.w - (left_margin+right_margin +(img_per_row - 1) * 5)) / img_per_row
	else:
		row = len(plots) // 2
		img_per_row = 2
		img_width = (pdf.w - (left_margin+right_margin +(img_per_row - 1) * 5)) / img_per_row
		
	img_heights = [] 
	for label, plot in plots.items():
		img=Image.open(plot)
		w, h = img.size
		aspect_ratio = h / w
		img_height = img_width * aspect_ratio     
		

		if row_count == img_per_row:
			row_count=0
			pdf.set_y(final_y+max(img_heights)+5)  
			img_heights.clear()
			
		if row_count == 0 and (pdf.get_y() + img_height + 15) > pdf.h:
			pdf.add_page(format='A4')    
			# pdf.set_margins(20, 10, 10)
			# pdf.set_x(10)
			pdf.ln(5)
			
			

			
		x = pdf.get_x()
		y = pdf.get_y()
		pdf.set_font('Arial', 'BU', 10)
		pdf.cell(img_width, 10, f"Figure: {label}", ln=1, align='C')    
		final_y = pdf.get_y() 
		p_img = pdf.image(plot, x=x, y=final_y, w=img_width, h=img_height)
		img_heights.append(img_height)
		if label != list(plots.keys())[-1]:
			pdf.set_xy(x+img_width+5, y)   
		else:
			pdf.set_y(final_y+max(img_heights)+5)
		
		row_count += 1
	pdf.ln(5)
	if bf_dict is not None:
		pdf.set_font('Arial', 'B', 12)
		pdf.set_text_color(0, 51, 102)
		pdf.cell(50, 5, "Contribution Portion", ln = 2)
		pdf.set_text_color(0, 0, 0)
		pdf.ln(1)
		pdf.set_font('Arial', '', 10)
		headers = bf_dict.keys()
		rows = bf_dict.values()
		with pdf.table(line_height=7, width=pdf.w/1.5, align='L') as table:
			header_row = table.row()
			row = table.row()
			for header in headers:
				pdf.set_text_color(0, 51, 102)
				header_row.cell(header)    
				pdf.set_text_color(0, 0, 0)    
			for value in rows:
				row.cell(str(value))
			
		pdf.ln(5)
	if tt_dict is not None:
		pdf.set_font('Arial', 'B', 12)
		pdf.set_text_color(0, 51, 102)
		pdf.cell(50, 5, "Time of Travel", ln = 2)
		pdf.set_text_color(0, 0, 0)
		pdf.ln(1)
		pdf.set_font('Arial', '', 10)
		headers = tt_dict.keys()
		rows = tt_dict.values()
		with pdf.table(line_height=7, width=pdf.w/2, align='L') as table:
			header_row = table.row()
			row = table.row()
			for header in headers:
				pdf.set_text_color(0, 51, 102)
				header_row.cell(header)    
				pdf.set_text_color(0, 0, 0)    
			for value in rows:
				row.cell(str(value))
			
			
		pdf.ln(5)
	html = create_download_link(pdf.output(dest="S"), "Report")
	st.markdown(html, unsafe_allow_html=True)
	