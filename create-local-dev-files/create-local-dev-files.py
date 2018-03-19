import os
import zipfile
import pandas as pd
import sys

random_sample_amount = sys.argv[1]
random_sample_seed = sys.argv[2]
file_storage_location = sys.argv[3]
unzip_files = sys.argv[4]

print("==>These are the arguments you selected")

print("Random Sample:", random_sample_amount)
print("Random Seed:", random_sample_seed)
print("File Location:", file_storage_location)
print("Unzip Files:", unzip_files)

# Since we do not want to source control the raw data in git
# To run this script, you will need to create a raw directory under the raw_data
# and place a the zip file there

# Here I am figuring out the relative path of the directory you are working here
dir_path = os.path.dirname(os.path.realpath(__file__))

# Going back a directory and going into the expected raw directory with the zip file
os.chdir("../raw_data/")
raw_dir_path = os.getcwd()

# Creating the zip file path
raw_zip_path = raw_dir_path + '/raw/pythonquestions.zip'
raw_zip_result = raw_dir_path + '/raw'

# This will unzip the files in the raw_dir_path location
# If you already have the files unzipped, you can comment this out to save processing time

if unzip_files == "True":
    print("==> Unzipping files.")
    zip_ref = zipfile.ZipFile(raw_zip_path, 'r')
    zip_ref.extractall(raw_zip_result)
    zip_ref.close()

print("==> Producing files...")

# Setting up my path to the different files
raw_answers_path = os.path.join(raw_dir_path, 'raw/Answers.csv')
raw_questions_path = os.path.join(raw_dir_path, 'raw/Questions.csv')
raw_tags_path = os.path.join(raw_dir_path, 'raw/Tags.csv')

answers_df = pd.read_csv(raw_answers_path, encoding='latin1')
questions_df = pd.read_csv(raw_questions_path, encoding='latin1')
tags_df = pd.read_csv(raw_tags_path, encoding='latin1')

# Here I am random sampling the questions
sampled_questions_df = questions_df.sample(n=int(random_sample_amount), random_state=int(random_sample_seed))

# Here I am merging the answers onto the questions to limit
# the answers to just the randomly selected questions
sampled_answers_df_stg = pd.merge(sampled_questions_df, answers_df, left_on='Id', right_on='ParentId', how='inner')

# Since the merge takes in all columns, I am limiting it to just the answers ones
sampled_answers_df = sampled_answers_df_stg.iloc[:, 6:12]
sampled_answers_df_r = sampled_answers_df.rename(columns={"Id_y": "Id", "OwnerUserId_y": "OwnerUserId",
                                                          "CreationDate_y": "CreationDate", "ParentId": "ParentId",
                                                          "Score_y": "Score", "Body_y": "Body"})

# Here I am reducing down the tags to just the sampled questions
sample_tags_df_stg = pd.merge(tags_df, sampled_questions_df, left_on='Id', right_on='Id', how='inner')

# Same as answers, pulling out just the tags columns
sample_tags_df_with_python_tag = sample_tags_df_stg.iloc[:, 0:2]

# Save the down sampled files to the desired location
sampled_path = raw_dir_path + '/' + file_storage_location + '/'

# Removing the python tags
# By using the ~, it does the reverse of the filter
# I am using match since I ONLY want the tags removed that are simply python, and not
# just having python within the tag
# Got an error so having to use the astype(str) to cast everything as a string.
sample_tags_df = sample_tags_df_with_python_tag[~sample_tags_df_with_python_tag['Tag'].astype(str).str.match('python')]

if os.path.isdir(sampled_path) is False:
    os.mkdir(sampled_path)

question_sample_path = sampled_path + 'Questions.csv'
answers_sample_path = sampled_path + 'Answers.csv'
tags_sample_path = sampled_path + 'Tags.csv'

sampled_questions_df.to_csv(question_sample_path, index=False)
sampled_answers_df_r.to_csv(answers_sample_path, index=False)
sample_tags_df.to_csv(tags_sample_path, index=False)


print("==> Completed, files can be found here: ", sampled_path)
