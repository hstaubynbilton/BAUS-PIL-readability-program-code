import MDimporter
import textstat, pathlib
import csv
import re
from PassivePySrc import PassivePy
passivepy = PassivePy.PassivePyAnalyzer(spacy_model = "en_core_web_lg")

#Variables
#path1 is the location of your input PDF documents
path1 =  'PDF/newall edited v2 Dec 2025'

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
        #prints file to MDimporterLog for easy inspection of text

        with open(exp_title, 'w') as xf:
            xf.write(md1)
        xf.close()

        assert isinstance(md1, str) #confirms file4 is just text
        year =  'invalid' #a loss from pdf to markdown
        output.append([ file.stem, year, md1])
    return output

def stats_listurator(text_list):
    """
    :param text_list: takes a list of text as an input
    :return : returns the required readability stats for each document and returns as a list
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
    print(text_item[0])
        #prints the current item title to check progress
    text1= text_item[2]
    sentences = re.findall(r'\b[^.!?]+[.!?]*', text1, re.UNICODE)
        #finds all sentences
    #Variables
    s_length=[]
    long_sentences = []
    all_sentences = []
    over_22_sentence = []
    over_25_sentence = []
    bracket_controlled_long_sentences = []

    passivePyObject = passivepy.match_text(text1, full_passive=True, truncated_passive=True)
    #identifies the number of passive sentences using passivepy
    passive_count = passivePyObject.iloc[0]['passive_count']
    #extracts the count of passive sentences as saves it as passive_count variable
    bracketed_text =[]
    for sentence in sentences:
        words = re.findall(r"[\w']+", sentence, re.UNICODE)
        s_length.append(len(words))
        #saves all sentence lengths as a list- unused feature
        if len(words)>20:
            long_sentences.append(sentence)
            #saves sentences longer than 20 to long sentences
            if len(words)>22:
                over_22_sentence.append(sentence)
                #saves sentences longer than 22 to over_22_sentence
                if len(words)>25:
                    over_25_sentence.append(sentence)
                    #saves sentences longer than 25 to over_25_sentence

        # ==Below is an unused feature to count bracketed text==
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

    # ==This section extracts output variables from lists==
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
    total_sentences = textstat.textstat.sentence_count(text1)
    av_sentence_length = textstat.textstat.avg_sentence_length(text1)
    numb_2plus = textstat.textstat.difficult_words(text1, syllable_threshold=2)
    numb_3plus = textstat.textstat.polysyllabcount(text1)
    numb_4plus = textstat.textstat.difficult_words(text1, syllable_threshold=4)
    difficult_words_list = textstat.textstat.difficult_words_list(text1, syllable_threshold=4)
    total_words = textstat.textstat.lexicon_count(text1)
    total_characters = textstat.textstat.char_count(text1, ignore_spaces=True)
    total_letter_count = textstat.textstat.letter_count(text1, ignore_spaces=True)

    #==Readability stats== This section extracts multiple readability stats which can then be chosen from
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

    #Here the required variables to write to the output excel document are specified, and the required order, which are then returned as a list
    output = [SMOG, FRE, FKG, CLI, ARI, FCG, DCR,
              LWF, GF, TS, FH, SP, GP, CRA, GPI, OSM, FORCAST, av_sentence_length,
              numb_2plus, numb_3plus,numb_4plus, total_sentences, total_words,
              total_letter_count, difficult_words_list, sentence_lengths,
              all_sentences, number_over_22_sentence, number_over_25_sentence, number_long_sentences, passive_count]
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
                 'all_sentences', 'number_over_22_sentence','number_over_25_sentence', 'passive_count']
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