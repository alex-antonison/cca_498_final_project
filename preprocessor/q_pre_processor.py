import pandas as pd
import os


def remove_lines(text):
    try:
        return text.rstrip(os.linesep).replace('\n', ' ')
    except:
        print(text)


# Before Executing this please open and save the file in Sublime Text to enforce UTF-8 encoding
data = pd.read_csv('raw_data/full/Questions.csv')
data = data.fillna(0)

data['Title'] = data['Title'].apply(remove_lines)
data['Body'] = data['Body'].apply(remove_lines)

data.to_csv('raw_data/full/Questions_New.csv', encoding='utf-8', index=False)
