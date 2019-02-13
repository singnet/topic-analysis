__author__ = 'eyob'
# Tested on python3.6

import psutil
print('===================ram used at program start:',float(list(psutil.virtual_memory())[3])/1073741824.0,'GB')

import os
import sys
import pathlib
import csv
import random
import datetime
import time
import json
import logging

sys.path.append(str(pathlib.Path(os.path.abspath('')).parents[1])+'/plsa-service/plsa')
sys.path.append(str(pathlib.Path(os.path.abspath('')).parents[1])+'/plsa-service/preprocessing')
sys.path.append(str(pathlib.Path(os.path.abspath('')).parents[0])+'/topic-analysis/plsa-service/plsa')
sys.path.append(str(pathlib.Path(os.path.abspath('')).parents[0])+'/topic-analysis/plsa-service/preprocessing')


import example_plsa as pplsa
import cleansing as pclean

class PLSA_wrapper:

    def __init__(self, docs,local=False):

        self.docs = docs
        if not local:
            self.root_path = str(pathlib.Path(os.path.abspath('')).parents[0]) + '/appData/plsa/'
        else:
            self.root_path = str(pathlib.Path(os.path.abspath('')).parents[2]) + '/appData/plsa/'
        print('>>>>>>>>>>>>>self.root_path>>>>>>>>>>>')
        print(self.root_path)
        self.extracted_folder = self.root_path + 'extracted/'
        self.file_dict = self.root_path + 'dict/'
        self.source_texts = self.root_path + 'extracted/'
        self.output_dir = self.root_path + 'cleaned/'
        print(self.output_dir)
        self.folder = self.root_path + 'cleaned/'
        self.dict_path = self.root_path + 'dict/'
        self.plsa_parameters_path = self.root_path + 'plsa-parameters/'
        self.PLSA_PARAMETERS_PATH = ''

        # self.messages
        self.unique_folder_naming = None
        self.num_topics = None
        self.topic_divider = None
        self.max_iter = None
        self.beta = None

    def __del__(self):

        # Close db connections
        pass



    def write_to_json(self):



        # self.unique_folder_naming = str(datetime.datetime.now()).replace(':','-').replace('.','-') + '^' + str(random.randint(100000000000, 999999999999)) + '/'
        print(self.unique_folder_naming)

        os.mkdir(self.extracted_folder+self.unique_folder_naming)

        contents_dict = {}

        file = self.extracted_folder + self.unique_folder_naming + 'extracted' + '.json'

        for i in range(len(self.docs)):
            contents_dict[str(i)] = self.docs[i]

        with open(file, "w") as f:
            json.dump(contents_dict, f, indent=4)

        print("len(contents_dict):",len(contents_dict))



    def generate_topics_json(self):

        start_time_1 = time.time()

        pplsa.file_parts_number=10
        pclean.file_parts_number = 10
        pclean.file_dict = self.file_dict + self.unique_folder_naming[:-1] +'_dict'
        pclean.source_texts = self.source_texts + self.unique_folder_naming + 'extracted.json'
        pclean.output_dir = self.output_dir + self.unique_folder_naming

        os.mkdir(pclean.output_dir)


        # Do cleansing on the data and turing it to bad-of-words model

        with open(self.plsa_parameters_path + self.unique_folder_naming+'status.txt','w') as f:
            f.write('Preprocessing started.')

        pclean.pre_pro()

        with open(self.plsa_parameters_path + self.unique_folder_naming+'status.txt','w') as f:
            f.write('Preprocessing finished. Topic analysis started.')

        # Train using PLSA
        pplsa.topic_divider = self.topic_divider
        pplsa.num_topics = self.num_topics
        pplsa.maxiter2 = self.max_iter
        pplsa.beta = self.beta
        pplsa.folder = pclean.output_dir[:-1]
        pplsa.dict_path = pclean.file_dict
        pplsa.PLSA_PARAMETERS_PATH = self.plsa_parameters_path + self.unique_folder_naming
        pplsa.PATH = pplsa.PLSA_PARAMETERS_PATH + 'topic-by-doc-matirx'
        pplsa.PATH_word_by_topic_conditional = pplsa.PLSA_PARAMETERS_PATH + 'word_by_topic_conditional'
        pplsa.logL_pic = pplsa.PLSA_PARAMETERS_PATH + 'logL.png'

        # Folder paths to delete
        self.PLSA_PARAMETERS_PATH = pplsa.PLSA_PARAMETERS_PATH
        self.output_dir_stream = pclean.output_dir
        self.file_dict_stream = pclean.file_dict


        try:
            os.mkdir(pplsa.PLSA_PARAMETERS_PATH)
        except:
            print('-----------------------Folder exists-------------------------')


        pplsa.main()


        end_time_1 = time.time()

        print('Total training time took:',round((end_time_1 - start_time_1) / 60, 4))

        with open(self.plsa_parameters_path + self.unique_folder_naming+'status.txt','w') as f:
            f.write('Topic analysis finished.\n')
            f.write(str(round((end_time_1 - start_time_1) / 60, 4)))





def run_plsa():

    path = str(pathlib.Path(os.path.abspath('')).parents[2])+'/appData/misc/extracted.json'

    docs = []


    with open(path, "r") as read_file:
        fileList = json.load(read_file)

    for k in fileList:
        docs.append(fileList[k])

    s = PLSA_wrapper(docs,local=True)
    s.write_to_json()
    s.generate_topics_json()



__end__ = '__end__'


if __name__ == '__main__':

    run_plsa()

    pass
