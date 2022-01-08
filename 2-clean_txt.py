import os
import argparse
import glob
import re


#################################################################
# grab files
#################################################################
# set up text directory
directory = input("Enter path to this folder: ")
print("You entered: " + directory)
os.chdir(directory)

files = glob.glob('data/txt_out/*/*.txt') # get list of txt files within site folders

# import texts to list
textlist = []
for file in files:
    text = " ".join(open(file,'r').readlines())
    textlist.append(text)


#################################################################
# clean text - apply minimal cleaning to remove line breaks and double spaces.
############ clean
textlist_clean = []
for t in textlist:
    t = t.replace('\n',' ')     # replace line breaks with spaces
    t = re.sub(' +', ' ', t)   # remove double spaces
    textlist_clean.append(t)     # add results to list

#################################################################
# save clean texts to txt files
#################################################################
for i, text_clean in enumerate(textlist_clean):
    ############################ save clean texts
    outpath = files[i].replace('txt_out/','txt_clean/')     # set up file path for clean text output
    outpath = outpath.replace('.txt','_CLEAN.txt')          # mark filename as "clean"


    if os.path.isfile(outpath):                             # skip if file already exists
        print('File already exists: ' + outpath)
    else:
        print('Writing: ' + outpath)
        os.makedirs(os.path.dirname(outpath), exist_ok=True)
        with open(outpath, 'w') as output_file:
            output_file.write(text_clean)
