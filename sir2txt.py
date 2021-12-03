import textract
import glob
import os
import multiprocessing



# This script converts PDF to text

dirpath = input("Please input path to data directory: ")
print("You entered: " + dirpath)

os.chdir(dirpath)

files = glob.glob('pdf_in/*/*.pdf') # get list of PDF files within site folders

def extract_txt(file_path):

    outpath = file_path[:-4] + '.txt'  # assuming filenames end with '.pdf'
    outpath = outpath.replace('pdf_in/','txt_out/')

    # only run text extraction if output .txt file doesn't already exist AND the file isn't a map or image file
    if os.path.isfile(outpath) or outpath.count("map")>0 or outpath.count("image")>0:
        pass
    else:
        print('converting file:', file_path)
        os.makedirs(os.path.dirname(outpath), exist_ok=True)

        text = textract.process(file_path, method='tesseract')
        with open(outpath, 'wb') as output_file:
            output_file.write(text)
        return file_path

p = multiprocessing.Pool()
for fn in p.imap_unordered(extract_txt, files):
    print('completed file:', fn)
