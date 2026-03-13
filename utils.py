import pandas as pd
import re
import json

#remove extra white spaces 
def remove_extra_spaces(text):
    if not isinstance(text, str) or text.strip() == "":
        return text
    
    return re.sub(r'\s+', ' ', text).strip()

#title grammar. Capitalize every words except minor words like 'a', 'the', 'in'
def title_grammar(text):
    if not isinstance(text, str) or text.strip() == "":
        return text

    text = text.lower()
    
    minor_words = {
        'a', 'an', 'the', 'and', 'but', 'or', 'for', 'nor', 'on', 
        'at', 'to', 'from', 'by', 'with', 'in', 'of', 'as'
    }

    parts = re.split(r'(\s+|-)', text)
    parts = [p for p in parts if p]

    word_indices = [i for i, p in enumerate(parts) if not re.match(r'\s+|-', p)]
    
    if not word_indices:
        return text

    result = []
    for i, part in enumerate(parts):
        if re.match(r'\s+|-', part):
            result.append(part)
            continue
            
        if i == word_indices[0] or i == word_indices[-1] or part not in minor_words:
            result.append(part.capitalize())
        else:
            result.append(part)

    return "".join(result)

def infer_schema(df):
    schema = {}
    # We look at the first 5 rows to ensure we aren't tricked by a single NaN
    sample = df.head(5)
    
    for col in df.columns:
        dtype = str(df[col].dtype)
        
        if 'int' in dtype:
            schema[col] = 'int'
        elif 'float' in dtype:
            schema[col] = 'float'
        elif 'datetime' in dtype or 'date' in col: # Heuristic for dates
            schema[col] = 'datetime'
        else:
            schema[col] = 'str'
            
    return schema


def validate_and_purge(df, schema):
    for col, dtype in schema.items():
        if col not in df.columns:
            continue
            
        initial_count = len(df)
        
        if dtype == 'int':
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df = df.dropna(subset=[col])
            df[col] = df[col].astype(int)
            
        elif dtype == 'float':
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df = df.dropna(subset=[col])
            df[col] = df[col].astype(float)
            
        elif dtype == 'datetime':
            df[col] = pd.to_datetime(df[col], errors='coerce')
            df = df.dropna(subset=[col])
            
        elif dtype == 'str':
            df[col] = df[col].astype(str).replace(['nan', 'None', 'NULL'], '')
            
        dropped = initial_count - len(df)
        if dropped > 0:
            print(f"[{col}]: Dropped {dropped} rows due to type mismatch.")
            
    return df

def save_schema_json(df, filename='schema.json'):
    schema_export = {col: str(dtype) for col, dtype in df.dtypes.items()}
    with open(filename, 'w') as f:
        json.dump(schema_export, f, indent=4)
    print(f"Schema exported to {filename}")