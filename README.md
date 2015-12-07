# d-script

Writer identification using neural networks

## Project Document

<table class="confluenceTable">

<tbody>

<tr>

<th class="confluenceTh">Title</th>

<th class="confluenceTh">Last Modified Date</th>

<th class="confluenceTh">Status</th>

<th class="confluenceTh">Summary</th>

</tr>

<tr>

<td class="confluenceTd">D*SCRIPT Presentation to Steve Bowsher</td>

<td class="confluenceTd">

<div class="page" title="Page 1">

<div class="layoutArea">

<div class="column">

11/5/2015

</div>

</div>

</div>

</td>

<td class="confluenceTd">Draft</td>

<td class="confluenceTd">![](/rest/documentConversion/latest/conversion/thumbnail/21627582/3?attachmentId=21627582&version=3&mimeType=application%2Fvnd.openxmlformats-officedocument.presentationml.presentation&height=250&thumbnailStatus=200)</td>

</tr>

<tr>

<td colspan="1" class="confluenceTd">D*Script Kickoff Slides</td>

<td colspan="1" class="confluenceTd">11/5/2015</td>

<td colspan="1" class="confluenceTd">Draft</td>

<td colspan="1" class="confluenceTd">![](/rest/documentConversion/latest/conversion/thumbnail/21627581/7?attachmentId=21627581&version=7&mimeType=application%2Fvnd.openxmlformats-officedocument.presentationml.presentation&height=250&thumbnailStatus=200)</td>

</tr>

</tbody>

</table>

##   
Research

### _Preprocessing_

Image Processing R

<table style="font-size: 14.0px;line-height: 1.42857;" class="confluenceTable">

<tbody>

<tr>

<th class="confluenceTh">Title</th>

<th class="confluenceTh">Authors</th>

<th class="confluenceTh">Year</th>

<th class="confluenceTh">Summary</th>

</tr>

<tr>

<td class="confluenceTd">Colin Priest</td>

<td class="confluenceTd">2015</td>

</tr>

</tbody>

</table>

### _**Deep Learning Techniques**_

<table style="line-height: 1.42857;" class="confluenceTable">

<tbody>

<tr>

<th class="confluenceTh">Title</th>

<th class="confluenceTh">Authors</th>

<th class="confluenceTh">Year</th>

<th class="confluenceTh">Summary</th>

</tr>

<tr>

<td class="confluenceTd">[Writer Identification and Retrieval using a Convolutional Neural Network](http://www.caa.tuwien.ac.at/cvl/wp-content/uploads/2014/12/fiel-caip2015.pdf)</td>

<td class="confluenceTd">

<div class="page" title="Page 1">

<div class="layoutArea">

<div class="column">

Stefan Fiel and Robert Sablatnig

</div>

</div>

</div>

</td>

<td class="confluenceTd">2015</td>

</tr>

<tr>

<td class="confluenceTd">[Offline Writer Identification Using Convolutional Neural Network Activation Features](https://slack-files.com/files-pri-safe/T042F3W8U-F0DS51RDE/writer_ident.pdf?c=1449086005-8059ae6211d9dec87a6cede1af21db42a6d0908a)</td>

<td class="confluenceTd">Vincent Christlein, David Bernecker, Andreas Maier, and Elli Angelopoulou</td>

<td class="confluenceTd">2015</td>

</tr>

<tr>

<td colspan="1" class="confluenceTd">

[Feature extraction with convolutional neural networks for handwritten word recognition](/download/attachments/21627490/a.pdf?version=1&modificationDate=1449095408463&api=v2)

</td>

<td colspan="1" class="confluenceTd">Theodore Bluche, Hermann Ney, and Christopher Kermorvant</td>

<td colspan="1" class="confluenceTd">2013</td>

</tr>

<tr>

<td colspan="1" class="confluenceTd">[Offline Handwriting Recognition with Multidimensional Recurrent Neural Networks](http://people.idsia.ch/~juergen/nips2009.pdf)</td>

<td colspan="1" class="confluenceTd">Alex Graves and Jurgen Schmidhuber</td>

<td colspan="1" class="confluenceTd">2009</td>

</tr>

</tbody>

</table>

### _**Non-Deep Learning Techniques**_

<table class="confluenceTable">

<tbody>

<tr>

<th class="confluenceTh">Title</th>

<th class="confluenceTh">Authors</th>

<th class="confluenceTh">Year</th>

<th class="confluenceTh">Summary</th>

</tr>

<tr>

<td class="confluenceTd">[Classification of Handwritten Documents: Writer Recognition](http://www.math-info.univ-paris5.fr/~vincent/siten/Publications/theses/pdf/Siddiqi.pdf)</td>

<td class="confluenceTd">Imran Siddiqi</td>

<td class="confluenceTd">2009</td>

</tr>

<tr>

<td class="confluenceTd"><span>Text-Independent Writer Identification and Verification on Offline Arabic</span></td>

<td class="confluenceTd">M. Balacu</td>

<td class="confluenceTd">2007</td>

</tr>

</tbody>

</table>

## Datasets

<table class="confluenceTable">

<tbody>

<tr>

<th class="confluenceTh">Name</th>

<th class="confluenceTh">Link</th>

<th colspan="1" class="confluenceTh">Language</th>

<th class="confluenceTh">Info</th>

<th colspan="1" class="confluenceTh">Usage</th>

</tr>

<tr>

<td class="confluenceTd">IAM Dataset</td>

<td class="confluenceTd">[IAM Dataset](http://www.iam.unibe.ch/fki/databases/iam-handwriting-database)</td>

<td colspan="1" class="confluenceTd">English</td>

<td class="confluenceTd">

The IAM Handwriting Database 3.0 is structured as follows:

*   657 writers contributed samples of their handwriting
*   1'539 pages of scanned text
*   5'685 isolated and labeled sentences
*   13'353 isolated and labeled text lines
*   115'320 isolated and labeled words

</td>

<td colspan="1" class="confluenceTd"><span style="color: rgb(0,0,0);">This database may be used for non-commercial research purpose only.</span></td>

</tr>

<tr>

<td class="confluenceTd">CVL Dataset</td>

<td class="confluenceTd">[CVL Dataset](https://www.caa.tuwien.ac.at/cvl/research/cvl-databases/an-off-line-database-for-writer-retrieval-writer-identification-and-word-spotting/)</td>

<td colspan="1" class="confluenceTd">English + German</td>

<td class="confluenceTd">

7 Texts (1 German, 6 English)

27 Authors - 7 texts

283 Authors - 5 Text

300 DPI color image for each

</td>

<td colspan="1" class="confluenceTd">

This database may be used for non-commercial research purpose only.

</td>

</tr>

<tr>

<td colspan="1" class="confluenceTd">ICDAR 2011 Writer Identification</td>

<td colspan="1" class="confluenceTd">

[Main Contest](http://www.icdar2011.org/EN/column/column26.shtml#OLE_LINK42)

[Kaggle Download](https://www.kaggle.com/c/wic2011/data)

[Additional Contests](http://www.icdar2011.org/EN/column/column26.shtml)

</td>

<td colspan="1" class="confluenceTd">Arabic?</td>

<td colspan="1" class="confluenceTd">50 writers, 3 paragraphs each?</td>

</tr>

<tr>

<td colspan="1" class="confluenceTd">ICHFR 2012 Writer Identification Contest for Arabic Scripts</td>

<td colspan="1" class="confluenceTd">

[Contest](http://awic2012.qu.edu.qa/)

[Kaggle Data](https://www.kaggle.com/c/awic2012/data)

</td>

<td colspan="1" class="confluenceTd">Arabic</td>

<td colspan="1" class="confluenceTd">

Challenge: Identify which authors wrote which documents

</td>

</tr>

<tr>

<td colspan="1" class="confluenceTd">ICDAR 2013 Writer Identification</td>

<td colspan="1" class="confluenceTd">

[Writer ID Contest](http://users.iit.demokritos.gr/~louloud/ICDAR2013WriterIdentificationComp/resources.html)

[All ICDAR 13 Contests](http://www.icdar2013.org/program/competitions)

</td>

</tr>

<tr>

<td colspan="1" class="confluenceTd">ICDAR2015 Multi-script Writer Identification and Gender Classification Competition using "QUWI" Database</td>

<td colspan="1" class="confluenceTd">[Writer ID Contest](http://www.univ-tebessa.dz/ICDAR2015/database/database.htm)</td>

<td colspan="1" class="confluenceTd">English + Arabic</td>

<td colspan="1" class="confluenceTd">300 English, 300 Arabic (Subset of the QUWI Database)</td>

</tr>

<tr>

<td colspan="1" class="confluenceTd">NMEC Dataset</td>

<td colspan="1" class="confluenceTd">Arabic + Farsi + French</td>

<td colspan="1" class="confluenceTd">200 Authors, 1600 Authors</td>

</tr>

</tbody>

</table>

From: QUWI: An Arabic and English Handwriting Dataset for Offline Writer Identification (I'll add these to the table above as I find more info)

![](/download/attachments/21627490/Screen%20Shot%202015-11-02%20at%2010.20.39%20AM.png?version=1&modificationDate=1446488484665&api=v2 "Lab41 Potential Challenges > d*Script > Screen Shot 2015-11-02 at 10.20.39 AM.png")

## Reading Group Topics

*   Why gradients vanish in RNN's

*   Effectiveness of GRU's over LSTM's due to initialization
*   Word2Vec & negative sampling
*   Backpropagating images back for visualization
*   Generative methods in deep learning
*   Bi-directional (or in addition, 2D) LSTM's  

<table style="font-size: 14.0px;line-height: 1.42857;" class="confluenceTable">

<tbody>

<tr>

<th colspan="1" class="confluenceTh">Paper/Discussion Link</th>

<th class="confluenceTh">Presenter</th>

<th colspan="1" class="confluenceTh">Summary</th>

<th class="confluenceTh">Date</th>

</tr>

<tr>

<td colspan="1" class="confluenceTd">

[Batch Normalization:  
Accelerating Deep Network Training  
by Reducing Internal Covariate Shift](http://arxiv.org/pdf/1502.03167.pdf)

</td>

<td class="confluenceTd">Karl</td>

<td colspan="1" class="confluenceTd">

*   What's Covariate Shift?
*   What's Internal Covariate Shift & How to Reduce?
*   Normalization with Mini-Batch Statistics
*   How do we train & infer with batch-normalized networks?
*   Convolution with batch-normalized networks
*   Why does batch-normalization enable higher learning rates?

</td>

<td class="confluenceTd">12/1/2015</td>

</tr>

<tr>

<td colspan="1" class="confluenceTd">What's New at NIPS?</td>

<td class="confluenceTd">Pat</td>

<td class="confluenceTd">12/16</td>

</tr>

<tr>

<td colspan="1" class="confluenceTd">12/23</td>

</tr>

<tr>

<td colspan="1" class="confluenceTd">12/30</td>

</tr>

<tr>

<td colspan="1" class="confluenceTd">1/6</td>

</tr>

<tr>

<td colspan="1" class="confluenceTd">1/13</td>

</tr>

<tr>

<td colspan="1" class="confluenceTd">1/20</td>

</tr>

<tr>

<td colspan="1" class="confluenceTd">1/27</td>

</tr>

<tr>

<td colspan="1" class="confluenceTd">2/3</td>

</tr>

<tr>

<td colspan="1" class="confluenceTd">2/10</td>

</tr>

<tr>

<td colspan="1" class="confluenceTd">2/17</td>

</tr>

<tr>

<td colspan="1" class="confluenceTd">2/24</td>

</tr>

<tr>

<td colspan="1" class="confluenceTd">3/2</td>

</tr>

<tr>

<td colspan="1" class="confluenceTd">3/9</td>

</tr>

<tr>

<td colspan="1" class="confluenceTd">3/16</td>

</tr>

<tr>

<td colspan="1" class="confluenceTd">3/23</td>

</tr>

<tr>

<td colspan="1" class="confluenceTd">3/30</td>

</tr>

</tbody>

</table>

## Convolutional Network Architectures Tried

<table style="line-height: 1.42857;" class="confluenceTable">

<tbody>

<tr>

<th colspan="1" class="confluenceTh">Run Name</th>

<th class="confluenceTh">Data Information</th>

<th class="confluenceTh">Conv Layers</th>

<th class="confluenceTh">Model Information</th>

<th class="confluenceTh">Optimization</th>

<th colspan="1" class="confluenceTh">

Stopping Point

</th>

<th colspan="1" class="confluenceTh">Accuracy</th>

<th class="confluenceTh">Visualizations</th>

</tr>

<tr>

<td colspan="1" class="confluenceTd">Small ConvNet</td>

<td class="confluenceTd">

5 Authors,

1312/329 Train/Val Split

120x120 Random Shards in Line

/work/iam-data/output_shingles_sample.pkl

</td>

<td class="confluenceTd">

<span style="line-height: 1.42857;">Conv-10x12x12, ReLU</span>

<span style="line-height: 1.42857;">Conv-7x6x6, ReLU, MaxPool-2x2, DO-0.25</span>

<span style="line-height: 1.42857;"><span>FC-10, ReLU, DO-0.5</span></span>

FC-5-Softmax

</td>

<td class="confluenceTd">[conv2layer.hd5](/download/attachments/21627490/authors_40_forms_per_author_15_epoch_2550.hdf5.hdf5?version=1&modificationDate=1448465560191&api=v2)</td>

<td class="confluenceTd">

SGD, Rate 0.1

Momentum 0.9

Nesterov

</td>

<td colspan="1" class="confluenceTd">

Epoch 122

Loss = 0.421

</td>

<td colspan="1" class="confluenceTd">

Train: 0.73

Validate: 0.71

</td>

<td class="confluenceTd">

Original Data: ![](/download/attachments/21627490/image2015-11-23%209%3A40%3A6.png?version=1&modificationDate=1448300406544&api=v2 "Lab41 Potential Challenges > d*Script > image2015-11-23 9:40:6.png")

Layer 1: ![](/download/attachments/21627490/Screen%20Shot%202015-11-20%20at%204.58.43%20PM.png?version=1&modificationDate=1448067580777&api=v2 "Lab41 Potential Challenges > d*Script > Screen Shot 2015-11-20 at 4.58.43 PM.png")

</td>

</tr>

<tr>

<td colspan="1" class="confluenceTd">Early Tests</td>

<td class="confluenceTd">

40 Authors,

.7/.2/.1 Train/Test/Val Split

120x120 Random Shards in line (generated on the fly)

</td>

<td class="confluenceTd">

<span class="s1">Conv-48x12x12, ReLU</span>

<span class="s1">Conv-48x6x6, ReLU, MaxPool-2x2, DO-0.25</span>

<span class="s1">Conv-128x6x6, ReLU, MaxPool-2x2</span>

<span class="s1">Conv-128x3x3, ReLU, MaxPool-2x2, DO-0.5</span>

<span class="s1">FC-128, ReLU, DO-0.5</span>

<span class="s1">FC-40-Softmax</span>

</td>

<td class="confluenceTd">

[model_hdf5](/download/attachments/21627490/authors_40_forms_per_author_15_epoch_2550.hdf5.hdf5?version=1&modificationDate=1448465560191&api=v2)

</td>

<td class="confluenceTd">

SGD, Rate 0.1

Momentum 0.9

Nesterov

</td>

<td colspan="1" class="confluenceTd">

Epoch 2550

Loss =

<span>0.9551</span>

</td>

<td colspan="1" class="confluenceTd">

Train: <span>0.6944</span>

Validate: <span>0.7391</span>

</td>

<td class="confluenceTd">

Heatmaps for conv4 layer:

![](/download/attachments/21627490/image2015-12-1%209%3A1%3A32.png?version=1&modificationDate=1448989292314&api=v2 "Lab41 Potential Challenges > d*Script > image2015-12-1 9:1:32.png")

![](/download/attachments/21627490/image2015-12-1%209%3A1%3A58.png?version=1&modificationDate=1448989318172&api=v2 "Lab41 Potential Challenges > d*Script > image2015-12-1 9:1:58.png")![](/download/attachments/21627490/image2015-12-1%209%3A2%3A15.png?version=1&modificationDate=1448989334997&api=v2 "Lab41 Potential Challenges > d*Script > image2015-12-1 9:2:15.png")![](/download/attachments/21627490/image2015-12-1%209%3A2%3A29.png?version=1&modificationDate=1448989349647&api=v2 "Lab41 Potential Challenges > d*Script > image2015-12-1 9:2:29.png")![](/download/attachments/21627490/image2015-12-1%209%3A2%3A45.png?version=1&modificationDate=1448989364963&api=v2 "Lab41 Potential Challenges > d*Script > image2015-12-1 9:2:45.png")![](/download/attachments/21627490/image2015-12-1%209%3A2%3A59.png?version=1&modificationDate=1448989378936&api=v2 "Lab41 Potential Challenges > d*Script > image2015-12-1 9:2:59.png")

Top 5 Activations at highest layer.

</td>

</tr>

<tr>

<td class="confluenceTd">

40 Authors,

.7/.2/.1 Train/Test/Val Split

60x120 Random Shards in line (generated on the fly)

</td>

<td class="confluenceTd">

<span class="s1">Conv-48x12x12, ReLU</span>

<span class="s1">Conv-48x6x6, ReLU, MaxPool-2x2, DO-0.25</span>

<span class="s1">Conv-128x6x6, ReLU, MaxPool-2x2</span>

<span class="s1">Conv-128x3x3, ReLU, MaxPool-2x2, DO-0.5</span>

<span class="s1">FC-128, ReLU, DO-0.5</span>

<span class="s1">FC-40-Softmax</span>

</td>

<td class="confluenceTd">

SGD, Rate 0.1

Momentum 0.9

Nesterov

</td>

</tr>

<tr>

<td colspan="1" class="confluenceTd">Basic Recurrent Network</td>

<td class="confluenceTd">40 Authors</td>

<td class="confluenceTd">

1.  Conv-48x12x12) + Relu + MaxPool (2,2)
2.  Conv-48x6x6 + Relu + MaxPool (2,2)
3.  Conv->1D (48, 6, 35) + Rel
4.  Squeeze

</td>

</tr>

<tr>

<td colspan="1" class="confluenceTd">Large Scale Recurrent Network</td>

<td colspan="1" class="confluenceTd">40 Authors</td>

</tr>

</tbody>

</table>

## TPS Reports

<table class="confluenceTable">

<tbody>

<tr>

<td class="confluenceTd">Date</td>

<td colspan="1" class="confluenceTd">Document</td>

<td colspan="1" class="confluenceTd">Summary - Data</td>

<td colspan="1" class="confluenceTd">Software and Algorithms</td>

<td colspan="1" class="confluenceTd">Visualization / UI</td>

</tr>

<tr>

<td colspan="1" class="confluenceTd">11/23/2015</td>

<td colspan="1" class="confluenceTd">![](/rest/documentConversion/latest/conversion/thumbnail/21628003/1?attachmentId=21628003&version=1&mimeType=application%2Fvnd.openxmlformats-officedocument.wordprocessingml.document&height=150&thumbnailStatus=200)</td>

<td colspan="1" class="confluenceTd">

*   Sharding into lines
*   Obtain from NMEC

</td>

<td colspan="1" class="confluenceTd">

1.  Small-scale recurrent neural network

</td>

<td colspan="1" class="confluenceTd">

*   <span>Visualization</span>
    *   Convolutional 1st Layer
    *   Heatmap for convolutional
    *   Top 5 results per single neuron

</td>

</tr>

<tr>

<td colspan="1" class="confluenceTd">11/30/2015</td>

<td colspan="1" class="confluenceTd">![](/rest/documentConversion/latest/conversion/thumbnail/21628122/1?attachmentId=21628122&version=1&mimeType=application%2Fvnd.openxmlformats-officedocument.wordprocessingml.document&height=150&thumbnailStatus=200)</td>

<td colspan="1" class="confluenceTd">

*   Shard into document
*   Begin work on ICDAR 2015

</td>

<td colspan="1" class="confluenceTd">

1.  Large scale recurrent neural network
2.  Convolutional network in Theano

</td>

<td colspan="1" class="confluenceTd">

*   Lindsay to discuss with Nancy and John Mastarone

</td>

</tr>

<tr>

<td colspan="1" class="confluenceTd">

12/6/2015

</td>

<td colspan="1" class="confluenceTd">

*   Data preprocessing
*   Data augmentation
*   Document level CNN

</td>

</tr>

</tbody>

</table>
