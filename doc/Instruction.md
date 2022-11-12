# Install MNE Python and get familar with Spyder

1. Download and install **MNE-Python** installers from [here](https://mne.tools/stable/install/installers.html#installers).

    - Choose the installers based on your operating system (Windows,MacOS or Linux).
    - Use the default option during the installation.
    - The installer adds menu entries on Linux and Windows, and several application bundles to the Applications folder on macOS.

2. Open **Spyder** from the menu/application. 

    - You can use Spyder to write your own python analysis scripts or open demo python scripts.
    - The python scripts (*.py file) can be opened form File menu-> Open.
    - Run the entire script/file by clicking the ![](button1.png) button the Toolbar (or press F5 key).
    - Run selection or current line by clicking the  ![](button2.png)  button in the Toolbar (or press F5 key).
    - You can learn more about the basics of Spyder from the Youtube video [here.](https://www.youtube.com/watch?v=WV9bm4ey7Cg&list=PLPonohdiDqg9epClEcXoAPUiK0pN5eRoc&index=2)

# Analyze oddball and imagmove EEG data in MNE Python
* Download the whole repository as a [zip file](https://github.com/weiyongxu/CIBA120-2022-Analyzing-EEG/archive/refs/heads/master.zip) and unzip it on your own computer.
* The scripts are located in **CIBA120-2022-Analyzing-EEG-master\script** folder.

## Task 1: Practice the EEG preprocessing step using the oddball data from two participants:
* Open the script: **Practise-processing-oddball.py** in Spyder.
* Follow the detailed instruction in the comments (lines starting with `#`) of the scripts.
* It is possible to run the entire script or run each line at a time.

## Task 2: Run the group analysis script for Oddball task
* Open the script: **oddball-group_analysis.py** in Spyder 
* Change the **processed_data_folder**  in the code to the place where you put the processed_data_folder (downloaded from Moodle) in your own computer.
* Run the script and try to resovle possible errors.
* Check the output in the ipython terminal and the figure plotted.
* Compare your own results with the demo results in  **[oddball-group_analysis.ipynb](https://github.com/weiyongxu/CIBA120-2022-Analyzing-EEG/blob/master/script/oddball-group-analysis.ipynb)** (can be opened on the Github webpage) or **oddball-group_analysis.html** (need to download and open locally).
## Task 3: Run the group analysis script for ImagMove task
* Same steps as in Task 2 but run the script: **ImagMove-group_analysis.py** and compare with corresponding demo results.
