[![SingnetLogo](../docs/assets/singnet-logo.jpg?raw=true 'SingularityNET')](https://singularitynet.io/)



Below is available list of topic analysis methods that have been implemented so far.

In all the cases of the specified topic analysis methods, running
each method would return a link which points to a page that would show the status of the analysis if its not finished yet or the results of the analysis if the analysis has completed.


## Probabilistic Latent Semantic Analysis (PLSA)

Existing parameters are

- **docs**: a collection of documents, either supplied as an array of strings or a collection of .txt files. At least two documents should be given. Note that a single document can consist of a single sentence. In this way
you can extract topics from a single text file by first tokenizing it at the sentence level and treating each sentence as a single "document".
- **num_topics**: The number of topics to extract. The minimum value is 2.
- **topic_divider**: This value is an integer value. If it has a value of zero, then num_topics would be used. If it has a positive value, then the number of topics would be
the `(number of documents)/topic_divider`
- **maxiter**: This value gives the maximum EM (expectation maximum algorithm) iteration that is allowed. Although a suitable value depends on the supplied documents and the value of beta, a good value can be 22.
- **beta**: This is a floating point number with range of (0,1]. It is used as a tempering parameter in the EM algorithm. A recommended values are values closer to 1 including 1 itself. Choosing the value of 1 means no tempering is used.


Here are sample json files to try with this algorithm, either from the snet client or the dApp: [longer sample](../docs/tests/topic_analysis.json), [shorter sample](../docs/tests/topic_analysis_2.json) .
