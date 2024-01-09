# RBFsim

RBFsim is an implementation of Analytic Element Method (AEM) for analyzing a very basic River Bank Filtration (RBF) scenario.


<img src="https://github.com/HTWDMAR/RBFsim/blob/main/Manual/RBFsim.png" width="400" height="250">

The current code can simulate:

1. Single and multiple (<6) wells
2. Calculate river water portion in the filterate
3. Calculate river capture length
4. Compute travel time for river water to the well
5. Include impact of riverbed clogging
6. Visualization (isolines streamlines etc) for the above scenario.

The RBFsim results have been verified using **MODFLOW** results. The MODFLOW results (in **JUPYTER** notebook fromat) can be obtained from [here]

## How to use the code:

The code currently can be used both as offline (preferred) and online mode (in development). Following steps need to be followed for running the code in **offline** mode. The interface of the code is based on Python [**streamlit**](https://streamlit.io/) library. The interface of RBFsim (online/0ffline)is:

<img src="https://github.com/HTWDMAR/RBFsim/blob/main/Manual/RBFsim%20Interface.png" width="700" height="400">


## Steps for using code 

1. Make sure that you have Python installed in your system and the Python libraries provided in the [requirements.txt](https://github.com/HTWDMAR/RBFsim/blob/main/requirements.txt)
2. Download the code as a zip file and extract it to any folder in your system
3. From the folder, run the command _**`streamlit app.py`**_
   
    using [VScode](https://code.visualstudio.com/) or any such IDE or also command-prompt that can execute the Python command.
4. The RBFsim interface (seen above) will open in your default browser
5. For performing simulations follow the steps described in the user (under development) [manual](https://github.com/HTWDMAR/RBFsim/blob/main/Manual/RBFsim%20User%20Manual_03.09.2022.pdf) 

### Running the online app

The online app of RBFsim can be run from:
[**https://rbf-sim.streamlit.app/**](https://rbf-sim.streamlit.app/)

## Output from RBFsim
RBFsim provides visuals as wells as numerical results. The numerical results can be downloaded as **CSV** file. The graphics can be downloaded as **PNG** file. Check the user [manual](https://github.com/HTWDMAR/RBFsim/blob/main/Manual/RBFsim%20User%20Manual_03.09.2022.pdf) for more complete details.

**Few screenshots from RBFsim**

<img src="https://github.com/HTWDMAR/RBFsim/blob/main/Manual/screenshot.png" width="800" height="300">



The codes in this site are **CC BY 4.0** licensed. The license wording can be found [here](https://creativecommons.org/licenses/by/4.0/).
Basically, for using code from here- the original authors should be credited.


Following authors are credited for this version [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10040816.svg)](https://doi.org/10.5281/zenodo.10040816) of the code (names not in any order):

1. **Dr P. K. Yadav** - For conceptualization and basic code development
2. **M. Tufail** - Main code development for online implementation
3. **V. Cantarella** - Offline code and verification
4. **A. Villa** - offline code and case studies
5. **M Gomez** - offline code and case studies
6. **Tassilo Reuschling** - First offline code development
7. **Prof. Dr T. Grischek** - Supervisory support on contents
8. **Prof. Dr A. Hartmann** - Supervisory support on contents
9. **Vibhu Batheja** 
10. **Anton Kohler**

## References

- Coming up


## Funding:

This project was partially funded by BMBF MEWAC-FEMAR Project (grant no. 02WME1612A-C, Prof. T. Grischek)
