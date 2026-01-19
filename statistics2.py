import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
import plotly.express as px
import re
import plotly.io as pio
# import cohens_d as cohen
import pingouin as pg #for effect size

import textstat
import statsmodels
import kaleido

def find_iqr(arr1):
    q1 = np.percentile(arr1, 25)
    q3 = np.percentile(arr1, 75)
    iqr = q3 - q1
    return iqr

df = pd.read_excel('reformatted output 16.1.26.xlsx')
sorted_column = df.sort_values(['Year'], ascending=False)

def compare_by_xyz(column1, xyz):
    grouped = df.groupby([xyz])
    for year, value in grouped[column1]:
        print((year, value.mean()))


def save_image(fig, title):
    filename= 'images/' +str(title) + '.png'
    pio.write_image(fig,filename, scale=6, width=1080, height=1080)

# compare_by_xyz('SMOG', 'simplified year category')

paired_grouped = df.groupby('Paired Group')
paired_old_group = df.loc[df['Paired Group'] == 'Historical']
paired_new_group = df.loc[df['Paired Group'] == 'Current']


cats = ['SMOG', 'FRE', 'FKG', 'av_sentence_length',
        'numb_3plus', 'total_sentences', 'total words',
        'number_long_sentences', 'number_over_22_sentence',
        '3syl per sen', 'Passive_percentage',
        'perc_long_sentences', 'per_over_22_word_sentence', 'per_over_25_word_sentence']

# ind_grouped = df.groupby('Group2')
# ind_old_group = df.loc[df['Group2'] == 'old']
# ind_new_group = df.loc[df['Group2'] == 'new']

# extended_cats = ['SMOG', 'FRE', 'FKG', 'FCG',
#         'GF', 'FORCAST', 'av_sentence_length',
#         'numb_3plus', 'total_sentences', 'total words', 'total_letter_count',
#         'total_characters',
#         'bracketed_text_length', 'num_long_bracket_controlled_sentences', 'number_long_sentences', 'number_over_22_sentence',
#         'we_count', 'you_count', '2syl per sen', '3syl per sen', '4syl per sen', 'Undefined counter', 'Passive_percentage', 'No undefined word',
#         'perc_long_sentences', 'per_over_22_word_sentence', 'per_over_25_word_sentence'

# cats_old = ['SMOG', 'FRE', 'FKG', 'CLI', 'ARI', 'FCG',
#         'GF', 'av_sentence_length',
#         'numb_2plus', 'numb_3plus', 'numb_4plus', 'total_sentences', 'total words', 'total_letter_count',
#         'total_characters',
#         'bracketed_text_length', 'num_long_bracket_controlled_sentences', 'number_long_sentences',
#         'we_count', 'you_count', 'Undefined term count']

def paired_comparisons():
    for cat in cats:
        print('\n\n***' + cat + '***\n')
        # print('normality test')
        # print(stats.normaltest(paired_old_group[cat]))
        # print(stats.normaltest(paired_new_group[cat]))
        # print('* MEAN *')
        # print(numpy.mean(paired_old_group[cat]))
        # print(numpy.mean(paired_new_group[cat]))

        print('\n\n*historical group*' + str(stats.describe(paired_old_group[cat])))
        print('*MEDIAN* = ' + str(np.median(paired_old_group[cat])))
        print('\n **IQR** = ' + str(find_iqr(paired_old_group[cat])))
        POG1=paired_old_group[cat]
        print('\n\n*current group*' + str(stats.describe(paired_new_group[cat])))
        print('*MEDIAN* = ' + str(np.median(paired_new_group[cat])))
        print('\n **IQR** = ' + str(find_iqr(paired_new_group[cat])))
        PNG2 = paired_new_group[cat]
        # print('Normal paired t test')
        # print(scipy.stats.ttest_rel(old_group[cat], new_group[cat]))
        print('\n')
        print('\n\nWilcoxon')
        print(stats.wilcoxon(paired_old_group[cat], paired_new_group[cat], alternative='two-sided'))
        # print('\n **COHENs D** = ')
        # CohensD = cohen.cohens_d(paired_old_group[cat], paired_new_group[cat], paired=True)
        # print(f"Paired Cohen's d: {CohensD:.3f}")
        print ("\n")
        pg_effect = pg.wilcoxon(paired_old_group[cat], paired_new_group[cat], correction=False)
        print(pg_effect)


        #Man Whitney is the equivalent for independent T-test
        # Wilcoxon is for Paired non parametric
#
# def non_paired_comparison():
#     for cat in cats:
#         print('*** independent mann whitney ' + cat + '***\n')
#         print('*old group*' + str(stats.describe(ind_old_group[cat])))
#         print('*new group*' + str(stats.describe(ind_new_group[cat])))
#         print('Man whitney')
#         print(stats.mannwhitneyu(ind_old_group[cat], ind_new_group[cat], alternative='two-sided'))


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

# non_paired_comparison()
''' I have stopped the non paired comparisons for now'''

df = df.rename(columns={'Paired Group': 'Paired_Group'})
df = df.query("Paired_Group == 'Historical' or Paired_Group == 'Current'")



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
# filtered_df = df.query("Paired_Group == 'Historical' or Paired_Group == 'Current'")
# df_limited = filtered_df.loc[:, ['Title', 'Year', 'SMOG', 'FKG', 'Paired_Group', 'Passive_percentage', 'perc_long_sentences', '3syl per sen'] ]
# cats_limited = ['SMOG', 'FKG', 'Paired_Group', 'Passive_percentage', 'perc_long_sentences', '3syl per sen']

# manual_df = {'Outcome': ['FRE', 'FKGL', 'SMOG', 'Average sentence length', 'Polysyllabic words per sentence', 'Percentage long sentences','Passive sentence percentage'],
#              'Historical PILs': [paired_old_group['FRE'].mean]
#              }


# new_df= df_limited.groupby('Paired_Group')
# example_df = px.data.tips()

# fig8 = px.box(df_limited, x=cats_limited, y=, color='Paired_Group')

df_joined= pd.DataFrame(joined_array, columns=['Value', 'Group'])
df_joined = df_joined.astype({"Value": int, "Group": str})
df_joined = df_joined[df_joined['Value'] > 24]

fig8 = px.histogram(df_joined, color='Group', barmode='overlay', title = "Histogram of All Sentence Lengths in all PILs by Group over 25 words long",
                    labels = {"Sentence Length": "Sentence Length",
                              "Group": "Group"}
                    )

save_image(fig8, r"Histogram of long Sentences")
# # fig8 = px.box(df_joined, x='Group', y='Value', points='all')
#
# currentFig = fig6
# currentFig.update_layout(title=dict(font=dict(size=24), automargin=False, yref='container'))
#

# currentFig.show()






#fig2.write_image('pngname.png',format="png",width=800,height=500)

# small_df = df[['Title', 'Group2', 'total_sentences', 'sentence_lengths']]
# df2 = pd.DataFrame(columns=['Title', 'Group2','total_sentences','sentence_length'])
#
# for index, row in small_df.iterrows():
#     sentences = eval(row['sentence_lengths'])
#     for sentence in sentences:
#         print(sentence)
#         df2.loc[len(df2)] = [row['Title'], row['Group2'], row['total_sentences'], sentence]
#
# fig3 = px.scatter(df2, x='sentence_length', y='total_sentences', color="Group2", hover_data='Title')
# fig3 = px.histogram(df2, x='sentence_length', color="Group2", hover_data='Title')

# df2 = pd.read_excel('Reformed data for stats.xlsx')
# print("*MANUAL CHECK* SMOG")
# print(stats.mannwhitneyu(df2['Old SMOG'], df2['New SMOG'], alternative='two-sided'))

#
# df['all_words']=df['all_words'].apply(ast.literal_eval)
# Titles = []
# all_words=[]
# for index, row in df.iterrows():
#     Titles.append(row['Title'])
#     all_words.append(row['all_words'])
# raw_data= {'Title':Titles, 'all_words': all_words}
#
# df2 = pandas.DataFrame(raw_data)
# all_wrds = all_words
#
# df3 = pd.DataFrame({'Title':Titles, 'all_words': all_wrds})