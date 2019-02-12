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

sys.path.append(str(pathlib.Path(os.path.abspath('')).parents[1])+'/plsa/plsa')
sys.path.append(str(pathlib.Path(os.path.abspath('')).parents[1])+'/plsa/preprocessing')

import example_plsa as pplsa
import cleansing as pclean

class TopicAnalysis:

    def __init__(self, path,channel=''):

        self.data_path = path
        self.channel = channel
        self.root_path = str(pathlib.Path(os.path.abspath('')).parents[2]) + '/appData/plsa/'
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
        # self.unique_folder_naming

    def __del__(self):

        # Close db connections
        pass

    def read_csv(self):

        messages_list = []

        with open(self.data_path, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                messages_list.append(row)

        self.messages = messages_list



    def write_to_files_slack(self):

        self.read_csv()


        self.unique_folder_naming = str(datetime.datetime.now()).replace(':','-').replace('.','-') + '^' + str(random.randint(100000000000, 999999999999)) + self.channel + '/'
        print(self.unique_folder_naming)

        os.mkdir(self.extracted_folder+self.unique_folder_naming)

        # idx = 0

        for row in self.messages:
            if row['subtype'] == 'chat':
                file = self.extracted_folder+self.unique_folder_naming+row['id']+'.txt'
                if self.channel == '':
                    with open(file, 'w') as f:
                        f.write(row['text'])
                else:
                    if row['channel_name'] == self.channel:
                        with open(file, 'w') as f:
                            f.write(row['text'])
                    else:
                        continue

            # idx = idx + 1



    def write_to_json(self):

        self.read_csv()


        self.unique_folder_naming = str(datetime.datetime.now()).replace(':','-').replace('.','-') + '^' + str(random.randint(100000000000, 999999999999)) + self.channel + '/'
        print(self.unique_folder_naming)

        os.mkdir(self.extracted_folder+self.unique_folder_naming)

        # idx = 0
        contents_dict = {}

        file = self.extracted_folder + self.unique_folder_naming + 'extracted' + '.json'

        for row in self.messages:
            if row['subtype'] == 'chat':
                if self.channel == '':
                    contents_dict[row['id']]=row['text']
                    # with open(file, 'w') as f:
                    #     f.write(row['text'])
                else:
                    if row['channel_name'] == self.channel:
                        contents_dict[row['id']] = row['text']
                        # with open(file, 'w') as f:
                        #     f.write(row['text'])
                    else:
                        continue

            # idx = idx + 1

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
        pclean.pre_pro()

        # Train using PLSA
        pplsa.topic_divider = 0
        pplsa.num_topics = 2
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



        os.mkdir(pplsa.PLSA_PARAMETERS_PATH)

        pplsa.main()

        end_time_1 = time.time()

        print('Total training time took:',round((end_time_1 - start_time_1) / 60, 4))




    def generate_topics(self):

        start_time_1 = time.time()

        pplsa.file_parts_number=10
        pclean.file_parts_number = 10
        pclean.file_dict = self.file_dict + self.unique_folder_naming[:-1] +'_dict'
        pclean.source_texts = self.source_texts + self.unique_folder_naming + '*.txt'
        pclean.output_dir = self.output_dir + self.unique_folder_naming

        os.mkdir(pclean.output_dir)


        # Do cleansing on the data and turing it to bad-of-words model
        pclean.pre_pro()

        # Train using PLSA
        pplsa.topic_divider = 0
        pplsa.num_topics = 2
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



        os.mkdir(pplsa.PLSA_PARAMETERS_PATH)

        pplsa.main()

        end_time_1 = time.time()

        print('Total training time took:',round((end_time_1 - start_time_1) / 60, 4))






def run_plsa_slack_json():
    path_1 = str(pathlib.Path(os.path.abspath('')).parents[2]) + '/appData/misc/slack_messages.csv'
    print(path_1)
    s = TopicAnalysis(path_1,'singnet')
    s.write_to_json()
    s.generate_topics_json()



def run_plsa_slack():
    path_1 = str(pathlib.Path(os.path.abspath('')).parents[2]) + '/appData/misc/slack_messages.csv'
    print(path_1)
    s = TopicAnalysis(path_1,'singnet')
    s.write_to_files_slack()
    s.generate_topics()


def run_1():

    t = TopicAnalysis('local')


    pass


def test_preprocessing():

    root_folder = str(pathlib.Path(os.path.abspath('')).parents[1])+'/appData/plsa/test/'

    pclean.file_parts_number=10
    pplsa.file_parts_number = 10
    pclean.file_dict = root_folder + 'dict/test_dict'
    pclean.source_texts = root_folder + 'extracted/*.txt'
    pclean.output_dir = root_folder + 'cleaned/'


    # Do cleansing on the data and turing it to bad-of-words model
    pclean.pre_pro()

    # Train using PLSA
    pplsa.folder = pclean.output_dir[:-1]
    pplsa.dict_path = pclean.file_dict
    pplsa.folder = pclean.output_dir[:-1]
    pplsa.main()




def isEnglish(s):
    print(s)
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






__end__ = '__end__'


if __name__ == '__main__':

    run_plsa_slack_json()
    # run_plsa_slack()
    # run_1()
    # test_preprocessing()
    #
    # print(isEnglish('meeeee'))
    pass
