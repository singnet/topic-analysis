[![SingnetLogo](docs/assets/singnet-logo.jpg?raw=true 'SingularityNET')](https://singularitynet.io/)

[![CircleCI](https://circleci.com/gh/singnet/topic-analysis.svg?style=svg)](https://circleci.com/gh/singnet/topic-analysis)

# Topic Analysis Services


This repository contains various [topic analysis](https://en.wikipedia.org/wiki/Topic_model) services for SingularityNET. The topic analysis methods would include:

* Latent semantic analysis (LSA)
* Probabilistic latent semantic analysis (PLSA)
* Latent Diritchlet allocation (LDA)
* LDA2vec

The services are wrapped using gRPC.

The user provides a collection of documents for topic analysis and the service would return discoverd topics. Each topic
consists of a collection of words that represent a given topic.


All services have been tested to work with python3.6.



## User Guide

Please look at the [user guide](docs/USERGUIDE.md) for a detailed spec of the services and how to use the services.



## Running the service locally

### Install preprequisites

```
pip install -r requirements.txt
```


### Setup

Run the following commands to generate gRPC classes for Python

```
python3.6 -m grpc_tools.protoc -I. --python_out=.  --grpc_python_out=. service_spec/topic_analysis.proto
```



### Running unit tests


```
python3.6 test_topic_analysis_grpc.py
```

### Usage

To start the gRPC server locally

```
python3.6 topic_analysis_grpc.py

```

Topic analysis would most likely involve running a dimensionality reduction alogrithm which would take a considerable lenght of time to complete. For this reason, running the service above would return a handle which you will need to use to query a restapi endpoint at a later time. See the user guide for details. You can start that endpoint with the command

```
python3.6 analysis_results.py
```

You can also use a suitable application server for python flask. A sample config file using gunicorn is [config.py](Docker/gunicorn/config.py).

Then, you can execute the below command to serve analysis_results.py, by executing gnunicorn in a folder containing config.py, while the configuration file confi.py has a path pointing to analysis_results.py.

```
gunicorn -c config.py analysis_results:app
```



## Resources

LSA:
 * Research paper: [Indexing by Latent Semantic Analysis](http://citeseer.ist.psu.edu/viewdoc/download?doi=10.1.1.108.8490&rep=rep1&type=pdf)
 * [Wikipedia entry](https://en.wikipedia.org/wiki/Latent_semantic_analysis)

PLSA:
 * Research aper: [Unsupervised Learning by Probabilistic Latent Semantic Analysis](http://www.cs.bham.ac.uk/~pxt/IDA/plsa.pdf)
 * [Wikipedia entry](https://en.wikipedia.org/wiki/Probabilistic_latent_semantic_analysis)

LDA:
 * Research paper: [Latent Dirichlet Allocation](http://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf)
 * [Wikipedia entry](https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation)

LDA2vec:
 * Research paper: [Mixing Dirichlet Topic Models and Word Embeddings to Make lda2vec](https://arxiv.org/abs/1605.02019)


## Contributors

### Authors

* Eyob Yirdaw

### Maintainers

* Eyob Yirdaw