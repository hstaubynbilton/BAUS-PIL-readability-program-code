import re
#This imports the file and opens it
def import_text(file):
    with open(file) as file1:
        text = file1.read()
    return text


#This variable lists text strings specifically to be removeed
remove_list = (
        #markdown specific
        r'###+',
        r'\[.*?\]\(.*?\)',
        r'\(https?:.*?\)',
        r'##',
        r'#',
        r'\*\*\*+',
        r'\*\*',
        r'\*',
        r'\|\-\-\-\|-\-\-\|',
        r'( )( )+',  # 2+ spaces
        # BAUS PIL specific
        r'35-­‐‑43',
        r'(\|)(Col\d*)(\|)(.{0,9})(\|)',
        r'\[.*?\]',
        r'https?:\S*',
        r'(\()(baus.org.uk)(\/).*?(\))',
        r'www\.*?\S*',
        r'Published:( )*(\w)*(\s)*(\n)?(\s)*(\w)*(\n)?(\d)*\s*(\.)?',
        r'Review due:\s\w*\s*\w*\s*',
        r'\[',
        r'\]',
        r'Due for review:(\s)*(\w)*(\s)*(\w)*',
        r'Date for review:(\s)*(\w)*(\s)*(\w)*',
        r'\xa0',
        r'\t',
        r'\r',
        r'\xad',
        r'35-­‐‑43',
        r'Signature ?\.+',
        r'Date\.+',
        r'admin@baus.org.uk',
        r'\+\d\d.{0,10}?\d',
        r'(35-(\s*)(\n*)‐‑43(\s*)(\n*))?Lincoln(\s*)(\n*)’(\s*)(\n*)s(\s*)(\n*)Inn(\s*)(\n*)Fields(\s*)(\n*)(\.)?(\s*)(\n*)London(\s*)(\n*)(\.)?(\s*)(\n*)WC2A(\s*)(\n*)3PE',
        r' Phone: ',
        r' Fax: ',
        r' E\-*mail: ',
        r'E ?mail:',
        r' Website: ',
        r'( )( )+', #2+ spaces
        r'\.\.\.*',
        r'Page:? *\d',
        r'BAUS\n? ?\n?35[_-]43',
        r'\(0\)20  7869  6950',
        r'\(0\)20  7404  5048',
        r'\(0\)',
        r'\.pdf',
        r'™',
        r'®',
        r'No:\s*\w*\s*',
        r'Leaflet(\s*)(\n)?No:(\.)?(\n)?(\s)*(\n)?\w*(\n)?\/\d*(\n)?\s*(\n)?\|?\s*(\n)?(Page)?(\n)?\s*(\n)?\d*',
        r'Leaflet No:\s*\w*\s*',
        r'Page \d',
        )

def smart_remove_char(text, remove_list=remove_list):
    '''
    This function performs slightly more complex sanitization tasks
    '''
    # Changes double lines to a temporary symbol for later processing due to an artefact of processing
    text = re.sub(r'\n\n', '$$$', text)
    # Removes remaining single lines
    text = re.sub(r'\n', ' ', text)
    #Replaces pre-existing double lines into a single new line
    text = re.sub(r'\$\$\$', ' \n ', text)
    # replaces dashes with _ for easier processing
    text = re.sub(r'\- \-\-', '_', text)
    #removes copyright notices
    text = text.replace(r'© British Association of Urological Surgeons Limited', ' ')
    #removes artefactual character
    text = re.sub(r'-­‐‑', '_', text)
    #removes generic copyright notice with link
    text = text.replace(r'[© British Association of Urological Surgeons (BAUS) Limited](http://www.baus.org.uk/)',' ')

    # This section ensures numbered lists are treated as separate sentences
    text = re.sub(
        r"1 _",
        '.1 _', text)
    text = re.sub(
        r"2 _",
        '.2 _', text)
    text = re.sub(
        r"3 _",
        '.3 _', text)
    text = re.sub(
        r"4 _",
        '.4 _', text)

    #Removes simple variabels specified above, and replaces with a space
    for item in remove_list:
        text = re.sub(item, ' ', text)

    return text

def replace_char(text):
    """
    For more complex replacements
    """
    def fraction_modifier(match_obj):
        '''
        Replaces decimal point numbers with a comma to avoid counting this as a sentence
        '''
        ab = match_obj.group()
        groups_ = match_obj.groups()
        if match_obj.group() is not None:
            ans = str(groups_[0]) + ',' + str(groups_[2])
        return ans

    text = re.sub(r'(\d)(\.)(\d)', fraction_modifier, text)


    def list_replacer(match_obj):
        ab = (match_obj.group())
        if match_obj.group() is not None:
            return str(match_obj.group()) + '. '
    identifier = r'Between .{0,35}(\n)?.{0,35}patients' #corrects an issue with handling edge case with this text
    text = re.sub(identifier, list_replacer, text)

    def add_periods(match_obj):
        ''' a function to add periods only when appropriate and missing'''
        ab = (match_obj.group())
        groups_ = match_obj.groups()
        if match_obj.group() is not None:
            ans =  (str(groups_[0]) + str(groups_[1]) + str('. \n ') + str(groups_[2]) + str(groups_[3]))
            return ans

    def correct_underscore(match_obj):
        '''replaces previously added underscores with space'''
        ab = (match_obj.group())
        groups_ = match_obj.groups()
        if match_obj.group() is not None:

            ans = str(groups_[0]) + ' ' + str(groups_[2])
            return ans

    def correct_dashes(match_obj):
        #replaces isolated dashes with equal sign
        ab = (match_obj.group())
        groups_ = match_obj.groups()
        if match_obj.group() is not None:
            ans = str(groups_[0]) + str(groups_[1]) + str('=') + str(groups_[3]) + str(groups_[4])
            return ans

    #Removes periods from acronyms to avoid over counting sentences
    text = text.replace('.e.g.', 'eg')
    text = text.replace('e.g.', 'eg')
    text = text.replace('.i.e.', 'ie')
    text = text.replace('i.e.', 'ie')
    text = text.replace( r'•', '. ')

    text = re.sub(r'\n +?\- +?', ' \n . ', text)

    dash_identifier= r'(\w)( +?)(\-)( +?)(\w)'
    text = re.sub(dash_identifier, correct_dashes, text)
    text = re.sub( r' \- ', '. ', text)

    text = re.sub(r' o ', '. ', text) # replaces bullet points imported as isolated o as a period
    text = text.replace(r'|',' .') #Replaces new cell line with a period to avoid cells merging to produce large sentence
    text = re.sub(r'(\.)\n(\.)*', '. ', text) # removes any 'sentence' with just new lines
    text = re.sub(r'(\.)(\s)?(\.)*', '. ', text) # removes any white space only sentences
    text = re.sub(r'(\.)(\s)?(\.)*', '. ', text) # identical to the above
    text = re.sub(r'(\.)(\.)*', '. ', text) #removes long single lines of periods
    text = re.sub(r'  ', ' ', text) #removes double space to single space
    text = re.sub(r'(\.)(\s)*(\.)+', '. ', text)
    text = re.sub(r'(\.)(\s)*(\.)+', '. ', text)
    text = re.sub(r'(\.)(\s)*(\.)+', ' ', text)
    text = re.sub(r'([a-z]|[A-Z])(_)([a-z]|[A-Z])', correct_underscore, text)

    # removes remaining phone numbers
    text = re.sub(r'()2 *7869 *695', ' ', text)
    text = re.sub(r'( *)2 *74 4 *5 *48', ' ', text)
    text = re.sub(r'(\d{2,4})\s(\d{2,4})(\d{2,4})\s(\d{2,4})?', '', text)

    #identifies sections with missing periods after a newline (e.g due to bullet points)
    identifier3 = r'([\w\:\)])(\s*)(\n)+ *([A-Z][a-z])'
    text = re.sub(identifier3, add_periods, text)
    identifier4 = r'([\w\:\)])(\s*)(\n)+ *(A)'
    text = re.sub(identifier4, add_periods, text)
    identifier5 = r'([\w\:\)])(\s*)(\n+ *\-\-\-\-) *\n* *([A-Z][a-z])'

    text = re.sub(identifier5, add_periods, text)
    text = re.sub(r'©', '', text)
    text = re.sub(r'Leaflet *\/\d+', '', text)
    text = re.sub(r'\. *\n* *\n* *\.', '', text)
    return text



def remove_header(text):
    '''
    Manually removes headers from each different year for older leaflets which were not removed by above steps
    '''
    header14_1 = "# The British Association of Urological Surgeons\n\n\n35-43 Lincoln’s Inn Fields\nLondon\nWC2A 3PE\n\n\n**Phone:**\n\n**Fax:**\n\n**Website:**\n\n**E-mail:**\n\n\n+44 (0)20 7869 6950\n+44 (0)20 7404 5048\n\n[www.baus.org.uk](http://www.baus.org.uk/)\n\nadmin@baus.org.uk\n"
    header14_2 = "## The British Association of Urological Surgeons\n\n\n35-43 Lincoln’s Inn Fields\nLondon\nWC2A 3PE\n\n\n**Phone:**\n\n**Fax:**\n\n**Website:**\n\n**E-mail:**\n\n\n+44 (0)20 7869 6950\n+44 (0)20 7404 5048\n\nwww.baus.org.uk\n\nadmin@baus.org.uk"
    header14_3 = "## The British Association of Urological Surgeons\n\n\n35-43 Lincoln’s Inn Fields\nLondon\nWC2A 3PE\n\n\n**Phone:**\n\n**Fax:**\n\n**Website:**\n\n**E-mail:**\n\n\n+44 (0)20 7869 6950\n+44 (0)20 7404 5048\n\n[www.baus.org.uk](http://www.baus.org.uk/)\n\nadmin@baus.org.uk"
    header15 = "## The British Association of Urological Surgeons\n\n\n35-43 Lincoln’s Inn Fields\nLondon\nWC2A 3PE\n\n\n**Phone:**\n\n**Fax:**\n\n**Website:**\n\n**E-mail:**\n\n\n+44 (0)20 7869 6950\n+44 (0)20 7404 5048\n\n[www.baus.org.uk](http://www.baus.org.uk/)\n\nadmin@baus.org.uk\n"
    header16_1 = "# The \n British \n Association \n of \n Urological \n Surgeons \n \n\n\n35-­‐‑43 \n Lincoln’s \n Inn \n Fields\nLondon\nWC2A \n 3PE\n\n\n**Phone:**\n\n**Fax:**\n\n**Website:**\n\n**E-­‐‑mail:**\n\n\n+44 \n (0)20 \n 7869 \n 6950\n+44 \n (0)20 \n 7404 \n 5048\n\nwww.baus.org.uk\n\nadmin@baus.org.uk"
    header16_2 = "## The \n British \n Association \n of \n Urological \n Surgeons \n \n\n\n35-­‐‑43 \n Lincoln’s \n Inn \n Fields\nLondon\nWC2A \n 3PE\n\n\n**Phone:**\n\n**Fax:**\n\n**Website:**\n\n**E-­‐‑mail:**\n\n\n+44 \n (0)20 \n 7869 \n 6950\n+44 \n (0)20 \n 7404 \n 5048\n\nwww.baus.org.uk\n\nadmin@baus.org.uk"
    header16_3 = "## The British Association of Urological Surgeons\n\n\n35-43 Lincoln’s Inn\nFields\nLondon\nWC2A 3PE\n\n\n**Phone:**\n\n**Fax:**\n\n**Website:**\n\n**E-mail:**\n\n\n+44 (0)20 7869 6950\n+44 (0)20 7404 5048\n\nwww.baus.org.uk\n\nadmin@baus.org.uk"
    if header14_1 in text:
        text = text.replace(header14_1, '')
    if header14_2 in text:
        text = text.replace(header14_2,'')
    if header14_3 in text:
        text = text.replace(header14_3,'')
    if header15 in text:
        text = text.replace(header15,'')
    if header16_1 in text:
        text = text.replace(header16_1, '')
    if header16_2 in text:
        text = text.replace(header16_2,'')
    if header16_3 in text:
        text = text.replace(header16_3,'')
    return text

def remove_footer(text):
    def match_caps(match_obj):
        ab = (match_obj.group())
        groups_ = match_obj.groups()
        if match_obj.group() is not None:
            ans = str(groups_[0]) + str(groups_[1]) + str(groups_[2])
            return str(groups_[2])
    # Removes the footer for 14-16 with capitals
    all_caps_identifier = r'([A-Z][^a-z]+[ \-\(\)]*)(.{1,5}\n*)(Leaflet| ?Page +\n? ?\d)'
    text = re.sub(all_caps_identifier, match_caps, text)

    # Removes footers with leaflet numbers and pages from 2016 onwards
    footer_1 = r"\**Leaflet *\n *No: *\n ?\d*\/\d* *\n* *\|.{0,30}\n.{0,30}Page.{0,30}\n \d*\n\n\n-----"
    # Removes footers with published and review dates from 2024 onwards
    footer_2 = r"\**Published:.{0,30}Leaflet No:.{0,30}\/\d*.{0,30}Page:.{0,30}\d*\n*.{0,30}Due for review:.{0,30}\n+-----"
    footer_3 = r"\**Published:.{0,30}Leaflet No:.{0,30}\/\d*.{0,30}\n*.{0,30}Review due:.{0,30}British Association of Urological Surgeons Limited\n*-----"
    footer_4 = r"\**Published:.{0,30}Leaflet No:.{0,30}Page:.{0,30}\n+Due for review:.{0,30}\[.{0,50}\]\(.{0,50}\)n+-----"
    footer_5 = r"\**Published:.{0,30}Leaflet No:.{0,30}\n+.{0,30}Review due:.{0,30}© British Association of Urological Surgeons Limited\n+-----"
    footer_6 = r"Page \d+\n+-----"
    footers = [footer_1, footer_2, footer_3, footer_4, footer_5, footer_6]
    for footer in footers:
        text = re.sub(footer, '----', text) #4---- to prevent loops
    return text

def sanitizer(text):
    #applies each step of sanitization
    text = remove_header(text)
    text = remove_footer(text)
    text = smart_remove_char(text)
    text = replace_char(text)

    return text

