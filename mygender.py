from math import sqrt
import string
import sys
import os


#Feature List
def lengthCheck(name):
    return [('length', len(name))]

def vowelsCheck(name):
    def isVowel(c):
        return c in 'aeiouy'
    return [('vowels', len(filter(isVowel, name)))]


alphabet = string.lowercase
def countLettersCheck(name):
    def count(s):
        return ('count-' + s, name.count(s))
    return map(count, alphabet)

def lastLetterCheck(name):
    def last(s):
        return ('last-'+ s, int(s == name[-1]))
    return map(last, alphabet)

def firstLetterCheck(name):
    def first(s):
        return ('first-' + s, int(s == name[0]))
    return map(first, alphabet)

#Combines All the features for generation of vectors
def combine(featureFunc1, featureFunc2):
    def com(name):
        return featureFunc1(name) + featureFunc2(name)
    return com

def combineMany(listOfFeatureFuncs):
    def com(name):
        return reduce(combine, listOfFeatureFuncs)(name)
    return com

#Standard Euclidian Distance Calculator
def getEuclideanDistance(v):
    def euclideanDistanceHelper(w):
        def squareDiff(i):
            return (v[i][1] - w[i][1])**2
        return sqrt(sum(map(squareDiff, range(len(v)))))
    return euclideanDistanceHelper


def generateTrainingVectors(featurefunc, trainfile):
    inputFile = open(trainfile, 'r')
    contents = map(lambda x: x.strip().split(), inputFile)
    inputFile.close()
    return map(lambda x: (x[1], featurefunc(x[0])), contents)


#Sort the labels by euclidian distance
def getSortedLabels(testvector, trainingVectors):
    def getItem1(item):
        return item[0]

    def getItem2(item):
        return item[1]

    distanceFromTest = getEuclideanDistance(testvector)
    featureVecs = map(getItem2, trainingVectors)
    listOfGenders = map(getItem1, trainingVectors)
    finalList = zip(listOfGenders, map(distanceFromTest, featureVecs))
    finalList2 = sorted(finalList, key=getItem2)
    return finalList2

#Manger Function
def getGenderPrediction(featurefunc, testname, trainingVectors, threshold):
    testVector = featurefunc(testname)
    sortedLabels = getSortedLabels(testVector, trainingVectors)
    searchLabels = sortedLabels[:threshold]
    def getFirst(item):
        return item[0]
    gender = map(getFirst, searchLabels)

    if gender.count('male') > gender.count('female'):
        return 'male'
    else:
        return 'female'

#Accuracy calculator
def getAccuracy(featurefunc, testfile, trainingVectors, threshold):
    inputFile = open(testfile, 'r')
    contents = map(lambda x: x.strip().split(), inputFile)
    inputFile.close()
    count = 0
    for name in contents:
        guessGender = getGenderPrediction(featurefunc, name[0], trainingVectors, threshold)
        if name[1] == guessGender:
            answer = 'CORRECT'
            count += 1
        else:
            answer = 'WRONG'
        print name[0], name[1], guessGender, answer
    return float(count)/len(contents)

def main():
    try:
        threshold = int(sys.argv[1])
        featureList = map(lambda x: eval(x), sys.argv[2:])
        combinedFeatures = combineMany(featureList)
        trainedVectors = generateTrainingVectors(combinedFeatures, 'train.txt')
        accuracy = getAccuracy(combinedFeatures, 'test.txt', trainedVectors, threshold)
        print accuracy
    except:
        print 'Arguments to this program: threshold featurefunc1 featurefunc2'


if __name__=='__main__':  # invothresholde main() when program is run
    main()
