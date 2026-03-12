import pandas as pd
from utils import remove_extra_spaces, title_grammar

raw = pd.read_csv('dataset/RAW_recipes.csv', encoding='latin1')
df1 = raw.copy()


# standarize format
df1['name'] = df1['name'].apply(remove_extra_spaces)
df1['description'] = df1['description'].apply(remove_extra_spaces)
df1['name'] = df1['name'].apply(title_grammar)

# remove duplicates
name_dupes = df1.duplicated(subset=['name']).sum()
id_dupes = df1.duplicated(subset=['id']).sum()

print(f"Duplicates found in 'name': {name_dupes}")
print(f"Duplicates found in 'id': {id_dupes}")

if name_dupes == 0 and id_dupes == 0:
    print("No duplicates found")
elif name_dupes > 0:
    print(f"Processing {name_dupes} name duplicates...")
    
    contributor_counts = df1['contributor_id'].value_counts()
    df1['user_total_contributions'] = df1['contributor_id'].map(contributor_counts)
    df1['submitted'] = pd.to_datetime(df1['submitted'])
    
    df1['n_ingredients'] = df1['ingredients'].str.count(',') + 1
    df1['n_steps'] = df1['steps'].str.count(',') + 1

    df1 = df1.sort_values(
        by=[
            'name', 
            'user_total_contributions', # 1. submitted by more active contributor
            'submitted',                # 2. More recent
            'n_ingredients',            # 3. Less ingredients
            'n_steps',                  # 4. Less steps
            'minutes',                  # 5. Less minutes
            'id'                        # 6. Smaller ID
        ],
        ascending=[True, False, False, True, True, True, True]
    )

    before_count = len(df1)
    df1 = df1.drop_duplicates(subset=['name'], keep='first')
    after_count = len(df1)

    df1 = df1.drop(columns=['user_total_contributions', 'n_ingredients', 'n_steps'])
    
    print(f"Dropped {before_count - after_count} duplicate recipes.")

# handle missing data

before_drop = len(df1)

df1 = df1.dropna(subset=['steps', 'ingredients'], how='any')

after_drop = len(df1)
print(f"Removed {before_drop - after_drop} recipes missing steps or ingredients.")


# fix structural errors
## n_ingredients and n_steps are not being read
df1 = df1.loc[:, ~df1.columns.str.contains('^Unnamed')]
df1 = df1.drop(columns=['n_steps', 'n_ingredients'], errors='ignore')

df1['step_count'] = df1['steps'].str.count(',') + 1
df1['ingredient_count'] = df1['ingredients'].str.count(',') + 1

df1['step_count'] = df1['step_count'].fillna(0).astype(int)
df1['ingredient_count'] = df1['ingredient_count'].fillna(0).astype(int)

print("Ghost columns dropped and counts recalculated.")
print(df1[['name', 'step_count', 'ingredient_count']].head())



# handle outliers 
# validate data
# print(raw.head())
print(df1.head())
df1.to_csv('dataset/df1/cleaned_recipes.csv', index=False)


