import streamlit as st
from multiapp import MultiApp
import home, theory, result, help_page, data_col # import your app modules here


app = MultiApp()
st.set_page_config(
        page_title="Riverbank Filtration tool **_RBFsim_**",
        layout="wide",

        )


# Add all your application here
app.add_app("Home", home.app)
app.add_app("Theory", theory.app)
app.add_app("Data Collection", data_col.app)
#app.add_app("Calculations", calculations.app)
app.add_app("Results", result.app)
app.add_app("Case Study", help_page.app)


with st.sidebar.expander("About"):
     st.warning("""
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



**References**

- Coming up

     """)



# The main app
app.run()
