import pandas as pd
from utils import remove_extra_spaces, title_grammar

raw = pd.read_csv('dataset/RAW_recipes.csv', encoding='latin1')
df1 = raw.copy()


# remove duplicates
# handle missing data
# standarize format
df1['name'] = df1['name'].apply(remove_extra_spaces)
df1['description'] = df1['description'].apply(remove_extra_spaces)
df1['name'] = df1['name'].apply(title_grammar)
# fix structural errors
# handle outliers 
# validate data
print(df1.head())


