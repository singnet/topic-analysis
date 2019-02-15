# Tested on python3.6


import unittest
import grpc

import json
import time

from service_spec import topic_analysis_pb2
from service_spec import topic_analysis_pb2_grpc

import topic_analysis_grpc
import analysis_results

sleep_time_secs = 10 # This is to allow for topic models to be generated before unit testing occurs in the following code

class TestTopicAnalysisGrpc(unittest.TestCase):


    def setUp(self):

        self.app = analysis_results.app.test_client()
        self.docs = []

        sample_doc = 'docs/tests/test_doc.txt'
        with open(sample_doc,'r') as f:
            self.docs = f.read().splitlines()

        self.docs = list(filter(lambda a: a != '', self.docs))

        channel = grpc.insecure_channel('localhost:5000')
        self.stub = topic_analysis_pb2_grpc.TopicAnalysisStub(channel)

        self.server = topic_analysis_grpc.serve_test()
        self.server.start()

    def tearDown(self):
        self.server.stop(0)
        print('Server stopped')

    def test_response_format_grpc(self):

        plsa_request = topic_analysis_pb2.PLSARequest(docs=self.docs, num_topics=2, maxiter=22, beta=1)

        resp = self.stub.PLSA(plsa_request)

        print('////////////// Sleeping till topic analysis finishes')
        time.sleep(sleep_time_secs)
        print('\\\\\\\\\\\\\\\\\\\\\\\\\\\\  Wide awake now')

        print(resp)

        self.assertEqual([resp.status,resp.message],[True,'success'])

        resp2 = self.app.get('/topic-analysis/api/v1.0/results?handle='+resp.handle)
        resp2_data = json.loads(resp2.get_data(as_text=True))
        print(';;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;')

        self.assertEqual(resp2_data['status'],'Topic analysis finished.')
        self.assertGreater(resp2_data['total running time in minutes'],0.0)
        self.assertEqual(resp2_data['docs_list'], [str(i) for i in range(0,44)])
        self.assertEqual(len(resp2_data['topics']),2)
        self.assertIsInstance(resp2_data['topics'][0],str)
        self.assertIsInstance(resp2_data['topics'][1],str)
        self.assertEqual(len(resp2_data['topicByDocMatirx']),2)
        self.assertEqual(len(resp2_data['topicByDocMatirx'][0]),44)
        self.assertAlmostEqual(sum(sum(resp2_data['topicByDocMatirx'],[])),1.0,delta=0.1)
        print('sum of p(z,d)=',sum(sum(resp2_data['topicByDocMatirx'],[])))
        self.assertAlmostEqual(resp2_data['topicProbabilities'][0]+ resp2_data['topicProbabilities'][1],1.0,delta=0.1)
        self.assertEqual(len(resp2_data['wordByTopicConditional']), 2)
        self.assertEqual(len(resp2_data['wordByTopicConditional'][0]), 300)
        self.assertAlmostEqual(sum(sum(resp2_data['wordByTopicConditional'], [])), 1.0, delta=0.1)
        print('sum of p(w|z)=',sum(sum(resp2_data['wordByTopicConditional'],[])))
        self.assertEqual(len(resp2_data['logLikelihoods']),23)
        for i in range(0,23):
            self.assertLess(resp2_data['logLikelihoods'][i],0)














__end__ = '__end__'

if __name__ == '__main__':
    unittest.main()