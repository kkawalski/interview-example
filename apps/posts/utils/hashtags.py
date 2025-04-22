import re


def extract_hashtags(text):
    return list(set(
        tag.lower() 
        for tag in re.findall(r'#(\w+)', text)
    ))
