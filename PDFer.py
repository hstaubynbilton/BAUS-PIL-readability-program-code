import select
from dataclasses import replace
from operator import truth, index

import setuptools
from pypdf import PdfReader
import textstat
import readability
from readability import Readability
import re
import pathlib, pymupdf
import pymupdf4llm, pandas, numpy, matplotlib

def import_pdf3(file1): # the old version using a rectangle which did not really work...
    """imports the document into pymupdf and takes a crop removing header and footer,
    then combines each page into one document"""

    doc = pymupdf.open(file1)
    output = ''
    for page in doc:  # iterate the document pages
        rect = pymupdf.Rect(50, 0, 750, page.rect.width)  # define rectangle to remove header/footer
        text = page.get_textbox(rect)  # get text from rectangle

        # text = page.get_text(sort=True) #the old method that sorted text
        output = output + text
    return output

def import_pdf2(file1):
    doc = pymupdf.open(file1)
    output = ''
    for page in doc:  # iterate the document pages
        text = page.get_text(sort=False) #the old method that sorted text
        output = output + text
    return output


remove_list = (
        r'https?:\S*',
        r'www\.\S*',
        r'Published: \w\S* \S*',
        r'Review due: \w\S* \S*',
        r'Leaflet No: \w\S*',
        r'Leaflet No: \w\S*',
        r'Between .* patients',
        r'To view this leaflet online, scan the QR code (right) or type the short URL below it into your web browser.',
        r'  ', #2 spaces
        u'\xa0',
        u'\t',
        u'\r',
        u'\xad',
        u'Signature............................................................... ',
        u'Date...........................................',
        )

def smart_remove_char(text, remove_list=remove_list):
    for item in remove_list:
        text = re.sub(item, ' ', text)
    return text


def break_sentences(text):
    """ Not implemented"""
    sen_list = []
    expression1 = '' #expression to identify each sentence.
    def iterate1(text):
        a = re.findall(expression1, text)


def move_to_new_sentence(text): #not implemented
    criteria = r'.*\(.*\).*\.' #identifies sentences with a () in them
    list1 = re.findall(criteria, text)
    returned_ans = ''
    for item in list1:
        bracketed_list = re.findall(r"(.*)", item) #puts bracketed text into list
        unbracketed = re.sub(r"(.*)", '', item)  #removes bracketed text from sentence
        ans = unbracketed
        for bracketed_text in bracketed_list:
            bracketed_text = bracketed_text.strip() # removes end white space
            bracketed_text = bracketed_text.replace('(','') #removes bracket
            bracketed_text = bracketed_text.replace(')','') # removes bracket
            ans += '.  ' + str(bracketed_text)
        returned_ans += ans

    return ans

def replace_char(text):
    """
    For more complex replacements
    """
    def list_replacer(match_obj):
        ab = (match_obj.group())
        if match_obj.group() is not None:
            return str(match_obj.group()) + '.'
    identifier = r'Between .*(\n)?.*patients'
    text = re.sub(identifier, list_replacer, text)

    def add_periods(match_obj):
        ''' a function to add periods only when appropriate and missing'''
        ab = (match_obj.group())
        groups_ = match_obj.groups()
        if match_obj.group() is not None:
            # return '.' + str(match_obj.group())
            ans =  str(groups_[0]) + str(groups_[1]) + str('.') + str(groups_[2]) + str(groups_[3]) + str(groups_[4])
            return ans
    identifier = r'(\n)([A-Z])'
    #identifier2 = r'([a-z]|\))(\s*)(\n)([A-Z])(\w|" "|)'
    identifier2= r'(\w|\))(\s*)(\n)([A-Z])(\w|" "|)'
    text = re.sub(identifier2, add_periods, text)

    text = text.replace('.e.g.', 'eg')
    text = text.replace('e.g.', 'eg')
    text = text.replace( u'•', '.')
    text = text.replace(r'\+\d\d.*', ' ')
    text = text.replace(r'admin@baus.org.uk', ' ')
    text = text.replace(r"(© British Association of Urological Surgeons Limited)(\s*)(\d)", " ")
    text = text.replace(r"© British Association of Urological Surgeons Limited", " ")
    #
    return text



print('End of PDFER')
