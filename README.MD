## Basic Info

The Executable file is in the Output Folder, This is the only file you need to run the Multi Stager


The Baudrate is 115200  
The File transfer protocol is Xmodem1k  

Green  - Pass   
Red  - Fail  

## Things of Note

when connecting to a unit, it will only return green if it can read the units menu  
a unit may be working but throwing out a voltage error as the power supply is not providing enough power, so will return red 

the progress bar only really works for pushing Firmware, compares the file size with how much data has been sent. 
once progress hits 95% it will stop as the unit will lock up for 10-20 seconds to install the firmware, and then will push personailty and then do final checks, so the last 5% is not linear

getting the unit info, viewing stautus screen and config, is not live updating like on terra term, it takes a snapshot on button press, so keep pressing the button untill all fields are populated

## 
