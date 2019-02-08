# Tested on python3.6

import grpc
from concurrent import futures
import time
import logging
import sys
import pathlib
import os


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
                lines = f.readlines()


            resp = topic_analysis_pb2.PLSAResponse(status=True,message='success',topics=lines)



        #         resp = network_analytics_bipartite_pb2.BipartiteGraphResponse(status=ret[0], message=ret[1], output=graph_resp)
        #
        #
        #     print('status:',resp.status)
        #     print('message:',resp.message)
        #     print('Waiting for next call on port 5000.')

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













