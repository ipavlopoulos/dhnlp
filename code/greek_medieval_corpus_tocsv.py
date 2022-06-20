# convert .doc to .docx (linux environment assumed) with the following command: >> lowriter --convert-to docx *.doc

# !pip install docx
from docx import Document
import os

def docx2txt(path, sep="<NEWPARAGRAPH>"):
    """ Extract the text from a file stored as docx. 
    param: path: the path of the file to be parsed
    param: sep: the separator of the paragraphs, when these will be merged into a single text
    return: the text of the file at the given path 
    """
    document = Document(path)
    paragraphs = [p.text.replace("\n", "<NEWLINE>") for p in document.paragraphs]
    return sep.join(paragraphs)

def docx2txt_batch(path, extention=".docx", verbose=0):
    """ Extract the text from each file in a path
    param: path: the path of the directory that comprises the files in question
    param: genre: the extention of each file
    param: verbose: whether to work silently (0) or print any warnings
    return: a list of texts, parsed from the files stored in that path
    """
    files, filenames = [], []
    for i, filename in enumerate(os.listdir(path)):
        if not filename.endswith(extention):
            if verbose:
                print(f"Ignoring file with name: {filename}")
            continue
        fname = f"{path}/{filename}"
        files.append(docx2txt(fname))
        filenames.append(fname)
    return files, filenames


parsed_files = {}
parsed_names = {}
for genre in os.listdir("Greek_Medieval_Corpus"):
    # for each subdirectory
    # ignore existing hidden files
    if genre.startswith("."): continue
    # some directories contain files, other contain subdirectories, read them all using only for / if
    items_in_dir = os.listdir(f"Greek_Medieval_Corpus/{genre}")
    if len(items_in_dir) > 5: # files in the dir
        docs, names = docx2txt_batch(path=f"Greek_Medieval_Corpus/{genre}")
        parsed_files[genre] = docs
        parsed_names[genre] = names
    else: # directories (with files) in the dir
        for subdir in items_in_dir:
            if subdir == ".DS_Store": 
                continue
            docs, names = docx2txt_batch(path=f"Greek_Medieval_Corpus/{genre}/{subdir}")
            parsed_files[f"{genre}/{subdir}"] = docs
            parsed_names[f"{genre}/{subdir}"] = names
            

import pandas as pd
long_format = []
for genre in parsed_files:
    docs = parsed_files[genre]
    names = parsed_names[genre]
    long_format.extend(list(zip(names, docs, [genre]* len(docs))))
    
data_pd = pd.DataFrame(long_format)
data_pd.columns = ["filename", "text", "genre"]
data_pd.sample(2)
