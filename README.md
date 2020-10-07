# RLPoker
Code Used for APMA Seminar Project: Reinforcement Learning HUNL Poker
Alex Paskov, Alan Zhang, William Shamma

Note, no data files are included in this repo, as Github does not allow us to store the large (>20GB) data matrices and card mapping files.

# File Description
In the code directory, there are 2 .py files and 3 folders. The webpageInteract.py file was used to play against the online poker bot (as a benchmark). The RPSDemo.py file is in preparation for the presentation; this is one of the tech nugget demos we will do, in which we show the RL algorithm in action and use data vizualization to show its behavior.

As for the 3 folders:

# Training
This contains the code we used to train the Neural Net and Decision Trees (Optimal, CART, etc.), in the trainModel.py, trainNN.py, and ipynb.jl (incase Julia online notebook is not installed, a screenshot of the Julia code is provided). The rest of the files are short, data manipulation files or files used to parallelize data manipulation using Mac Terminal; for instance, removeDups.py removes data duplicates in our data matrices, to avoided over-weighed training.

# Result Gen
This contains the main code to run our poker bot, based off of several data files and traing NNs or Trees. In particular, pysocket.py connects our bot to an online server (via hostname and port) to play poker with the dealer executable. All of the C programs in this folder are take from the open-source ACPC Protocol repository, which provides an easy-to-use Poker server for playing with user-created bots.

# MainProcessing
This contains the central code for the first 2 parts of the project: Creating a Poker Hand to Interpretable Feature mapping, and running the CFR Reinforcement Learning Algorithm. All of the cpp and py files with Hand or Card in their names were used to process poker equity values and translate them into probability distributions, ultimately used for the model features. Note, we had to do one part in cpp, because python was too slow (cpp resulted in a 140x speedup, which was exciting!). As for CFR, our original CFR python file is in a AWS Zip, and would be costly and time-consuming to recover. As such, we provided the Example code our CFR python file is based on (they are mostly identical, other than file parameter specifications in the code). We must also mention that this code comes from OpenSpiel, which is DeepMind's open-source Reinforcement Learning repository to aid in RL research; they implemented CFR in C, so that it runs extremely fast (at least relative to Python). Their object-oriented setup also makes for a smooth experience running the algorithm on more advanced games (like HUNL Poker).













