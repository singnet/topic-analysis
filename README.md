[![SingnetLogo](docs/assets/singnet-logo.jpg?raw=true 'SingularityNET')](https://singularitynet.io/)

# Topic Analysis Services


This repository contains various [topic analysis](https://en.wikipedia.org/wiki/Topic_model) services for SingularityNET. The topic analysis methods would include:

* Latent semantic analysis (LSA)
* Probabilistic latent semantic analysis (PLSA)
* Latent Diritchlet allocation (LDA)
* LDA2vec

The services are wrapped using gRPC.

The user provides a collection of documents for topic analysis and the service would return discoverd topics. Each topic
consists of a collection of words that represent a given topic.


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