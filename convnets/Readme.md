# Convolutional Network Folder

Welcome to the convolutional networks for handwriting recognition folder. In here, there are several folders, with the descriptions as follows:

* examplenet
  - Example network. This is where you should probably start. Take a look through it. You'll learn how to ingest data.
* fielnet
   - Network based on Stefan Fiel's work
* basicnet
   - Small convolutional network based with only 5 authors to recognize
* fulldocnet
   - Convolutional network intended to shard into the entire document. Currently, the document read in is incorrect as there are no (x,y,h,w) positions specified in the forms.txt file. However, if someone were to fix it, the iterators and shingling should work in this folder.
* yonasnet
   - Yonas's base network with hooks into batch normalization
