# Tested on python3.6

import logging
import os
import pathlib
import json
import csv
import numpy as np

import grpc

from service_spec import topic_analysis_pb2, topic_analysis_pb2_grpc

import subprocess




def sample_data():

    path = str(pathlib.Path(os.path.abspath('')).parents[0])+'/appData/misc/extracted.json'

    docs = []

    with open(path, "r") as read_file:
        fileList = json.load(read_file)

    for k in fileList:
        docs.append(fileList[k])

    return docs

def sample_data_2():

    path = str(pathlib.Path(os.path.abspath('')).parents[0])+'/topic-analysis/docs/tests/test_doc_2.txt'

    docs = []

    with open(path, "r") as read_file:
        text = read_file.read().splitlines()

    for k in text:
        if k != "":
            docs.append(k)

    return docs

def csv_reader():

    path = str(pathlib.Path(os.path.abspath('')).parents[0]) + '/appData/misc/topic-by-doc-matirx.csv'

    resp = []


    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        docs_list = next(csv_reader)

        print(docs_list[1:])

        for row in csv_reader:
            print('^^^^^^^^^^^^^^^^^^^^^^^^^^')
            print(len(row))
            # print(row[1:])
            resp.append(list((np.array(row[1:])).astype(np.float)))

    print('`````````````````````````````````')
    print(resp)




def try_plsa():
    channel = grpc.insecure_channel('localhost:5001')
    # channel = grpc.insecure_channel('172.17.0.75:5001')
    stub = topic_analysis_pb2_grpc.TopicAnalysisStub(channel)


    plsa_request = topic_analysis_pb2.PLSARequest(docs=sample_data(),num_topics=2,maxiter=22,beta=1)

    resp = stub.PLSA(plsa_request)


    print(resp.status)
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    print(resp.message)
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    print(resp.handle)


def try_plsa_2():
    channel = grpc.insecure_channel('localhost:5000')
    # channel = grpc.insecure_channel('172.17.1.53:5001')
    # channel = grpc.insecure_channel('172.17.0.75:5001')
    stub = topic_analysis_pb2_grpc.TopicAnalysisStub(channel)


    plsa_request = topic_analysis_pb2.PLSARequest(docs=sample_data_2(),num_topics=2,maxiter=22,beta=1)

    resp = stub.PLSA(plsa_request)


    print(resp.status)
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    print(resp.message)
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    print(resp.handle)






if __name__ == '__main__':

    # try_plsa()
    # print(sample_data_2())
    try_plsa_2()
    # csv_reader()


