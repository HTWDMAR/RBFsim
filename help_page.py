import streamlit as st
import numpy as np
import streamlit.components.v1 as components
import base64

#def displayPDF(file):
    # Opening file from file path
    #with open(file, "rb") as f:
        #base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Embedding PDF in HTML
    


def app():
	#st.title("This is help page")

	y = np.asarray([0.0879, 0.1455, 0.1976, 0.2474, 0.2962, 0.3446, 0.3931, 0.4419, 0.4914,
			0.5417, 0.5929, 0.6452, 0.6988, 0.7537, 0.8102, 0.8681, 0.9279, 0.9894, 1.0529,
			1.1185, 1.1863, 1.2564, 1.3290, 1.4043, 1.4823, 1.5633, 1.6475, 1.7349, 1.8259,
			1.9207, 2.0194, 2.1223, 2.2297, 2.3419, 2.4591, 2.5817, 2.7100, 2.8445, 2.9855,
			3.1335, 3.2889, 3.4523, 3.6243, 3.8059, 3.9964, 4.1980, 4.4109, 4.6362, 4.8748,
			5.1277, 5.3961, 5.6814, 5.9850, 6.3086, 6.6537, 7.0227, 7.4178, 7.8409, 8.2955,
			8.7845, 9.3115, 9.881, 10.4964, 11.1641, 11.8897, 12.6803, 13.5437, 14.4892, 15.5277,
			16.6716, 17.9358, 19.3378, 20.8983, 22.6423, 24.5996, 26.8066, 29.3075, 32.1572, 35.4235,
			39.1918, 43.5705, 48.6991, 54.7590, 61.9903, 70.7154, 81.3762, 94.5906, 111.245, 132.644,
			160.779, 198.807, 251.969, 329.511, 448.983, 647.122, 1011.878, 1799.932, 4051.51, 16210.05])

	x = np.asarray([0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10,
			0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.20, 0.21,
			0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.30, 0.31, 0.32, 
			0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.40, 0.41, 0.42, 0.43,
			0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.50, 0.51, 0.52, 0.53, 0.54, 
			0.55, 0.56, 0.57, 0.58, 0.59, 0.60, 0.61, 0.62, 0.63, 0.64, 0.65,
			0.66, 0.67, 0.68, 0.69, 0.70, 0.71, 0.72, 0.73, 0.74, 0.75, 0.76, 0.77, 0.78, 0.79,
			0.80, 0.81, 0.82, 0.83, 0.84, 0.85, 0.86, 0.87, 0.88, 0.89, 0.90, 0.91, 0.92, 0.93,
			0.94, 0.95, 0.96, 0.97, 0.98, 0.99])	

	st.sidebar.markdown("---")
	st.title(":red[Estimate Parameters]")
	e1,e2,e3 = st.tabs(["**Estimate Distance**", "**Estimate Baseflow**","**Estimate Well Q**"])
	with e1:

		t1, t2,t3 = st.columns([1.75,0.25, 1.25])
		with t1:
			st.subheader(":blue[Estimate Distance:]")
			alpha_value = st.number_input("Enter Desired Contribution Ratio \u03B1:", 0.010)
			beta_value = np.interp(alpha_value, x, y)
			beta = beta_value
			Q_beta = st.number_input("Pumping / Recharge Rate [m\u00B3/day]:",0., 10000., 1.0)
			Qx_beta = st.number_input("Baseflow in X-Direction [m\u00B2/day]:",1.,1000.,1.)
			d_button = st.button("Calculate Distance")
			d_value = Q_beta/(np.pi*(beta+1)*Qx_beta)
			d_value_int = np.round(np.float64(d_value), 2)
			if d_button:
				st.markdown(""" ### Distance to the Well = {} m """.format(d_value_int))					
		with t2:
                        st.write('')
		with t3:
			st.subheader(":blue[Equation:]")
			st.markdown("***(From Holzbecher, 2013)***")
			st.markdown("")
			st.markdown("")
			st.latex(r'''
				f(\beta) = -\arctan(\sqrt{\beta}) + \frac{\sqrt{\beta}}{\beta+1} + \frac{\Pi\alpha}{2}
			''')
			st.latex(r'''
				\alpha = \text{Distribution Ratio}
			''')
			st.latex(r'''
				\beta = \frac{1}{\Pi d} \frac{Q}{Qxo}
			''')
	
			st.markdown("")
			st.markdown("")
			st.markdown("")

		st.markdown("---")
	st.info("Holzbecher, E. (2013), Analytical Solution for Well Design with Respect to Discharge Ratio. Groundwater, 51: 128-134. ***[https://doi.org/10.1111/j.1745-6584.2012.00927.x](https://doi.org/10.1111/j.1745-6584.2012.00927.x)***.")

	with e2:
				

		t1,t2,t3 = st.columns([1.75,0.25, 1.25])
		with t1:
			st.subheader(":blue[Estimate Baseflow:]")
			alpha_value = st.number_input("Enter Desired Contribution Ratio \u03B1:", 0.011)
			beta_value = np.interp(alpha_value, x, y)
			beta = beta_value
			Q_beta = st.number_input("Pumping / Recharge Rate [m\u00B3/day]:",0.1, 10001., 1.0)
			dist_beta = st.number_input("Distance from the Well [m]:",1.,200.,1.)
			Qx_button = st.button("Calculate Baseflow")
			Qx_beta_1 = Q_beta/(np.pi*(beta+1)*dist_beta)
			Qx_beta_1_int = np.round(np.float64(Qx_beta_1), 2)
			if Qx_button:
                                st.markdown(""" ### Base Flow in X-Direction = {} m\u00B2/day """.format(Qx_beta_1_int))

		with t3:
			st.subheader(":blue[Equation:]")
			st.markdown("")
			st.markdown("")
			st.markdown("")
			st.latex(r'''
				f(\beta) = -\arctan(\sqrt{\beta}) + \frac{\sqrt{\beta}}{\beta+1} + \frac{\Pi\alpha}{2}
			''')
			st.latex(r'''
				\alpha = \text{Distribution Ratio}
			''')
			st.latex(r'''
				\beta = \frac{1}{\Pi d} \frac{Q}{Qxo}
			''')

			st.markdown("")
			st.markdown("")
			st.markdown("")
		st.markdown("---")

	with e3:
			

		t1,t2,t3 = st.columns([1.75,0.25, 1.25])
		with t1:
			st.subheader(":blue[Estimate Well Q:]")
			alpha_value = st.number_input("Enter Desired Contribution Ratio \u03B1:", 0.012)
			beta_value = np.interp(alpha_value, x, y)
			beta = beta_value
			Qx_beta = st.number_input("Baseflow in X-Direction [m\u00B2/day]:",1.,1002.,1.)
			dist_beta = st.number_input("Distance from the Well [m]:",1.,201.,1.)
			Q_button = st.button("Calculate Well Q")
			Q_beta_1 = Qx_beta*dist_beta*np.pi*(beta+1)
			Q_beta_1_int = np.round(np.float64(Q_beta_1), 2)	
			if Q_button:
				st.markdown(""" ### Well Discharge = {} m\u00B3/day """.format(Q_beta_1_int))
		with t3:
			st.subheader(":blue[Equation:]")
			st.markdown("")
			st.markdown("")
			st.markdown("")
			st.latex(r'''
				f(\beta) = -\arctan(\sqrt{\beta}) + \frac{\sqrt{\beta}}{\beta+1} + \frac{\Pi\alpha}{2}
			''')
			st.latex(r'''
				\alpha = \text{Distribution Ratio}
			''')
			st.latex(r'''
				\beta = \frac{1}{\Pi d} \frac{Q}{Qxo}
			''')

			st.markdown("")
			st.markdown("")
			st.markdown("")
			
		
		st.markdown("---")

		#pdf_path = "C:/Users/Working/GWbookdownloads/GW/RBF_Sim/RBFsim-main/local.pdf"

		#pdf_url = f"file://{pdf_path}"

		#pdf_display = f'<iframe src="{pdf_path}" width="700" height="1000" type="application/pdf"></iframe>'
		#st.markdown(pdf_display, unsafe_allow_html=True)


	#st.sidebar.markdown("---")