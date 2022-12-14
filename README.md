# RBFsim

RBFsim is an implementation of Analytic Element Method (AEM) for analyzing a very basic River Bank Filtration (RBF) scenario.


<img src="https://github.com/HTWDMAR/RBFsim/blob/main/Manual/RBFsim.png" width="300" height="200">

The current code can simulate:

1. Single and multiple (<6) wells
2. Calculate river water portion in the filterate
3. Calculate river capture length
4. Compute travel time for river water to the well
5. Include impact of riverbed clogging
6. Visualization (isolines streamlines etc) for the above scenario.


## How to use the code:

The code currently can be used both as offline (preferred) and online mode (in development). Following steps need to be followed for running the code in **offline** mode. The interface of the code is based on Python [**streamlit**](https://streamlit.io/) library. The interface of RBFsim (online/0ffline)is:

<img src="https://github.com/HTWDMAR/RBFsim/blob/main/Manual/RBFsim%20Interface.png" width="300" height="200">


## Steps for using code 

1. Make sure that you have Python installed in your system and the Python libraries provided in the [requirements.txt](https://github.com/HTWDMAR/RBFsim/blob/main/requirements.txt). The 
2. Download the code as a zip file and extract it to any folder.
3. From the folder, run the code using [VScode](https://code.visualstudio.com/) or any such IDE or also command-prompt that can run Python.
4. 
5. To conduct **Meta Analysis** you need to make sure the _csv_ file (of literature obtained from e.g., web of science) in which the data about all the research articles is in the similar format as mentioned in the   code and name of all.
6. **Sensitivity Analysis** of each Parameter in a given equation can be checked, codes such as Local Sensitivity and FAST Sensitivity can be used. In either of them the Equation and the range around which the variables required to calibrate has to be given in as Input. 
7. To carry out the **Functional Analysis**, codes provided requires the _function_ (to be analyzed) as input at the start and the code runs a varitey of  Monte Carlo simulations based on the initial conditions and based on the simulations a common regression line is produced with the main goal to generalize the equation. 



The codes in this site are CC BY 4.0 licensed. The license wording can be found [here](https://creativecommons.org/licenses/by/4.0/).
Basically, for using code from here- the original authors should be credited.



Following authors are credited for this version [![DOI](https://zenodo.org/badge/576730534.svg)](https://zenodo.org/badge/latestdoi/576730534) of the code (names not in any order):

1. **P. K. Yadav** - for conceptualization and basic code development
2. **M. Tufail** - Main code development for online implementation
3. **V. Cantarella** - Offline code and verification
4. **A. Villa** - offline code and case studies
5. **M Gomez** - offline code and case studies
6. Tassilo Reuschling - First offline code development
7. Prof. Dr. T. Grischek - Supervisory support on contents

## References

- Coming up

![image](https://user-images.githubusercontent.com/86523952/207420810-a3777257-5a7e-4de2-8c29-e5f64a760304.png)

DE 47 8207 0024 0624 7951 00
