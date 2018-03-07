import os
import zipfile
import pandas as pd

# Since we do not want to source control the raw data in git
# To run this script, you will need to create a raw directory under the raw_data
# and place a the zip file there

# Here I am figuring out the relative path of the directory you are working here
dir_path = os.path.dirname(os.path.realpath(__file__))

# Going back a directory and going into the expected raw directory with the zip file
os.chdir("../raw_data/raw/")
raw_dir_path = os.getcwd()

# Creating the zip file path
raw_zip_path = os.path.join(raw_dir_path, 'pythonquestions.zip')

# This will unzip the files in the raw_dir_path location
# zip_ref = zipfile.ZipFile(raw_zip_path, 'r')
# zip_ref.extractall(raw_dir_path)
# zip_ref.close()

# Setting up my path to the different files
raw_answers_path = os.path.join(raw_dir_path, 'Answers.csv')
raw_questions_path = os.path.join(raw_dir_path, 'Question.csv')
raw_tags_path = os.path.join(raw_dir_path, 'Tags.csv')


answers_df = pd.read_csv(raw_answers_path, encoding='latin1')

answers_df.head()


