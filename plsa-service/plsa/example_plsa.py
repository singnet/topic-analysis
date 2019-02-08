#!/usr/bin/env python

import sys

import os
import time
import glob
import random
import logging
import numpy as np


# import taskmanager as tm
import pandas as pd
from tfidf.preprocessing import read_files, preprocess_documents, read_json, json_files_list
# from tfidf.porter import PorterStemmer
from tfidf.tfidf import *
# from tfidf.preprocessing import file_list, empty_file_list

# from plsa import pLSA
import plsa as plsa1
import porter_dictionary

# s_file_list = []

empty_docs_list = []

file_parts_number = 8
# file_parts_number = 7 # Inspire

folder = ''
dict_path = ''

file= 'plsa_topics.txt'
# file1='word_topics'
file2='topic_probability_pz'

PLSA_PARAMETERS_PATH = ''
# file_txt1 = open(PLSA_PARAMETERS_PATH + file1, "w")

PATH=''
PATH_word_by_topic_conditional=''

matrix_file = ''
# num_topics = 1672
# num_topics = 5403
# num_topics = 5

num_topics = 24
topic_divider = 5
# num_topics = 256
num_topics_generated = 300
# cc = 0.3 # This is convergence criterion
cc = 0.0000000000000000007 # This is convergence criterion
# cc = 0.7 # This is convergence criterion -- was used for :D
# cc = 0.13 # This is convergence criterion
# maxiter2 = 50
maxiter2 = 22
beta = 1
min_iteration = 10
logL_pic = ''
eps = 0.01
number_of_words = 0
number_of_docs = 0
RAM_limit = 25 # In giga bytes

print('RAM usage has been limited to {} GBs >>>>>>>>>>>>>>>>>>>>>>>>>>'.format(RAM_limit))

# @tm.task(str)

def feat(folder):
    global num_topics
    # docs = list(preprocess_documents(read_files(os.path.join(folder, "*.txt"))))
    docs = list(preprocess_documents(read_json(folder+"/cleaned.json")))
    assert(len(docs) > 0)
    print("len(docs) =",len(docs))
    # Uncomment this later and fix it with the new json theme
    # docs_2 = list(docs)
    # docs_reduced = reduce_docs(docs)
    #
    #
    # if docs_reduced.__len__() != docs_2.__len__():
    #
    #     list_1 = docs_to_delete(docs=docs_2, docs_red=docs_reduced)
    #     delete_docs(list_1)
    #
    #     docs = preprocess_documents(read_files(os.path.join(folder, "*.txt")))
    #     assert(len(docs) > 0)
    #     print("len(docs) =",len(docs))
    # Uncomment ends here

    # num_topics = int(len(docs) / topic_divider)
    # if(num_topics < 2):
    #     num_topics = 2
    #stemmer = PorterStemmer()
    #docs = stemmer.stem_documents(docs)
    td_dict, vocab = tc(docs)

    print("'''''''''''''''''''''''''''''''")
    # print(td_dict)

    for doc in range(len(docs)):
        if docs[doc] == '':
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Empty doc detected with id:',doc,' and file name is:',json_files_list[doc])
            empty_docs_list.append(doc)

    print ('len(td_dict) =', len(td_dict))
    print ('len(vocab) =',len(vocab))
    global number_of_words
    global number_of_docs
    number_of_words = len(vocab)
    number_of_docs = len(td_dict)
    print('type(docs):',type(docs))
    print('type(vocab):',type(vocab))
    # print('docs',docs)
    # print('td_dict:',td_dict)
    # print('vocab',vocab)
    td = to_sparse_matrix(td_dict, vocab).toarray()
    # print('td:',td)
    print('type(td):',type(td))
    # idf = to_vector(idf_from_tc(td_dict), vocab)
    print ("term-document matrix size", td.shape)
    print(td.shape[0],'terms by',td.shape[1],'docs')
    print("size of term-document matrix in bytes according to sys.getsizeof =",sys.getsizeof(td))
    if topic_divider == 0:
        pass
    else:
        num_topics = int(td.shape[1] / topic_divider)
    # num_topics = 30
    # num_topics = 7
    # num_topics = 2
    if (num_topics < 2):
        num_topics = 2
    # matrix_to_file(td)
    # print 'td\n',td
    # print 'vocab\n',vocab
    # return td, idf, vocab
    # exit(0)
    return td, vocab

def K(D):
    global num_topics
    if topic_divider == 0:
        pass
    else:
        num_topics = int(D/topic_divider)
    if (num_topics < 2):
        num_topics = 2
    return num_topics

def docs_to_delete(docs,docs_red):

    list_1 = []

    for i in range(docs.__len__()):

        index = next((k for k in range(docs_red.__len__()) if docs[i]==docs_red[k]),-1)

        if index != -1:
            del docs_red[index]
        else:
            list_1.append(i)

    print('Number of files for deletion ',list_1.__len__())

    return list_1

def delete_docs(list_1):

    pattern_1 = os.path.join(folder, "*.txt")

    f = glob.glob(pattern_1)

    print('Deleting files started ....................')

    for i in list_1:

        try:
            os.remove(f[i])

        except Exception as e:

            print('Error during file deletion while reducing docs')
            logging.exception("message")

    print('Deleting files ended ||||||||||||||||||||||')


def reduce_docs(docs):

    G = 1024**3
    percent_to_delete = 0.05

    counter = 0


    while True:

        counter = counter + 1
        print("counter =", counter)

        # Calculate number of keywords
        words_coll = []
        for words in docs:
            words_coll.extend(words.split())

        W = len(set(words_coll))

        # ram=((d*w)+(d+w)*k*2)*8)/G
        ram = (float(len(docs)*W) + float(len(docs)+W) * float(K(len(docs))*2))*8.0/float(G)


        # No more for debugging purposes
        print("ram =", ram)
        print('len(docs =', len(docs))
        print("W =", W)

        if ram > RAM_limit:

            # # For debugging
            # if counter == 68:
            #     break

            if counter == 1:
                print('Ram limiter code initialted ---------------------------------')

            del_len = int(len(docs) * percent_to_delete)

            del_list = random.sample(range(0, len(docs)), del_len)

            for i in range(del_list.__len__()):
                del docs[del_list[i]-i]


        else:

            break

    print("Final W =", W)
    print("Final len(docs) =", len(docs))
    print("Final counter =", counter)

    return docs





def matrix_to_file(mat):
    f = open(matrix_file,'w')

    # print mat.__len__()
    # print mat[0].__len__()

    f.write('function[a] = matPlsaFull()\n\n')

    f.write('a = [\n')

    for i in range(mat.__len__()):
        print (i)
        for j in range(mat[0].__len__()):
            f.write(str(mat[i][j]))
            f.write('   ')
        f.write('\n\n')

    f.write('\n\n];\n\n\n\n\n')

    f.close()

    exit()


# @tm.task(feat, int, int)
def train(data, maxiter=500, debug=True):
    # td, idf, vocab = data
    # s_file_list= sorted(file_list)
    # print('file_list:',file_list)
    # print s_file_list
    topic_list= range(0,num_topics)
    # print topic_list
    # file_list_2 = list(file_list)
    # empty_file_list()
    #Bug update
    # df= pd.DataFrame(0,index=topic_list,columns=file_list_2)
    # Bug update over



    td, vocab = data
    # td = td[:,:-1]
    plsa = plsa1.pLSA()
    plsa.debug = debug
    plsa.logL_pic = logL_pic
    # model=plsa.train(td, num_topics, maxiter)
    model=plsa.train(td=td,Z=num_topics,maxiter=maxiter2,eps=cc,beta=beta,min_iteration=min_iteration)
    p_z_d=plsa.topic_document()
    ii=0

    # print 'model2',model[0]
    # print 'p_z_D =',p_z_d[0]
    # print('row',len(p_z_d))
    # print('column',len(p_z_d[0]))
    # print(df.shape)

    # Bug update
    # for i in df.index:
    #     jj=0
    #     for j in df.columns:
    #         df.loc[i,j]= p_z_d[ii][jj]
    #         # print 'df loc', df.loc[i,j]
    #         # print'ii jj', p_z_d[ii][jj]
    #         jj=jj+1
    #     ii=ii+1
    # Bug update over
    # print('PATH =',PATH)
    # Bug update
    # df.to_csv(PATH+'.csv')
    # Bug update over


    file_list = json_files_list
    print('"""""""""""""""""""""""""""""')
    # print(file_list)

    print('>>>>>>> In method train:', empty_docs_list)
    for edl in empty_docs_list:
        # print(file_list[edl])
        del file_list[edl]

    print('Dimenstionssssssssssssssssss')
    print("topic_list_len =",topic_list.__len__())
    print("p_z_d_len =", p_z_d.__len__())
    print("file_list_len =",file_list.__len__())
    print("p_z_d[0] =", p_z_d[0].__len__())


    topic_by_doc = open(PATH+'.csv', "w")
    for i in range(file_list.__len__()):
        topic_by_doc.write(',')
        topic_by_doc.write(file_list[i])
    topic_by_doc.write('\n')

    for i in range(p_z_d.__len__()):
        topic_by_doc.write(str(i))
        for j in range(p_z_d[0].__len__()):
            topic_by_doc.write(',')
            topic_by_doc.write(str(p_z_d[i][j]))
        topic_by_doc.write('\n')
    topic_by_doc.close()

    print('////////////////////////////')
    print(p_z_d.__len__())
    print(p_z_d[0].__len__())


    word_by_topic_conditional = open(PATH_word_by_topic_conditional+'.csv', "w")

    p_w_z_transposed_truncated = np.sort(plsa.p_w_z.transpose()[:,0:num_topics_generated])

    for i in range(p_w_z_transposed_truncated.__len__()):
        for j in range(p_w_z_transposed_truncated[0].__len__()):
            word_by_topic_conditional.write(str(p_w_z_transposed_truncated[i][num_topics_generated-j-1]))
            word_by_topic_conditional.write(',')
        word_by_topic_conditional.write('\n')
    word_by_topic_conditional.close()





    # print('docs==========================')
    #
    # for i in file_list:
    #     print(i)
    # for i in p_z_d:
    #     print(i)

    pz=model[0]
    topic_prob_file = open(PLSA_PARAMETERS_PATH + file2, "w")
    for z in pz:
        topic_prob_file.write(str(z))
        topic_prob_file.write('\n')
    topic_prob_file.close()
    return model


# @tm.task(feat, int, int)
def average_train(data, maxiter=500, debug=True):
    td, idf, vocab = data
    td = td[:,:-1]
    plsa = plsa1.pLSA()
    plsa.debug = debug
    return plsa.average_train(10)(td, 10, maxiter)

# @tm.task(feat, train, int, int)
def folding_in(data, model, maxiter=30, debug=True):
    td, idf, vocab = data
    d = td[:,-1]
    plsa = plsa1.pLSA(model)
    plsa.debug = debug
    print (plsa.folding_in(d, maxiter))

# @tm.nocache
# @tm.task(train)
def document_topics(model):
    plsa = plsa1.pLSA(model)
    for i in  plsa.document_topics():
       print (i)
       # file_txt1.write(str(i))
       # file_txt1.write('\n')
    # print plsa.document_topics()

# @tm.nocache
# @tm.task(train)
def document_cluster(model):
    plsa = plsa1.pLSA(model)
    print (plsa.document_cluster())

# @tm.nocache
# @tm.task(train)
def word_topics(model):
    plsa = plsa1.pLSA(model)
    for i in  plsa.word_topics():
       print (i)
       # file_txt1.write(str(i))
       # file_txt1.write('\n')
    # print plsa.word_topics()

# @tm.nocache
# @tm.task(train)
def word_cluster(model):
    plsa = plsa1.pLSA(model)
    print (plsa.word_cluster())

# @tm.nocache
# @tm.task(train)
def unigram_smoothing(model):
    plsa = plsa1.pLSA(model)
    print (plsa.unigram_smoothing())

# @tm.nocache
# @tm.task(feat, train, int)
def topic_labels(data, model, N=50):
    # td, idf, vocab = data
    file_txt = open(PLSA_PARAMETERS_PATH + file, "w")
    port_dict = porter_dictionary.porter_dictionary()
    port_dict.load_dict(dict_path)
    # print port_dict.dictionary
    td, vocab = data
    plsa = plsa1.pLSA(model)
    inv_vocab = inverse_vocab(vocab)
    dict_vocab=[]
    # vocab_list=[x for x in inv_vocab[1]]

    # print vocab_list
    for ind in inv_vocab:
       try:
          dict_vocab.append(port_dict.dictionary[inv_vocab[ind]][0])
       except:
             dict_vocab.append(inv_vocab[ind])
    # print len(dict_vocab)
    for i in plsa.topic_labels(dict_vocab, N):
       # print (i)
       # file_txt.write(str(i))
       for j in i:
           file_txt.write(j+', ')
       file_txt.write('\n')
    file_txt.close()
    # print plsa.topic_labels(inv_vocab, N)

# @tm.nocache
# @tm.task(feat, train)
def global_weights(data, model):
    td, idf, vocab = data
    plsa = plsa1.pLSA(model)
    print (plsa.global_weights(idf))

def main():
    # import sys

    # try:
    #     # tm.TaskManager.OUTPUT_FOLDER = "./tmp"
    #     tm.run_command(sys.argv[1:])


    # except tm.TaskManagerError, m:
    #     print >>sys.stderr, m

    print ('Training started at',time.strftime("%c"))
    start_time = time.time()
    data=feat(folder)
    model=train(data)
    print ('>>>>>>>>>>>>>Finished training')
    end_time = time.time()
    print ('Training took ' + str(round((end_time - start_time) / 60, 4)) + ' minutes.')
    topic_labels(data,model,num_topics_generated)
    end_time = time.time()
    print ('Total time ' + str(round((end_time - start_time) / 60,4)) + ' minutes.')

    # doc_topics=document_topics(model)
    # topic_labels(data,model)
    # word_cluster(model)
    # word_topics(model)
    # document_topics(model)


if __name__ == "__main__":
    main()
