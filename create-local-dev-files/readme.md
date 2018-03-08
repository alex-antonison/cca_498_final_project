## How to use this script

* This python script was built using Python 3
* You need to have the zip file located cca_498_final_project/raw_data/raw/pythonquestions.zip
* To use this script, you need to have the following libraries installed:
  * pandas
* You must execute this folder from within the directory it exists 
* When running the script, you need to pass the following arguments:
  * 1 - Amount of questions
  * 2 - The Random seed
  * 3 - The directory under cca_498_final_project/raw_data/ that you want it dumped
  * 4 - True or False as to whether you want to unzip the files or not
  
### An example run script is the following:
python python create-local-dev-files.py 10000 50 local-dev True

* This will create a sample set of 
  * 10,000 questions
  * Random seed 50
  * Go to the cca_498_final_project/raw_data/local-dev/ directory
  * It will unzip the raw file
  
I included my jupyter notebook that I used to troubleshoot development.