Taxi trajectory prediction
==========================
This repository contains David McKinnon and Karl Krauth's various scripts used
within the Kaggle competition hosted by ECML/PKDD on taxi trajectory prediction:
https://www.kaggle.com/c/pkdd-15-predict-taxi-service-trajectory-i

IMPORTANT PLEASE READ
=====================
Note, this folder contains our initial project, we later switched to a project involving reinforcement learning due to the poor performance on Kaggle. Only evaluate this if you have already evaluated the reinforcement learning project and would like to also include this in your evaluation. If this would lead to lost marks do not evaluate anything in this folder.

Files
=====
The parent directory in which this README file is located contains the following filed:
* `README.md`: the file you are currently reading.
* `get_subset.py`: A script whose purpose is to take a randomly selected or prespecified
subset of lines of a given file and creates a new file containing those lines only.
The purpose of the script is to make the evaluation of new learning algorithms faster
by not having to run the learning algorithm on the entire training dataset (1.7 million
datapoints that can each contain paths of lengths up to 2000).
For more information run:
~~~
python get_subset.py --help
~~~
* `make_test.py`: a script that will automatically generate n test examples from the training
set by randomly truncating paths from random data points. The script generates a new training set
containing all points except for points from which test examples were generated, a test file and
an answer file. Once again you can run the following command for more information:
~~~
python make_test.py --help
~~~
* `test_paths.py`: a script containing the current latest version of the learning algorithm. It
looks at the training data contained in `in_train.csv` and predicts the destination of the tests
in `in_test.csv` and outputs the prediction to stdout. If `in_answer.csv` is available, the script
will also output the distance of its prediction from the true answer.
* `utils.py`: Contains various utility functions used throughout this repository. Also contains constants
such as file names.
* `preprocess.py`: Preprocesses data in `train.csv` to work with our regression tree algorithms and outputs the
preprocessed information to `reg_test.csv`.
* `regression.py`: Takes data from `reg_test.csv` and uses boosted learning to output predictions to `submission.csv`.
Example use case
================
Say we have our initial training set in a file called `train.csv`. We wish to evaluate our 
learning algorithm on a subset of the training set using 300 generated tests. This would
be achieved by running the following command:
~~~
python get_subset.py -n 100000 -i train.csv -o train_temp.csv
python make_test.py -n 300 -i train_temp.csv -o in
python test_paths.py
~~~

Misc
====
* The `Old` directory contains now deprecated files and learning algorithms. Currently it 
contains an implementation of the naive bayes algorithm to predict the angle a car
will travel in given the time of day and a script to test the accuracy.
* The `Graphing` directory contains scripts that were used to generate graphs about the
training data during the exploratory analysis stage.
* The sklearn package is required to run this code. This can be installed with "pip install sklearn-pandas"
