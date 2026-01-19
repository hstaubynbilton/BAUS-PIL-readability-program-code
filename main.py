import MDimporter
import textstat, pathlib
import csv
import re
from PassivePySrc import PassivePy
passivepy = PassivePy.PassivePyAnalyzer(spacy_model = "en_core_web_lg")

#Variables
path1 =  'PDF/newall edited v2 Dec 2025'

# #not in use
# def import_text(file):
#     #not in use currently
#     with open(file) as file1:
#         text = file1.read()
#     return text
# def find_year(doc: Document):
#     """finds year from a pdf document opened using pymuPDF"""
#     meta = doc.metadata['creationDate']
#     return meta[2:6]

def file_list_creator(path1):
    """
    Creates a list of pdf files from a path area
    path1 in the form such as 'PDF/2015' """
    output_files=[]
    p = pathlib.Path(path1)
    files1 = (p.glob('*.md'))
    for file in files1:
        output_files = output_files + [file]
    return output_files

def text_extractor3(files):
    """
    takes a list of files and extracts text from them with the file still attached
    :param files:
    :return:
    """
    output =[]
    for file in files:
        print(file)
        md1 = MDimporter.import_text(file)
        md1 = MDimporter.sanitizer(md1)
        exp_title= "MDimporterLog/" + str(file.name[:-3]) + ".txt"
        #prints file to area

        with open(exp_title, 'w') as xf:
            xf.write(md1)
        xf.close()

        assert isinstance(md1, str) #confirms file4 is just text
        year =  'invalid' #a loss from pdf to markdown
        output.append([ file.stem, year, md1])
    return output

def stats_listurator(text_list):
    """
    :param text_list:
    :return :
    """
    output = []
    for item in text_list:
        stats(item)

    return text_list

def stats(text_item):
    """Applies statistics to the 3rd ([2]) of a list item in the form (title, year, text)
    Returns an output list of each statistic [SMOG, SMOG2, FRE, FKG, Flesch2]
    Also currently prints a list of sentence count which varies significantly between functions
    """
    output=[]
    print(text_item[0])
    text1= text_item[2]
    sentences = re.findall(r'\b[^.!?]+[.!?]*', text1, re.UNICODE)
    s_length=[]
    long_sentences = []
    all_sentences = []
    over_22_sentence = []
    over_25_sentence = []
    bracket_controlled_long_sentences = []
    we_count = 0
    you_count = 0
    urethra_count = 0
    waterpipe_count = 0
    laparoscope_count = 0
    keyhole_count = 0
    anaesthetic_count = 0
    sleep_count = 0
    passivePyObject = passivepy.match_text(text1, full_passive=True, truncated_passive=True)
    passive_count = passivePyObject.iloc[0]['passive_count']
    bracketed_text =[]
    for sentence in sentences:
        words = re.findall(r"[\w']+", sentence, re.UNICODE)
        s_length.append(len(words))
        #all_sentences.append(sentence)
        if len(words)>20:
            long_sentences.append(sentence)
            if len(words)>22:
                over_22_sentence.append(sentence)
                if len(words)>25:
                    over_25_sentence.append(sentence)

        bracketed = re.findall(r'\(.+?\)', sentence, re.UNICODE)
        if len(bracketed) > 0:
            for string in bracketed:
                bracketed_text.append(string)
            bracketed_words = []
            for string in bracketed:
                    br_words = re.findall(r"[\w']+", string, re.UNICODE)
                    for word in br_words:
                        bracketed_words.append(word)
            if len(words) - len(bracketed_words) > 20:
                bracket_controlled_long_sentences.append(sentence)
        else:
            if len(words) > 20:
                bracket_controlled_long_sentences.append(sentence)
    num_long_bracket_controlled_sentences = len(bracket_controlled_long_sentences)


    sentence_lengths = s_length
    number_long_sentences = len(long_sentences)
    number_over_22_sentence = len(over_22_sentence)
    number_over_25_sentence = len(over_25_sentence)
    bracketed_text_length = 0
    for string in bracketed_text:
        br_words = re.findall(r"[\w']+", string, re.UNICODE)
        bracketed_text_length += len(br_words)
    bracketed_text_count = len(bracketed_text)
    we_temp = re.findall(r"\W[Ww]e\W", text1, re.UNICODE)
    you_temp = re.findall(r"\W[Yy]our?\W", text1, re.UNICODE)
    urethra_temp = re.findall(r"\W[Uu]rethral?\W", text1, re.UNICODE)
    waterpipe_temp = re.findall(r"\W[Ww]ater ?pipe\W", text1, re.UNICODE)
    laparoscope_temp = re.findall(r"\W[Ll]aparo", text1, re.UNICODE)
    teloscope_temp = re.findall(r"\W[Tt]eloscop", text1, re.UNICODE)
    keyhole_temp = re.findall(r"\W[Kk]ey ?hole\W", text1, re.UNICODE)
    anaesthetic_count = len(re.findall(r'[Gg]eneral.[Anaesth]', text1, re.UNICODE))
    abdomen_count = len(re.findall(r"[Aa]bdom", text1, re.UNICODE))
    tummy_count = len(re.findall(r"[Tt]ummy", text1, re.UNICODE))
    stricture_count = len(re.findall(r"[Ss]tricture", text1, re.UNICODE))
    narrowing_count = len(re.findall(r"[Nn]arrowing", text1, re.UNICODE))
    ED_count = len(re.findall(r"[Ee]rectile [Dd]ysfunction", text1, re.UNICODE))
    poor_erect_count = len(re.findall(r"[Pp]oor [Ee]rection", text1, re.UNICODE))
    impotence_count = len(re.findall(r"[Ii]mpotence", text1, re.UNICODE))
    impotence_count += poor_erect_count
    atrophy_count = len(re.findall(r"[Aa]trophy", text1, re.UNICODE))
    shrinking_count = len(re.findall(r"[Ss]hrink", text1, re.UNICODE))
    sleep_count = len(re.findall(r"[Ss]leep", text1, re.UNICODE))
    we_count = len(we_temp) #not much point in this as both are already addressed to the person
    you_count = len(you_temp)
    urethra_count = len(urethra_temp)
    waterpipe_count = len(waterpipe_temp)
    laparoscope_count = len(laparoscope_temp) +len(teloscope_temp)
    keyhole_count = len(keyhole_temp)

    # medical_terms_list= ['ureter', 'cystoscop', 'ureterosc', 'incision', ]
    # other_medical_terms = 0


    total_sentences = textstat.textstat.sentence_count(text1)
    av_sentence_length = textstat.textstat.avg_sentence_length(text1)
    numb_2plus = textstat.textstat.difficult_words(text1, syllable_threshold=2)
    numb_3plus = textstat.textstat.polysyllabcount(text1)
    numb_3plus_old = textstat.textstat.difficult_words(text1, syllable_threshold=3)
    numb_4plus = textstat.textstat.difficult_words(text1, syllable_threshold=4)
    difficult_words_list = textstat.textstat.difficult_words_list(text1, syllable_threshold=4)
    total_words = textstat.textstat.lexicon_count(text1)
    total_characters = textstat.textstat.char_count(text1, ignore_spaces=True)
    total_letter_count = textstat.textstat.letter_count(text1, ignore_spaces=True)

    #Readability stats
    SMOG = textstat.smog_index(text1)
    FRE = textstat.flesch_reading_ease(text1)
    FKG = textstat.flesch_kincaid_grade(text1)
    FCG = textstat.flesch_kincaid_grade(text1)
    CLI = textstat.coleman_liau_index(text1)
    ARI = textstat.automated_readability_index(text1)
    DCR = textstat.dale_chall_readability_score(text1)
    LWF = textstat.linsear_write_formula(text1)
    GF = textstat.gunning_fog(text1)
    TS = textstat.text_standard(text1)
    FH = textstat.fernandez_huerta(text1)
    SP = textstat.szigriszt_pazos(text1)
    GP = textstat.gutierrez_polini(text1)
    CRA = textstat.crawford(text1)
    GPI = textstat.gulpease_index(text1)
    OSM = textstat.osman(text1)
    FORCAST = textstat.forcast_index(text1)

    #Complex things
    all_words = re.findall(r"[\w']+", text1, re.UNICODE)

    # SMOG2 = s.smog_score #This is no longer relevant, as the counting of medical terms has been edited for text stat
    # Flesch2 = s.flesch_score
    # TS_sentence_count = textstat.textstat.sentence_count(text1)
    # TT_sentence_count = s.sent_count
    # print("SENTENCE COUNT")
    # print(text_item[0])
    # print(TT_sentence_count)
    # print(TS_sentence_count) #edited textstat.py line 384 to remove minimum sentence length requiement

    # r = Readability(text1)
    # SMOG2 = r.smog()
    # FKG2 = r.flesch_kincaid()


    output = [SMOG, FRE, FKG, CLI, ARI, FCG, DCR,
              LWF, GF, TS, FH, SP, GP, CRA, GPI, OSM, FORCAST, av_sentence_length,
              numb_2plus, numb_3plus,numb_4plus, total_sentences, total_words,
              total_letter_count, difficult_words_list, sentence_lengths,
              all_sentences, number_over_22_sentence, number_over_25_sentence, bracketed_text, bracketed_text_count, bracketed_text_length,
              num_long_bracket_controlled_sentences, number_long_sentences, we_count, you_count,
              urethra_count, waterpipe_count, laparoscope_count, keyhole_count, anaesthetic_count,
              sleep_count, abdomen_count, tummy_count, stricture_count, narrowing_count, ED_count,
              impotence_count, atrophy_count, shrinking_count, passive_count]
    for item in output:
        text_item.append(item)
    return text_item

def export(files_list):
    "exports to output.csv each line in the files_list with a Title, Year, text, and stats columns"
    with open ('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        field = ['Title', 'Year', 'text', 'SMOG', 'FRE', 'FKG', 'CLI', 'ARI', 'FCG', 'DCR',
                 'LWF', 'GF', 'TS', 'FH', 'SP', 'GP', 'CRA', 'GPI', 'OSM', 'FORCAST', 'av_sentence_length',
                 'numb_2plus', 'numb_3plus', 'numb_4plus', 'total_sentences', 'total words',
                 'total_letter_count', 'difficult_words_list', 'sentence_lengths',
                 'all_sentences', 'number_over_22_sentence','number_over_25_sentence', 'bracketed_text', 'bracketed_text_count', 'bracketed_text_length',
                 'num_long_bracket_controlled_sentences', 'number_long_sentences', 'we_count', 'you_count',
                 'urethra_count', 'waterpipe_count', 'laparoscope_count', 'keyhole_count', 'anaesthetic_count',
                 'sleep_count', 'abdomen_count', 'tummy_count', 'stricture_count', 'narrowing_count', 'ED_count',
                 'impotence_count', 'atrophy_count', 'shrinking_count', 'passive_count']
        writer.writerow(field)
        for file in files_list:
            writer.writerow(file)
    # for item in files_list:
    #     break
    return None



files1 = file_list_creator(path1)
processed_files = text_extractor3(files1)
c = stats_listurator(processed_files)
export(c)