# Tested on python3.6

import logging
import os
import pathlib
import json

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


def test_plsa():
    channel = grpc.insecure_channel('localhost:5000')
    stub = topic_analysis_pb2_grpc.TopicAnalysisStub(channel)


    plsa_request = topic_analysis_pb2.PLSARequest(docs=sample_data(),num_topics=2,maxiter=22,beta=1)

    resp = stub.PLSA(plsa_request)


    print(resp.status)
    print(resp.message)
    print(resp.topics)




if __name__ == '__main__':

    test_plsa()


