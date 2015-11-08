Practical Predictive Analitycs, Models and Methods
--------------------------------------------------
UW - Bill Howe
-----------

 
R Installation for Assignment5
------------------------------
1. Add a default download URL (source of the packages) aka repository
gedit ~/Rprofile:
local({r <- getOption("repos");         r["CRAN"] <- "http://cran.r-project.org"; options(repos=r)})

2. Add a dependency of ggplot2 package that should not come from CRAN, but directly from ubntu:
sudo apt-get install r-cran-plyr
sudo apt-get install r-cran-reshape2

3. Upgrading R / Installing R-3.2.0 on Ubuntu
codename=$(lsb_release -c -s)  
echo "deb http://ftp.iitm.ac.in/cran/bin/linux/ubuntu $codename/" | sudo tee -a /etc/apt/sources.list > /dev/null  
#Note that instead of http://ftp.iitm.ac.in/cran one must replace it with the geographically closest CRAN mirror. Also, the Ubuntu #archives on CRAN are signed with the key of Michael Rutter <marutter@gmail> with key ID E084DAB9. So we type in the following:
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E084DAB9  
sudo add-apt-repository ppa:marutter/rdev
# Followed by what we would normally have done:
sudo apt-get update  
sudo apt-get upgrade  
sudo apt-get install r-base r-base-dev  



3. Run the setup.r script in the R shell with root permissions:
Install the Caret package (massive: caret: Classification and Regression Training)
sudo Rscript setup.r 

Get the rpart library:
sudo apt-get build-dep r-cran-rpart
sudo apt-get install r-cran-rpart


4. But first install the python dev libs because the Caret depends on rPython that depends on python-dev:
sudo apt-get install python-dev

Run R interactively and install the RandomForest package:
sudo R
install.packages("randomForest")

install.packages('rPython', repos='http://cran.rstudio.com')






-----------------------------------------------------------------------------------------
