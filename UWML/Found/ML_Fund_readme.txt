ML: Foundations
---------------
warning: DO NOT Install separately Python or Anaconda package (includes Python 2.7 and iPython Notepad)

Tools
=====
RAM-based libraries:
- Pandas is a Data Manipulation librar
- SciKit-learn is a Machine Learning method library
The problem with them is that they require to load all the data in RAM, so they won't scale to real projects

Disk-based Libraries:
- SFrame is a scalable library for data manipulation
- GraphLab Create is a scalable ML method library (includes SFrame)

Install GraphLab Create from Dato, here https://dato.com/download/academic.html
Registered email address: mr.sarno2@gmail.com
Product key: 5E63-0553-777B-EB3A-CB40-3971-19CC-36DC
The Graphlab launcher installs Anaconda
Dowload additional 'kernels', means other versions of Python.

Launch the iPython Notebook
Download the course notebook files
To open a notebook file:
- click 'upload' and browse the file system and select your file from the git tree. 
  This will just copy to the iPython 'home folder', 
  which is  (where you are calling iPython notebook from) in the local host.
- once uploaded, look for the file in the list and click on it

It works like the screen of a debugger, combined with an old line-based text editor!
To open a data file in the same folder, you  need to 'upload' the data file too.
To read a Graphlab dataset, (is a folder with a few text files) you can't 'upload it'
so make sure you manualy copy it under the  (where you are calling iPython notebook from) 
In my case I called from my user folder, so I can use for example Downloads:
sales = graphlab.SFrame('Downloads/home_data.gl/') 

The IPython Notepad is launched inside the browser in a localhost site that is not available anymore after you close the Dato process,
So, the Dato launcher must be starting a local web service.
The brand in the page is Jupyter.
[INFO] Start server at: ipc:///tmp/graphlab_server-4972 - Server binary: C:\Users\hp\AppData\Local\Dato\Dato Launcher\lib\site-packages\graphlab\unity_server.exe - Server log: C:\Users\hp\AppData\Local\Temp\graphlab_server_1444195269.log.0
[INFO] GraphLab Server Version: 1.6.1

-----------------------------------------------------------------------------------------------
Concepts
========

Precission and Accuracy are common measures to evaluate predictions methods in science. 
- Accuracy is about the 'mean' of the detection method being equal to the mean of the population.
- Precission is about the 'standard deviation' or 'error range' of the detection method.

in Classification:
Accuracy: 'reliability of + and - predictions' : (true positives + true negatives)/(all data)
 - proportion of times the outcome is right
   (compared to the total number of input processed)
Accuracy is not enough because if there is a majority class that happens in 90% of the 
data examples, a method that simply chosses always that class will be 90% precise.

Precission: 'reliability of +' : true positives/(true positives + false positives)
 - proportion of times the method is right when it produces a + output
   (compared to the total number of + outputs)

 - an imprecise method calls positive anything in the vecinity of true positives, 
   the detection filter is too wide, the filtering is 'imprecise' 
   (and, as such, a claim of positive by this method is 'unreliable')

Recall:     'sensitivity' : true positives/(true positives + false negatives)
 - proportion of times the method is right when it processes a + input
   (as a proportion of the total number of times it is fed an + input)

 - if you want to detect every single positive, the method may become imprecise.
 - if you reduce the margin of error too much, you stert missing some true +, 
   the method becomes insensitive

Assignments
-----------
