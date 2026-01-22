import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
import plotly.express as px
import re
import plotly.io as pio
import pingouin as pg #for effect size


def find_iqr(arr1):
    """
    Finds IQR
    """
    q1 = np.percentile(arr1, 25)
    q3 = np.percentile(arr1, 75)
    iqr = q3 - q1
    return iqr

def save_image(fig, title):
    """
    function to save images to output folder
    """
    filename= 'images/' +str(title) + '.png'
    pio.write_image(fig,filename, scale=6, width=1080, height=1080)

data_file1 = 'reformatted output 16.1.26.xlsx'
#loads file as a dataframe
df = pd.read_excel(data_file1)

#Separates the files by group
sorted_column = df.sort_values(['Year'], ascending=False)
paired_grouped = df.groupby('Paired Group')
paired_old_group = df.loc[df['Paired Group'] == 'Historical']
paired_new_group = df.loc[df['Paired Group'] == 'Current']


#Defines the categories to analyse
cats = ['SMOG', 'FRE', 'FKG', 'av_sentence_length',
        'numb_3plus', 'total_sentences', 'total words',
        'number_long_sentences', 'number_over_22_sentence',
        '3syl per sen', 'Passive_percentage',
        'perc_long_sentences', 'per_over_22_word_sentence', 'per_over_25_word_sentence']



def paired_comparisons():
    """
    Performs a paired analysis
    :return:
    """
    for cat in cats:
        print('\n\n***' + cat + '***\n')
        # == This section no longer required- initially assessed normality
        # print('normality test')
        # print(stats.normaltest(paired_old_group[cat]))
        # print(stats.normaltest(paired_new_group[cat]))
        # print('* MEAN *')
        # print(numpy.mean(paired_old_group[cat]))
        # print(numpy.mean(paired_new_group[cat]))

        #prints the outputted stats
        print('\n\n*historical group*' + str(stats.describe(paired_old_group[cat])))
        print('*MEDIAN* = ' + str(np.median(paired_old_group[cat])))
        print('\n **IQR** = ' + str(find_iqr(paired_old_group[cat])))
        print('\n\n*current group*' + str(stats.describe(paired_new_group[cat])))
        print('*MEDIAN* = ' + str(np.median(paired_new_group[cat])))
        print('\n **IQR** = ' + str(find_iqr(paired_new_group[cat])))
        print('\n')
        print('\n\nWilcoxon')
        print(stats.wilcoxon(paired_old_group[cat], paired_new_group[cat], alternative='two-sided'))
        print ("\n")

        pg_effect = pg.wilcoxon(paired_old_group[cat], paired_new_group[cat], correction=False)
        print(pg_effect)


def all_sentence_length(array):
    #array of arrays here
    all_sentences=[]

    for list1 in array:
        list1 = list1[1:-1]
        list1 = re.findall(r'\d+', list1)
        for item in list1:
            item = int(item)
            all_sentences.append(item)
    return all_sentences


value1 = paired_old_group['sentence_lengths']
old_group_sentences = all_sentence_length(paired_old_group['sentence_lengths'])
new_group_sentences = all_sentence_length(paired_new_group['sentence_lengths'])
old_group_sentence_array = np.array(old_group_sentences)
new_group_sentence_array = np.array(new_group_sentences)
b1 = np.full(new_group_sentence_array.shape, 'Current')
current_array = np.stack((new_group_sentence_array, b1), axis=1)
b2 = np.full(old_group_sentence_array.shape, 'Historical')
old_array = np.stack((old_group_sentence_array, b2), axis=1)
joined_array = np.concatenate((current_array, old_array))



print('test')
paired_comparisons()
print('end of paired comparisons')


df = df.rename(columns={'Paired Group': 'Paired_Group'})
df = df.query("Paired_Group == 'Historical' or Paired_Group == 'Current'")


# ===Figure generator===
# This section generates figures using plotly using defined settings

fig1 = px.scatter(df, x="polysyl_per_100words", y="sent_per_100_words", color="Paired_Group",
                  marginal_x='histogram', marginal_y='histogram',
                  hover_data='Title', size='total_sentences',
                  title="Polysyllabilic words per 100 words versus sentences per 100 words",
                  labels={"polysyl_per_100words":"Polysyllabic words (per 100 words)",
                          "sent_per_100_words": "Sentences (per 100 words)",
                          "Paired_Group": "Group"
                          }

                  )
save_image(fig1, 'syllables vs sentences per 100 words')

fig2 = px.histogram(df, x='Passive_percentage', color="Paired_Group", hover_data='Title',
                    marginal="box", barmode='overlay',
                  title="Percentage of Passive Sentences by Group",
                  labels={
                     "Passive_percentage": "Percentage of Passive Sentences",
                     "Paired Group": "Group",
                    })
save_image(fig2, 'Percentage of Passive Sentences by Group')

fig3 = px.histogram(df, x='total words', color="Paired_Group", hover_data='Title',
                    marginal="box", barmode='overlay',
                   title="Word Count by Group",
                   labels={
                     "total words": "Total Number of Words",
                     "Paired_Group": "Group",
                    })
save_image(fig3, 'Total Number of Words by Group')

fig5 = px.scatter(df, x="number_long_sentences", y="total words", hover_data='Title', color="Paired_Group")
save_image(fig5, 'Total Number of Words by Group2')


fig6 = px.scatter(df, x="SMOG", y="FKG", color="Paired_Group", size="total words", hover_data="Title",
                  marginal_x='box', marginal_y='box',
                  title="SMOG vs Flesh-Kincaid Grade (FKGL)",
                  labels={
                     "SMOG": "SMOG",
                     "FKG": "Flesch-Kincaid Grade Level (FKGL)",
                     "Paired_Group": "Group",
                 },)
save_image(fig6, 'Flesh-Kincaid Grade vs SMOG by group')

df = df.rename(columns={'Paired Group': 'Paired_Group'})

# This section creates a custom dataframe to create a diagram for longer sentences
df_joined= pd.DataFrame(joined_array, columns=['Value', 'Group'])
df_joined = df_joined.astype({"Value": int, "Group": str})
df_joined = df_joined[df_joined['Value'] > 24]

fig8 = px.histogram(df_joined, color='Group', barmode='overlay', title = "Histogram of All Sentence Lengths in all PILs by Group over 25 words long",
                    labels = {"Sentence Length": "Sentence Length",
                              "Group": "Group"}
                    )
save_image(fig8, r"Histogram of long Sentences")
