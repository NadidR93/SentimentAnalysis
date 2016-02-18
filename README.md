# SentimentAnalysis

This project determines the accuracy of our NaiveBayes algorithm and analyze a person's review. We assume an independent probability of each of these reviews and filtered words or characters (such as "the", "a", "there", "!", or whitespace). The way our Python algorithm functions is that we give a set of positive and negative training reviews, and then we test it on a set of positive and negative test reviews. From there, we get an accuracy of our Sentiment Analysis algorithm based on the correct classification of our test data set.

The accuracy of our test data set is around 66 - 68 %

We have the respository set up using IMDb's data points available online: http://ai.stanford.edu/~amaas/data/sentiment/


# How to run SentimentAnalysis

1. In your terminal, go to the directory containing SentimentAnalysis.py

2. Enter this line: ~$ python SentimentAnalysis.py <train positive reviews> <train negative reviews> <test positive reviews> <test negative reviews>. For the 4 brackets, locate the directory containing the text files for the appropiate argument.

3. By this point, the Sentiment Analysis code should run.


# What if we want to enter our own reviews?

Its definitely possible entering your own reviews, around line 205 within SentimentAnalysis.py you can enter your own review in there and check out the accuracy of our algorithm. Appropiately enter a review that either falls under a positive review or a negative review list.
