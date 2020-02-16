import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import pymorphy2 as pm
import numpy as np
import roman
import os, sys, copy, math

#Preprocessing start#
def countingFeatures(features):
    number_of_features = 0
    for feature in features:
        number_of_features += features[feature]
    return number_of_features

def countingProbability(quantity, features):
    features_probability = {}
    for feature in features:
        probability = features[feature]/quantity
        features_probability.setdefault(feature, probability)
    return features_probability


def deletePunctuation(sentence):
    punct = string.punctuation
    punct += '—–...«»'
    words_list = [word for word in sentence if (word not in punct)]
    return words_list


morph = pm.MorphAnalyzer()
path = os.getcwd() + '\documents'
os.chdir(path)
file_list = os.listdir(path)                                     # список, хранящий имена файлов

dictionary = []
word_count = 0
sentence_count = 0
number_of_features = 0
number_of_words = 0
text_count = len(file_list)
unique_structures = []
morph_features = []

## Морфологические признаки ##
pos_count = {
                        # Часть речи
                        'NOUN': 0, 'ADJF': 0, 'ADJS': 0, 'COMP': 0, 'VERB': 0, 'INFN': 0,
                        'PRTF': 0, 'PRTS': 0, 'GRND': 0, 'NUMR': 0, 'ADVB': 0, 'NPRO': 0,
                        'PRED': 0, 'PREP': 0, 'CONJ': 0, 'PRCL': 0, 'INTJ': 0
            }
case_count = {
                        # Падеж
                        'nomn': 0, 'gent': 0, 'datv': 0, 'accs': 0, 'ablt': 0, 'loct': 0,
                        'voct': 0, 'gen2': 0, 'acc2': 0, 'loc2': 0
            }
number_count = {
                        # Число
                        'sing': 0, 'plur': 0
            }
gender_count = {
                        # Род
                        'masc': 0, 'femn': 0, 'neut': 0
            }
other_count = {
                        # Нестандартные граммемы
                        'LATN': 0, 'PNCT': 0, 'NUMB': 0, 'intg': 0, 'real': 0,
                        'ROMN': 0, 'UNKN': 0
            }


for name_text in file_list:
    with open(name_text, encoding='utf-8') as text:
        document = sent_tokenize(text.read().lower())
    sentence_count += len(document)

    for sent in range(len(document)):
        # Токенизация по словам
        document[sent] = word_tokenize(document[sent])
        # Определяем морфологические признаки слов в обрабатываемом предложении
        morph_features.append([morph.parse(word)[0] for word in document[sent]])
        # Удаляем пунктуацию из предложения
        document[sent] = deletePunctuation(document[sent])
        # Приводим в предложении слова к нормальной форме
        document[sent] = [morph.parse(word)[0].normal_form for word in document[sent]]
        # Добавляем количество слов из обрабатываемого предложения к счетчику слов
        number_of_words += len(document[sent])

        for word in range(len(document[sent])):
            dictionary.append(document[sent][word])

        for feature in range(len(morph_features[sent])):

            if morph_features[sent][feature].tag.POS != None:
                dump = morph_features[sent][feature].tag.POS
                pos_count[dump] += 1

                dump = morph_features[sent][feature].tag.case
                if dump != None: case_count[dump] += 1

                dump = morph_features[sent][feature].tag.number
                if dump != None: number_count[dump] += 1

                dump = morph_features[sent][feature].tag.gender
                if dump != None: gender_count[dump] += 1
            else:
                dump = str(morph_features[sent][feature].tag)
                if dump.find('NUMB') != -1:
                    dump = 'NUMB'
                other_count[dump] += 1

    document.clear()
    morph_features.clear()

dictionary = set(dictionary)
dictionary = sorted(dictionary)
number_pos = countingFeatures(pos_count)
number_case = countingFeatures(case_count)
number_number = countingFeatures(number_count)
number_gender = countingFeatures(gender_count)
number_other = countingFeatures(other_count)

pos_prob = countingProbability(number_pos, pos_count)
case_prob = countingProbability(number_case, case_count)
number_prob = countingProbability(number_number, number_count)
gender_prob = countingProbability(number_gender, gender_count)
other_prob = countingProbability(number_other, other_count)


print (dictionary)


# graph = np.zeros((len(dictionary), len(dictionary)))
# createGraph()
# np.set_printoptions(threshold=sys.maxsize, linewidth=sys.maxsize)
# print(graph)


# def createGraph(graph):
#     for dict in range(len(dictionary)):
#         for name_text in file_list:
#             for sent in range(len(corpus[name_text])):
#                 for word in range(len(corpus[name_text][sent])):
#                     if corpus[name_text][sent][word] in dictionary and corpus[name_text][sent][word] not in dictionary[dict]:
#                         wrd = morph.parse(corpus[name_text][sent][word])[0].normal_form
#                         index = dictionary.index(wrd)
#                         graph[dict][index] += 1
#     return graph


# def struc():
#     structure = []
#     # for name_text in file_list:
#     #     for sent in range(len(corpus[name_text])):
#     # print(corpus['text_0.txt'][0])
#     for word in range(len(corpus['text_0.txt'][0])):
#         if morph_parametres['text_0.txt'][0][word].tag.POS != None:
#             structure.append(str(morph_parametres['text_0.txt'][0][word].tag))
#         else:
#             structure.append(str(morph_parametres['text_0.txt'][0][word].tag))
#     return structure

# def termFrequency():
#     tf = []; nk = 0
#     for i in range(len(sentences)):
#         nk += len(sentences[i])
#
#     for i_vcb in range(len(vocabulary)):
#         ni = 0
#         for i_sent in range(len(sentences)):
#             ni += sentences[i_sent].count(vocabulary[i_vcb])
#         tf.append(ni/nk)
#     return tf
#
#
# def inverseDocumentFrequency():
#     idf = np.zeros(len(vocabulary))
#     nqi = np.zeros(len(vocabulary))
#     N = len(dir_work)
#     for word in range(len(vocabulary)):
#         for text in range(len(sentences)):
#             for sent in range(len(sentences[text])):
#                 if vocabulary[word] in sentences[text][sent]:
#                     nqi[word] += 1
#                     break
#         idf[word] = math.log((N - nqi + 0.5)/(nqi + 0.5))
#
#     return idf