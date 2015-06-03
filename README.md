Taxi trajectory prediction
==========================
This repository contains David McKinnon and Karl Krauth's various scripts used
within the Kaggle competition hosted by ECML/PKDD on taxi trajectory prediction:
https://www.kaggle.com/c/pkdd-15-predict-taxi-service-trajectory-i

Files
=====
The parent directory in which this README file is located contains the following filed:
* README: the file you are currently reading.
* get_subset.py: A script whose purpose is to take a randomly selected or prespecified
subset of lines of a given file and creates a new file containing those lines only.
The purpose of the script is to make the evaluation of new learning algorithms faster
by not having to run the learning algorithm on the entire training dataset (1.7 million
datapoints that can each contain paths of lengths up to 2000).
For more information run:
~~~
python get_subset.py --help
~~~ 
