# Tested on python3.6

import grpc
from concurrent import futures
import time
import logging
import sys
import pathlib
import os
import csv
import numpy as np


SLEEP_TIME = 86400 # One day


sys.path.append(str(pathlib.Path(os.path.abspath('')).parents[0])+'/topic-analysis/plsa-service/plsa')
sys.path.append(str(pathlib.Path(os.path.abspath('')).parents[0])+'/topic-analysis/plsa-service/preprocessing')

print(sys.path)

# import example_plsa as pplsa
# import plsa as plsa1
# import cleansing as pclean
#
#
# import random
# import json
# import datetime
import plsa_wrapper

from service_spec import topic_analysis_pb2
from service_spec import topic_analysis_pb2_grpc



class TopicAnalysis(topic_analysis_pb2_grpc.TopicAnalysisServicer):

    def PLSA(self,request,context):

        print('>>>>>>>>>>>>>>In endpoint plsa')
        print(time.strftime("%c"))


        docs = request.docs
        num_topics = request.num_topics
        topic_divider = request.topic_divider
        maxiter = request.maxiter
        beta = request.beta


        param_error = False
        message = ''

        if len(docs) < 2:
            message = 'Length of docs should be at least two'
            param_error =True

        if topic_divider < 0:
            param_error = True
            message = 'topic_divider parameter can not be a negative nubmer'

        if topic_divider != 0 and num_topics < 2:
            param_error = True
            message = 'Number of topics should be at least two'

        if maxiter < 0:
            param_error = True
            message = 'maxiter should be greater than zero'

        if beta < 0 or beta > 1:
            param_error = True
            message = 'beta should have value of (0,1]'


        if param_error:
            return topic_analysis_pb2.PLSAResponse(status=False, message=message)




        try:

            s = plsa_wrapper.PLSA_wrapper(docs)
            s.write_to_json()
            s.generate_topics_json()

            with open(s.PLSA_PARAMETERS_PATH+'plsa_topics.txt','r') as f:
                topics = f.read().splitlines()

            topic_by_doc = []
            word_by_topic_conditional = []
            logLikelihoods = []
            docs_list = []

            with open(s.PLSA_PARAMETERS_PATH+'topic-by-doc-matirx.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')

                docs_list = next(csv_reader)[1:]

                for row in csv_reader:
                    topic_by_doc.append(topic_analysis_pb2.FloatRow(doubleValue=list((np.array(row[1:])).astype(np.float))))


            with open(s.PLSA_PARAMETERS_PATH+'topic_probability_pz','r') as f:
                topic_probabilities = f.read().splitlines()

                topic_probabilities = list((np.array(topic_probabilities)).astype(np.float))


            with open(s.PLSA_PARAMETERS_PATH+'word_by_topic_conditional.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')

                for row in csv_reader:
                    word_by_topic_conditional.append(topic_analysis_pb2.FloatRow(doubleValue=list((np.array(row[:-1])).astype(np.float))))

            with open(s.PLSA_PARAMETERS_PATH+'logL.txt','r') as f:
                logLikelihoods = f.read().splitlines()

                logLikelihoods = list((np.array(logLikelihoods)).astype(np.float))


            resp = topic_analysis_pb2.PLSAResponse(status=True,message='success',docs_list=docs_list,topics=topics,topicByDocMatirx=topic_by_doc,topicProbabilities=topic_probabilities,wordByTopicConditional=word_by_topic_conditional,logLikelihoods=logLikelihoods)




            print('status:',resp.status)
            print('message:',resp.message)
            print('Waiting for next call on port 5000.')

            return resp


        except Exception as e:

            logging.exception("message")

            resp = topic_analysis_pb2.PLSAResponse(status=False, message=str(e))

            print('status:', resp.status)
            print('message:', resp.message)
            print('Waiting for next call on port 5000.')

            return resp






def serve():

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    topic_analysis_pb2_grpc.add_TopicAnalysisServicer_to_server(TopicAnalysis(), server)
    print('Starting server. Listening on port 5000.')
    server.add_insecure_port('127.0.0.1:5000')
    server.start()
    try:
        while True:
            time.sleep(SLEEP_TIME)
    except KeyboardInterrupt:
        server.stop(0)






def serve_test():

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    topic_analysis_pb2_grpc.add_TopicAnalysisServicer_to_server(TopicAnalysis(), server)
    print('Starting server. Listening on port 5000.')
    server.add_insecure_port('127.0.0.1:5000')
    return server




__end__ = '__end__'



if __name__ == '__main__':


    serve()

    pass













