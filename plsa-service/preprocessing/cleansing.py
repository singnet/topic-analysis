__author__ = 'masresha'
# Runs on python3.6
# this block of code first reads a files directory


import sys
import pathlib
import os
import json

sys.path.append(str(pathlib.Path(os.path.abspath('')).parents[1])+'/plsa')
sys.path.append(str(pathlib.Path(os.path.abspath('')).parents[1])+'/plsa/preprocessing')


# import codecs

import glob
import nltk
from nltk.corpus import stopwords
import pathlib as path
from stemming.porter2 import stem
import string
# import preprocessing.porter_dictionary as pp
import porter_dictionary as pp
# import re

port_dict = pp.porter_dictionary()



# file_parts_number = 9


file_dict = ''
source_texts = ''
output_dir = ''
file_parts_number = 8
# file_parts_number = 7 # Inspire



# fileList = glob.glob(source_texts)


punct=['…','•','”','→','↑','“','‘','’','—','£','€','$']







pos_dict = {'JJ': 'a', 'JJR': 'a',
            'JJS': 'a', 'NN': 'n',
            'NNS': 'n', 'NNP': 'n',
            'NNPS': 'n', 'PRP': 'n',
            'PRP$': 'n', 'RB': 'r',
            'RBR': 'r', 'RBS': 'r',
            'VB': 'v', 'VBD': 'v',
            'VBG': 'v', 'VBN': 'v',
            'VBZ': 'v', }

wnl = nltk.WordNetLemmatizer()
stop = stopwords.words('english')

z = []
wnl_tokens = []


def is_float(x):
    try:
        float(x)
        return True
    except:
        return False


def has_token_punct(token):
    for char in token:
        if (char in string.punctuation) or (char in punct):
            return True
            break
        else:
            pass


def find_punct(token):
    ch = []
    for char in token:
        if ((char in string.punctuation) or (char in punct)):
            ch.append(char)

    return ch
    # break
def isEnglish(s):
    # print('444444444444444444444444')
    # print(s)
    # s = s.decode('utf-8')
    # try:
    #     s.encode('ascii')
    # except UnicodeEncodeError:
    #     return False
    # else:
    #     return True

    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def return_cleaned(t1):
    returned_token = []



    for i in t1:
        # print(i)
        # print(type(i))
        if (len(i) < 2 or len(i)>12):
            # print('-------',i)
            pass
        elif (i[:2] == '//'):
            # print('*******',i)
            pass
        elif (is_float(i)):
            pass
        # elif (i.__contains__(',')):
        # pass
        elif (i.__contains__('www.') or i.__contains__('xxx.') or i.__contains__('yyy.') or i.__contains__('.gov') ):
            pass
        elif (str(i).endswith('.com') or str(i).endswith('.html') or str(i).endswith('.php') or str(i).endswith(
                '.aspx') or str(i).endswith('.asp') or str(i).endswith('htm') or str(i).endswith('pdf')):
            pass
        elif (str(i).startswith('http') or str(i).startswith('https') or str(i).startswith('/') ):
            pass
        # elif(isEnglish(i)==False):
        #         pass
        else:
            returned_token.append(i)

    # print returned_token
    #removes punctuation from a string and remove the  remaining string if it is a number
    token_list = []
    for token in returned_token:

        if ((has_token_punct(token))):
            chr = find_punct(token)
            new_token=token
            for ch in chr:
                if (ch=='-'):
                 new_token = str(new_token).replace(ch, ' ')

                else:
                  new_token = str(new_token).replace(ch, '')
            # checks if after punctuation is removed  and its length is <2
            if (is_float(new_token)):
            # if ((new_token.isalpha()=='false' or new_token.isdigit()=='false')):
                pass
            elif(isEnglish(new_token)==False):
                pass

            else:
                token_list.append(new_token)
        elif(isEnglish(token)==False):
                pass
        else:
            token_list.append(token)

    # print  ('Token List',new_token)
    return token_list
# print (token_list)

# print  returned_token
# return returned_token



def pre_pro():
    # fileList = glob.glob(source_texts)
    # fileList_len = fileList.__len__() - 1

    cleaned_dict = {}

    with open(source_texts, "r") as read_file:
        fileList = json.load(read_file)
    k = 0
    print('------pre-process started-------')
    for files in fileList:
        tFile = fileList[files]
        # tFile = codecs.open(files, 'r', 'utf-8')
        line = tFile.lower()
        # print(line)
        # print(type(line))
        # line = line.decode('utf-8')
        tokens = nltk.word_tokenize(line)
        # print(tokens)
        for ijk in range(len(tokens)):
            # tokens[ijk] = tokens[ijk].encode('utf-8')
            tokens[ijk] = tokens[ijk]

        clean_tokens = return_cleaned(tokens)



        # print clean_tokens
        clean_tokens = filter(lambda name: name.strip(), clean_tokens)
        # result = list(filter(None, clean_tokens))
        # print clean_tokens
        final_tok=[]
        for tok in clean_tokens:
            # print (tok)
            tok= str(tok).rstrip(' ')
            # if(len(tok) < 2 ):
            #     clean_tokens.remove(tok)
            if(len(str(tok).split(' ')) > 1):
                # print tok+' '+str(len(str(tok).split(' ')))
                # print tok
                token=nltk.word_tokenize(tok)
                cl_tok= return_cleaned(token)
                for tk in cl_tok:
                    # print tk
                    final_tok.append(tk)
                # clean_tokens.remove(tok)
            else:
                final_tok.append(tok)
            # print clean_tokens
                # clean_tokens.append(token)

                # print token
        # tokens= nltk.word_tokenize(clean_tokens)
        # print tokens

        # tokens = Pun_pattern.sub("", str(tokens))
        # tokenstemp = []
        # for t1 in tokens:
        # for tt1 in t1:
        #         if(not string.punctuation.__contains__(tt1)):
        #             if(t1 != "'s"):
        #                 tokenstemp.append(t1)
        #             break

        # tokens = tokenstemp

        filtered_words = [w for w in final_tok if not w in stopwords.words('english')]
        # print filtered_words
        POS_Tokens = nltk.pos_tag(filtered_words)

        z = []
        for x in POS_Tokens:
            try:
                z.append(pos_dict[x[1]])
            except:
                z.append('n')

        wnl_tokens = []
        for i in range(len(filtered_words)):
            # if (len(clean_tokens[i])>3):
            #     wnl_tokens.append(wnl.lemmatize(clean_tokens[i], z[i]))
            # else:
                wnl_tokens.append(filtered_words[i])
        por_tokens = [stem(t) for t in wnl_tokens]
        # print por_tokens

        temp_term1 = ''
        term1 = ''

        for stmd in range(len(filtered_words)):

                term1 = por_tokens[stmd]
                temp_term1 = filtered_words[stmd]

                # print term1,temp_term1

                port_dict.add_element(stemmed=term1,nonstemmed=temp_term1)

        # file_txt = open(output_dir + path.PurePath(files).parts[file_parts_number], "w")

        temp = ''

        for i in por_tokens:
            temp = temp + i + '\n'

        cleaned_dict[files] = temp

        # print('Processed ',k,'of',fileList_len)
        k = k + 1

    file_json = output_dir + 'cleaned.json'

    with open(file_json, "w") as f:
        json.dump(cleaned_dict, f, indent=4)

    port_dict.write_dict_to_file(file_dict)
    print('***------pre-process finished--------')

if __name__ == '__main__':

    pre_pro()



