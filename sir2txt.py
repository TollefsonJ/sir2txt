import textract
import glob
import os
import multiprocessing

# This script converts PDF to text

files = glob.glob('pdf_in/*/*.pdf') # get list of PDF files within site folders

def extract_txt(file_path):
    text = textract.process(file_path, method='tesseract')
    outpath = file_path[:-4] + '.txt'  # assuming filenames end with '.pdf'
    outpath = outpath.replace('pdf_in/','txt_out/')
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    with open(outpath, 'wb') as output_file:
        output_file.write(text)
    return file_path

p = multiprocessing.Pool()
for fn in p.imap_unordered(extract_txt, files):
    print('completed file:', fn)
