# tek17
Software package for capstone team 17 project.

Here is a set up guide for running the software package.
This is followed by a guide to set up the remote desktop.

--preliminary:

download the tek17 zip file and extract all to a folder of your choosing.


**** install RSA API ****   <===== link is on discord CS channel
**** make sure the API is downloaded to C:/Tektronix/.... I don't remember

--step 1: download python through anaconda

link:
https://docs.anaconda.com/anaconda/install/windows/

follow instructions.

click the link on step one. click the download button. choose 64-Bit Graphical Installer for Windows.

skip step 2.

choose the recommended option on step 8.

skip step 12.

close all windows that pop up after finishing.

--step 2: download pycharm

link:
https://www.jetbrains.com/pycharm/download/#section=windows

click download under the community label.

click the downloaded executable.

click through all the recommended steps.

--step 3: conda installs

search anaconda prompt on your taskbar searchbar.

click anaconda prompt.

type in these lines of code.

conda create -n my-env
conda activate my-env
conda config --env --add channels conda-forge
conda install numpy

*type y when prompted

conda install matplotlib

*type y when prompted

--step 4: open pycharm

find the folder that you extracted the tek17 code to.

right click inside the folder in white space and choose "open folder as pycharm project"

Alternative: open pycharm. open -> tek17 folder -> ok.

when pycharm prompts you to use python version from anaconda3\python.exe choose ok.

--step 5: add configurations

click add configurations at the top right of pycharm, next to the play button.

hit the plus button.

on the left hand side choose python.

on the right hand side in the script path bar, click the folder icon.

set the script path to the file path that leads to tek17 open tek17 folder and click main.py.

press apply and ok.

click terminal on the bottom of pycharm.

--step 6: pip installs

type two commands:

pip install opencv-python3

pip install arduino-python3

pip install pyqt5

--step 7: run package

click the green arrow at the top of pycharm to run the package.






-remote computer set up

go to https://remotedesktop.google.com/access/

click the download arrow on the bottom right hand corner of the "set up remote access prompt"

follow the download instructions

it should say your computer is online

go to remote support tab

under share this screen click generate code

send code to the laptop that wants remote access

-remote access set up

go to the remote support tab

put the access code that was generated on the other computer into the "connect to another computer" prompt