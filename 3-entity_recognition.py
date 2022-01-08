import os
import argparse
import glob
import spacy
from spacy.tokens import DocBin

################################################
################################################
# set up text directory
################################################
directory = input("Enter path to this folder: ")
print("You entered: " + directory)
os.chdir(directory)


# import texts to list
files = glob.glob('data/txt_clean/*/*.txt') # get list of txt files within site folders

textlist = []
for file in files:
    text = " ".join(open(file,'r').readlines())
    textlist.append(text)

################################################
################################################
# run NLP on texts and add to document bin
################################################
nlp = spacy.load("en_core_web_trf") # trf has better accuracy metrics than en_core_web_lg or en_core_web_sm

# set up pipelines to run NLP on texts
doc_bin = DocBin(attrs=["LEMMA", "ENT_IOB", "ENT_TYPE"], store_user_data=True)

# run NLP on all texts
for doc in nlp.pipe(textlist):
    doc_bin.add(doc)

# save NER results as spacy object
outfile = directory + "/data/analysis_output/nlp_output.spacy"
doc_bin.to_disk(outfile)

# send to list and view some results
doclist = list(doc_bin.get_docs(nlp.vocab)) # docbin to doclist

spacy.displacy.serve(doclist[0], style='ent') # view first result

################################################
################################################
# ents to dataframe: save ents and labels for each doc to a separate dataframe, to easily examine
################################################
import pandas as pd

ents_df=[]
for doc in doclist:
    texts = []
    labels = []

    for ent in doc.ents:
        texts.append(ent.text)
        labels.append(ent.label_)

    df = pd.DataFrame(list(zip(texts,labels)),columns=['text','label'])
    ents_df.append(df)

################
# save dataframes of entities and labels to csv files
for i, df in enumerate(ents_df):
    #df = df[~df.label.isin(['CARDINAL','ORDINAL','DATE','TIME','QUANTITY'])] # don't export numbers, dates, etc
    outpath = files[i].replace('_CLEAN.txt','_ENTITIES.csv').replace('txt_clean','analysis_output/entities_df')
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    df.to_csv(outpath, index=False)
