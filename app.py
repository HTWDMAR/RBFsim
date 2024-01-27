import streamlit as st
from multiapp import MultiApp
import home, result, help_page, data_col, new_help # import your app modules here



st.set_page_config(
    layout="centered", page_title="RBFsim", page_icon="♨"
)


app = MultiApp()


# Add all your application here
app.add_app("Home", home.app)
#app.add_app("Theory", theory.app)
app.add_app("Data Collection", data_col.app)
app.add_app("Results", result.app)
app.add_app("Parameter Estimation", help_page.app)
app.add_app("Help Page",new_help.app)



# The main app
app.run()
