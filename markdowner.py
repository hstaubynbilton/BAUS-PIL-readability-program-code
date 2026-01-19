import pymupdf4llm, pathlib
# was 1.24.13, trying 1.26.7
import pymupdf

def file_list_creator(path1):
    """
    Creates a list of pdf files from a path area
    path1 in the form such as 'PDF/2015' okay"""
    output_files=[]
    p = pathlib.Path(path1)
    files1 = (p.glob('*.pdf'))
    for file in files1:
        output_files = output_files + [file]
    return output_files

def find_year(doc):
    """finds year from a pdf document opened using pymuPDF"""
    meta = doc.metadata['creationDate']
    return meta[2:6]

path ='PDF/inbox'
a = file_list_creator(path)

files1 = file_list_creator(path)

def main_fn(files=files1):
    for file in files:
        doc1 = pymupdf.open(file)
        meta = doc1.metadata['creationDate']
        year = meta[2:6]
        md_text = pymupdf4llm.to_markdown(file)
        name1 = file.name[:-4]
        title = "PDF/outbox/" + str(name1) + str(year) +'.md'
        pathlib.Path(title).write_bytes(md_text.encode())
        print('(done)')


main_fn()
print('done)')