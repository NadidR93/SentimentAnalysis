#
#  CS 484 - Fall 2015
#  Authors: Reza Ahmad and Nadid Rahman
#  Movie Sentiment Analysis: Naive Bayes
#

from collections import Counter

import os
import sys

positive_reviews = []
negative_reviews = []
testset_pos = []
testset_neg = []
class_prob_pos = 0
class_prob_neg = 0
TP = 0
FP = 0
TN = 0
FN = 0


# helper function to keep track of words in each review
def prep_reviews(data, reviewtype=None):
	if reviewtype is None:
		return

	elif reviewtype is 'positive':
		positive_reviews.append((data, '+'))

	elif reviewtype is 'negative':
		negative_reviews.append((data, '-'))


def naiveBayes(posTest, negTest):
	# further scrubbing, only include words that are greater than 2 chars (positive)
	clean = []
	print '--> processing positive reviews (words)'
	for (text, review) in positive_reviews:
		cleanup = [word.lower() for word in text.split() if len(word) > 2]
		clean.append((cleanup, review))


	tmp = []
	for (txt, rev) in clean:
		tmp.extend(txt)

	# used python module Counter to calculate word counts
	pos_counts = Counter(tmp)
	print '--> processed %s positive words' % len(pos_counts)


	# further scrubbing, only include words that are greater than 2 chars (negative)
	clean = []
	print '--> processing negative reviews (words)'
	for (text, review) in negative_reviews:
		cleanup = [word.lower() for word in text.split() if len(word) > 2]
		clean.append((cleanup, review))


	tmp = []
	for (txt, rev) in clean:
		tmp.extend(txt)
	# used python module Counter to calculate word counts
	neg_counts = Counter(tmp)
	print '--> processed %s negative words' % len(neg_counts)

	# convert all counts to floats so we dont end up floats
	pos_reviews = float(len(positive_reviews))
	neg_reviews = float(len(negative_reviews))
	total_reviews = pos_reviews + neg_reviews
	

	print '--> total number of pos reviews: %s' % pos_reviews
	print '--> total number of neg reviews: %s' % neg_reviews
	print '--> total number of reviews: %s' % total_reviews

	# calculate class probabilities
	class_prob_pos = pos_reviews/total_reviews
	class_prob_neg = neg_reviews/total_reviews

	print '--> class probability pos: %s' % class_prob_pos
	print '--> class probability neg: %s' % class_prob_neg

	pos_words = len(pos_counts)
	neg_words = len(neg_counts)

	print '--> done training NaiveBayes classifier'


	# the brains of the classifier here
	def sentiment(reviews):
		global TP, TN, FN, FP
		# for each word in each review, the probability of it in:
		# - positive counts is calculated
		# - negative counts is calculated
		# TP, TN, FP, FN is kept track of
		# confusion matrix along with accuracy is printed 
		for review in reviews:

			p = 1.0
			txt_c = Counter(review.split(' '))
			pos_denom = sum(pos_counts.values()) + pos_reviews

			n = 1.0
			neg_denom = sum(neg_counts.values()) + neg_reviews
			if len(txt_c) > 120:
				pos_denom -= 1
				neg_denom -= 1
				continue

			for word in txt_c:
				if pos_counts.get(word, 0) != 0:
					p *= txt_c.get(word) * ( (pos_counts.get(word, 0) + 1) / pos_denom )

				if neg_counts.get(word, 0) != 0:
					n *= txt_c.get(word) * ( (neg_counts.get(word, 0) + 1) / neg_denom )

			p = p * class_prob_pos
			n = n * class_prob_neg


			if reviews == posTest:
				if (p > n):
					TP += 1
				else:
					FN += 1

			elif reviews == negTest:
				if (n > p):
					TN += 1
				else:
					FP += 1

	sentiment(posTest)
	sentiment(negTest)

	print('TP: %s TN: %s FP: %s FN: %s' % (TP, TN, FP, FN))
	accuracy = float(TP + TN)
	accuracy = accuracy / (TP + TN + FP + FN)
	print('Accuracy: %s' % round(accuracy * 100, 2))

def main(argv):
	# Main function takes 4 arguments trainpos trainneg testpos testneg 
	# Each argument needs to be a directory with text files containing reviews

	if len(sys.argv) != 5:
		sys.exit('Usage: %s <train positive reviews> <train negative reviews> <test positive reviews> <test negative reviews>' % sys.argv[0])

	pos = sys.argv[1]
	neg = sys.argv[2]
	testpos = sys.argv[3]
	testneg = sys.argv[4]

	# Eliminate common words and puncations that add no value
	fillers = ['<br />', '...', ';', ',', '-', '.', 'the', 'and', 'that', 'this']

	# Process positive reviews (training) and keep track of all the words
	print '--> pre-processing positive reviews'
	for root, dirs, files, in os.walk(pos, topdown=True):
		for review in files:
			filename = os.path.join(root, review)
			text = open(filename, 'r')
			text = text.read()
			for f in fillers:
				text = text.replace(f, '')

			prep_reviews(text, 'positive')
	print '--> pre-processing positive reviews [done]'

	# Process negative reviews (training) and keep track of all the words
	print '--> pre-processing negative reviews'
	for root, dirs, files, in os.walk(neg, topdown=True):
		for review in files:
			filename = os.path.join(root, review)
			text = open(filename, 'r')
			text = text.read()
			for f in fillers:
				text = text.replace(f, '')	
			prep_reviews(text, 'negative')
	print '--> pre-processing positive reviews [done]'

	# Process positive reviews (test) and keep track of each review
	for root, dirs, files, in os.walk(testpos, topdown=True):
		for review in files:
			filename = os.path.join(root, review)
			text = open(filename, 'r')
			text = text.read()
			for f in fillers:
				text = text.replace(f, '')
			testset_pos.append(text)

	# Process negative reviews (test) and keep track of each review
	for root, dirs, files, in os.walk(testneg, topdown=True):
		for review in files:
			filename = os.path.join(root, review)
			text = open(filename, 'r')
			text = text.read()
			for f in fillers:
				text = text.replace(f, '')
			testset_neg.append(text)


	# Uncomment the next 4 lines if you want to test your own case
	# Otherwise the program will classify all the test reviews
	# previews = ['it was a great movie', 'enjoyed it very much']
	# nreviews = ['bad movie bad acting', 'i didnt like it']
	# naiveBayes(previews, nreviews)
	# sys.exit(1)

	# this calls our classifier
	naiveBayes(testset_pos, testset_neg)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))