import re

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