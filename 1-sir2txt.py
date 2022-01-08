import textract
import glob
import os
import multiprocessing



# This script converts PDF to text

####################################
# get path to directory and set up file list
###################################
dirpath = input("Please input path to data directory: ")
print("You entered: " + dirpath)

os.chdir(dirpath)

files = glob.glob('data/pdf_in/*/*.pdf') # get list of PDF files within site folders


###################################
# define text extraction function
###################################
def extract_txt(file_path):

    outpath = file_path.replace('pdf_in/','txt_out/').replace('.pdf','.txt') # change dir to output dir, and .pdf to .txt

    # only run text extraction if output .txt file doesn't already exist
    if os.path.isfile(outpath):
        print('File already exists: ' + outpath)
    else:
        print('converting file:', file_path)
        os.makedirs(os.path.dirname(outpath), exist_ok=True) # make directory for output file

        text = textract.process(file_path, method='tesseract') # extract text and write
        with open(outpath, 'wb') as output_file:
            output_file.write(text)
        return file_path

###### run function using multiprocessing
p = multiprocessing.Pool()
for fn in p.imap_unordered(extract_txt, files):
    print('completed file:', fn)
