Writer identification using neural networks

## Project Document

| Title | Last Modified Date | Status | Summary |
| D*SCRIPT Presentation to Steve Bowsher | 

<div class="page" title="Page 1">

<div class="layoutArea">

<div class="column">

11/5/2015

</div>

</div>

</div>

 | Draft | ![](/rest/documentConversion/latest/conversion/thumbnail/21627582/3?attachmentId=21627582&version=3&mimeType=application%2Fvnd.openxmlformats-officedocument.presentationml.presentation&height=250&thumbnailStatus=200) |
| D*Script Kickoff Slides | 11/5/2015 | Draft | ![](/rest/documentConversion/latest/conversion/thumbnail/21627581/7?attachmentId=21627581&version=7&mimeType=application%2Fvnd.openxmlformats-officedocument.presentationml.presentation&height=250&thumbnailStatus=200) |

## 
Research

### _Preprocessing_

Image Processing R

| Title | Authors | Year | Summary |
 Colin Priest | 2015 |

### _**Deep Learning Techniques**_

| Title | Authors | Year | Summary |
| [Writer Identification and Retrieval using a Convolutional Neural Network](http://www.caa.tuwien.ac.at/cvl/wp-content/uploads/2014/12/fiel-caip2015.pdf) | 

<div class="page" title="Page 1">

<div class="layoutArea">

<div class="column">

Stefan Fiel and Robert Sablatnig

</div>

</div>

</div>

 | 2015 |
| [Offline Writer Identification Using Convolutional Neural Network Activation Features](https://slack-files.com/files-pri-safe/T042F3W8U-F0DS51RDE/writer_ident.pdf?c=1449086005-8059ae6211d9dec87a6cede1af21db42a6d0908a) | Vincent Christlein, David Bernecker, Andreas Maier, and Elli Angelopoulou | 2015 |
| 

[Feature extraction with convolutional neural networks for handwritten word recognition](/download/attachments/21627490/a.pdf?version=1&modificationDate=1449095408463&api=v2)

 | Theodore Bluche, Hermann Ney, and Christopher Kermorvant | 2013 |
| [Offline Handwriting Recognition with Multidimensional Recurrent Neural Networks](http://people.idsia.ch/~juergen/nips2009.pdf) | Alex Graves and Jurgen Schmidhuber | 2009 |

### _**Non-Deep Learning Techniques**_

| Title | Authors | Year | Summary |
| [Classification of Handwritten Documents: Writer Recognition](http://www.math-info.univ-paris5.fr/~vincent/siten/Publications/theses/pdf/Siddiqi.pdf) | Imran Siddiqi | 2009 |
| <span>Text-Independent Writer Identification and Verification on Offline Arabic</span> | M. Balacu | 2007 |

## Datasets

| Name | Link | Language | Info | Usage |
| IAM Dataset | [IAM Dataset](http://www.iam.unibe.ch/fki/databases/iam-handwriting-database) | English | 

The IAM Handwriting Database 3.0 is structured as follows:

*   657 writers contributed samples of their handwriting
*   1'539 pages of scanned text
*   5'685 isolated and labeled sentences
*   13'353 isolated and labeled text lines
*   115'320 isolated and labeled words

 | <span style="color: rgb(0,0,0);">This database may be used for non-commercial research purpose only.</span> |
| CVL Dataset | [CVL Dataset](https://www.caa.tuwien.ac.at/cvl/research/cvl-databases/an-off-line-database-for-writer-retrieval-writer-identification-and-word-spotting/) | English + German | 

7 Texts (1 German, 6 English)

27 Authors - 7 texts

283 Authors - 5 Text

300 DPI color image for each

 | 

This database may be used for non-commercial research purpose only.

 |
| ICDAR 2011 Writer Identification | 

[Main Contest](http://www.icdar2011.org/EN/column/column26.shtml#OLE_LINK42)

[Kaggle Download](https://www.kaggle.com/c/wic2011/data)

[Additional Contests](http://www.icdar2011.org/EN/column/column26.shtml)

 | Arabic? | 50 writers, 3 paragraphs each? |
| ICHFR 2012 Writer Identification Contest for Arabic Scripts | 

[Contest](http://awic2012.qu.edu.qa/)

[Kaggle Data](https://www.kaggle.com/c/awic2012/data)

 | Arabic | 

Challenge: Identify which authors wrote which documents

 |
| ICDAR 2013 Writer Identification | 

[Writer ID Contest](http://users.iit.demokritos.gr/~louloud/ICDAR2013WriterIdentificationComp/resources.html)

[All ICDAR 13 Contests](http://www.icdar2013.org/program/competitions)

 |
| ICDAR2015 Multi-script Writer Identification and Gender Classification Competition using "QUWI" Database | [Writer ID Contest](http://www.univ-tebessa.dz/ICDAR2015/database/database.htm) | English + Arabic | 300 English, 300 Arabic (Subset of the QUWI Database) |
| NMEC Dataset | Arabic + Farsi + French | 200 Authors, 1600 Authors |

From: QUWI: An Arabic and English Handwriting Dataset for Offline Writer Identification (I'll add these to the table above as I find more info)

![](/download/attachments/21627490/Screen%20Shot%202015-11-02%20at%2010.20.39%20AM.png?version=1&modificationDate=1446488484665&api=v2 "Lab41 Potential Challenges > d*Script > Screen Shot 2015-11-02 at 10.20.39 AM.png")

## Reading Group Topics

*   Why gradients vanish in RNN's

*   Effectiveness of GRU's over LSTM's due to initialization
*   Word2Vec & negative sampling
*   Backpropagating images back for visualization
*   Generative methods in deep learning
*   Bi-directional (or in addition, 2D) LSTM's

| Paper/Discussion Link | Presenter | Summary | Date |
| 

[Batch Normalization:
Accelerating Deep Network Training
by Reducing Internal Covariate Shift](http://arxiv.org/pdf/1502.03167.pdf)

 | Karl | 

*   What's Covariate Shift?
*   What's Internal Covariate Shift & How to Reduce?
*   Normalization with Mini-Batch Statistics
*   How do we train & infer with batch-normalized networks?
*   Convolution with batch-normalized networks
*   Why does batch-normalization enable higher learning rates?

 | 12/1/2015 |
| What's New at NIPS? | Pat | 12/16 |
 12/23 |
 12/30 |
 1/6 |
 1/13 |
 1/20 |
 1/27 |
 2/3 |
 2/10 |
 2/17 |
 2/24 |
 3/2 |
 3/9 |
 3/16 |
 3/23 |
 3/30 |

## Convolutional Network Architectures Tried

| Run Name | Data Information | Conv Layers | Model Information | Optimization | 

Stopping Point

 | Accuracy | Visualizations |
| Small ConvNet | 

5 Authors,

1312/329 Train/Val Split

120x120 Random Shards in Line

/work/iam-data/output_shingles_sample.pkl

 | 

<span style="line-height: 1.42857;">Conv-10x12x12, ReLU</span>

<span style="line-height: 1.42857;">Conv-7x6x6, ReLU, MaxPool-2x2, DO-0.25</span>

<span style="line-height: 1.42857;"><span>FC-10, ReLU, DO-0.5</span></span>

FC-5-Softmax

 | [conv2layer.hd5](/download/attachments/21627490/authors_40_forms_per_author_15_epoch_2550.hdf5.hdf5?version=1&modificationDate=1448465560191&api=v2) | 

SGD, Rate 0.1

Momentum 0.9

Nesterov

 | 

Epoch 122

Loss = 0.421

 | 

Train: 0.73

Validate: 0.71

 | 

Original Data: ![](/download/attachments/21627490/image2015-11-23%209%3A40%3A6.png?version=1&modificationDate=1448300406544&api=v2 "Lab41 Potential Challenges > d*Script > image2015-11-23 9:40:6.png")

Layer 1: ![](/download/attachments/21627490/Screen%20Shot%202015-11-20%20at%204.58.43%20PM.png?version=1&modificationDate=1448067580777&api=v2 "Lab41 Potential Challenges > d*Script > Screen Shot 2015-11-20 at 4.58.43 PM.png")

 |
| Early Tests | 

40 Authors,

.7/.2/.1 Train/Test/Val Split

120x120 Random Shards in line (generated on the fly)

 | 

<span class="s1">Conv-48x12x12, ReLU</span>

<span class="s1">Conv-48x6x6, ReLU, MaxPool-2x2, DO-0.25</span>

<span class="s1">Conv-128x6x6, ReLU, MaxPool-2x2</span>

<span class="s1">Conv-128x3x3, ReLU, MaxPool-2x2, DO-0.5</span>

<span class="s1">FC-128, ReLU, DO-0.5</span>

<span class="s1">FC-40-Softmax</span>

 | 

[model_hdf5](/download/attachments/21627490/authors_40_forms_per_author_15_epoch_2550.hdf5.hdf5?version=1&modificationDate=1448465560191&api=v2)

 | 

SGD, Rate 0.1

Momentum 0.9

Nesterov

 | 

Epoch 2550

Loss =

<span>0.9551</span>

 | 

Train: <span>0.6944</span>

Validate: <span>0.7391</span>

 | 

Heatmaps for conv4 layer:

![](/download/attachments/21627490/image2015-12-1%209%3A1%3A32.png?version=1&modificationDate=1448989292314&api=v2 "Lab41 Potential Challenges > d*Script > image2015-12-1 9:1:32.png")

![](/download/attachments/21627490/image2015-12-1%209%3A1%3A58.png?version=1&modificationDate=1448989318172&api=v2 "Lab41 Potential Challenges > d*Script > image2015-12-1 9:1:58.png")![](/download/attachments/21627490/image2015-12-1%209%3A2%3A15.png?version=1&modificationDate=1448989334997&api=v2 "Lab41 Potential Challenges > d*Script > image2015-12-1 9:2:15.png")![](/download/attachments/21627490/image2015-12-1%209%3A2%3A29.png?version=1&modificationDate=1448989349647&api=v2 "Lab41 Potential Challenges > d*Script > image2015-12-1 9:2:29.png")![](/download/attachments/21627490/image2015-12-1%209%3A2%3A45.png?version=1&modificationDate=1448989364963&api=v2 "Lab41 Potential Challenges > d*Script > image2015-12-1 9:2:45.png")![](/download/attachments/21627490/image2015-12-1%209%3A2%3A59.png?version=1&modificationDate=1448989378936&api=v2 "Lab41 Potential Challenges > d*Script > image2015-12-1 9:2:59.png")

Top 5 Activations at highest layer.

 |

40 Authors,

.7/.2/.1 Train/Test/Val Split

60x120 Random Shards in line (generated on the fly)

 | 

<span class="s1">Conv-48x12x12, ReLU</span>

<span class="s1">Conv-48x6x6, ReLU, MaxPool-2x2, DO-0.25</span>

<span class="s1">Conv-128x6x6, ReLU, MaxPool-2x2</span>

<span class="s1">Conv-128x3x3, ReLU, MaxPool-2x2, DO-0.5</span>

<span class="s1">FC-128, ReLU, DO-0.5</span>

<span class="s1">FC-40-Softmax</span>

 | 

SGD, Rate 0.1

Momentum 0.9

Nesterov

 |
| Basic Recurrent Network | 40 Authors | 

1.  Conv-48x12x12) + Relu + MaxPool (2,2)
2.  Conv-48x6x6 + Relu + MaxPool (2,2)
3.  Conv->1D (48, 6, 35) + Rel
4.  Squeeze

 |
| Large Scale Recurrent Network | 40 Authors |

## TPS Reports

| Date | Document | Summary - Data | Software and Algorithms | Visualization / UI |
| 11/23/2015 | ![](/rest/documentConversion/latest/conversion/thumbnail/21628003/1?attachmentId=21628003&version=1&mimeType=application%2Fvnd.openxmlformats-officedocument.wordprocessingml.document&height=150&thumbnailStatus=200) | 

*   Sharding into lines
*   Obtain from NMEC

 | 

1.  Small-scale recurrent neural network

 | 

*   <span>Visualization</span>
    *   Convolutional 1st Layer
    *   Heatmap for convolutional
    *   Top 5 results per single neuron

 |
| 11/30/2015 | ![](/rest/documentConversion/latest/conversion/thumbnail/21628122/1?attachmentId=21628122&version=1&mimeType=application%2Fvnd.openxmlformats-officedocument.wordprocessingml.document&height=150&thumbnailStatus=200) | 

*   Shard into document
*   Begin work on ICDAR 2015

 | 

1.  Large scale recurrent neural network
2.  Convolutional network in Theano

 | 

*   Lindsay to discuss with Nancy and John Mastarone

 |
| 

12/6/2015

 | 

*   Data preprocessing
*   Data augmentation
*   Document level CNN

 |
