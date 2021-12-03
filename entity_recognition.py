import os
import argparse
import glob
import spacy
from spacy.tokens import DocBin


# set up text directory
directory = input("Enter path to this folder: ")
print("You entered: " + directory)
os.chdir(directory)


# import texts to list
files = glob.glob('txt_out/*/*.txt') # get list of txt files within site folders

textlist = []
for file in files:
    print(file)
    text = " ".join(open(file,'r').readlines())
    textlist.append(text)



#######################
# run NLP on texts and add to document bin
#######################
nlp = spacy.load("en_core_web_lg")

# set up pipelines to run NLP on texts
doc_bin = DocBin(attrs=["LEMMA", "ENT_IOB", "ENT_TYPE"], store_user_data=True)

# run NLP on all texts
for doc in nlp.pipe(textlist):
    doc_bin.add(doc)


# view some results
doclist = list(doc_bin.get_docs(nlp.vocab))
spacy.displacy.serve(doclist[0], style='ent')

for ent in doclist[0].ents:
    print(ent.text,  ent.label_)






################
# output results to disk
################

# doc bin to bytes
bytes_data = doc_bin.to_bytes()

# ask for output directory


# save output to disk
outfile = directory + "/analysis_output/nlp_output"
with open(outfile, "wb") as out_file:
    out_file.write(bytes_data)




# Deserialize later, e.g. in a new process
#file = open("path/to/bytes_file", 'rb')
#bytes_data = file.read()
#
#nlp = spacy.blank("en")
#doc_bin = DocBin().from_bytes(bytes_data)
#docs = list(doc_bin.get_docs(nlp.vocab))
