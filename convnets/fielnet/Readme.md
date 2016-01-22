### Stefan Fiel's Deep Neural Network (Absent Feature Extractor)

To train, use fielnet.ipynb. This will save models

To load the net in, call fielload.ipynb.

- fielnet.ipynb - Not really Stefan Fiel's neural network, a smaller version
- fielload.ipynb - Loads the above network into memory and makes it possible to do inference
- fielnet.hdf5 - The resultant model from the above mini-model
- fielnet_verbatim.py - The real Stefan Fiel network (without the 1000 softmax layer: 657, instead)

Notes:
* No X-Validation
* Accuracy Train 79.05%
* Shard into lines at 120x120
* Shard into lines with verbatim network at 59 x 59
* Did not run with Yonas's minibatcher. Used my own custom ingest.
