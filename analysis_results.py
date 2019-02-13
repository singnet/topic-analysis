# Tested on python3.6


import time
import csv
import numpy as np

import os
import sys
import pathlib
import logging

sys.path.append(str(pathlib.Path(os.path.abspath('')).parents[0])+'/topic-analysis/plsa-service/plsa')

from flask import Flask, jsonify
from flask import make_response
from flask import request
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

app = Flask(__name__)



# '/topic-analysis/api/v1.0/results'
@app.route('/topic-analysis/api/v1.0/results', methods=['GET'])
# @auth.login_required
def results():


    try:
        # Code to test exception handler for this try
        # a=1/0

        print('In generate_topics:', time.strftime("%c"))
        handle = request.args['handle']
        print("handle =", handle)

    except Exception as e:

        logging.exception("message")
        return make_response(jsonify({'Error': 'Request was not fulfilled. Please try again.', "error_msg": str(e)}),400)




    try:

        parameters_path = str(pathlib.Path(os.path.abspath('')).parents[0]) + '/appData/plsa/' + 'plsa-parameters/' + handle + '/'
        print(parameters_path)

        with open(parameters_path + 'plsa_topics.txt', 'r') as f:
            topics = f.read().splitlines()

        topic_by_doc = []
        word_by_topic_conditional = []
        logLikelihoods = []
        docs_list = []

        with open(parameters_path + 'topic-by-doc-matirx.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            docs_list = next(csv_reader)[1:]

            for row in csv_reader:
                topic_by_doc.append(list((np.array(row[1:])).astype(np.float)))

        with open(parameters_path + 'topic_probability_pz', 'r') as f:
            topic_probabilities = f.read().splitlines()

            topic_probabilities = list((np.array(topic_probabilities)).astype(np.float))

        with open(parameters_path + 'word_by_topic_conditional.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            for row in csv_reader:
                word_by_topic_conditional.append(list((np.array(row[:-1])).astype(np.float)))

        with open(parameters_path + 'logL.txt', 'r') as f:
            logLikelihoods = f.read().splitlines()

            logLikelihoods = list((np.array(logLikelihoods)).astype(np.float))

        # resp = topic_analysis_pb2.PLSAResponse(status=True, message='success', docs_list=docs_list, topics=topics,
        #                                        topicByDocMatirx=topic_by_doc, topicProbabilities=topic_probabilities,
        #                                        wordByTopicConditional=word_by_topic_conditional,
        #                                        logLikelihoods=logLikelihoods)


    except Exception as e:

        logging.exception("message")

        # NOT: This line is tested: it throws back error message correctly

        return make_response(jsonify({'Error': 'Request was not fulfilled. Please try again.', "error_msg": str(e)}), 500)







@app.errorhandler(404)
def not_found(error):
    print ('In not_found:', time.strftime("%c"))
    return make_response(jsonify({'Error': 'Not found'}), 404)





__end__ = '__end__'



if __name__ == '__main__':



    # app.run(debug=True)
    app.run(debug=False)
