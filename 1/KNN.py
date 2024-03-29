from numpy import *
import operator
import matplotlib
import matplotlib.pyplot as plt
from os import listdir

def classify0(inX, dataSet, lables, K):
	dataSetSize = dataSet.shape[0]
	diffMat = tile(inX, (dataSetSize,1)) - dataSet
	sqDiffMat = diffMat ** 2
	sqDistances = sqDiffMat.sum(axis = 1)
	distances = sqDistances ** 0.5
	sortedDistIndicies = distances.argsort()
	classCount = {}
	
	for i in range(K):
		voteIlable = lables[sortedDistIndicies[i]]
		classCount[voteIlable] = classCount.get(voteIlable,0) + 1
	
	sortedClassCount = sorted(classCount.iteritems(),key = operator.itemgetter(1),reverse=True)
	return sortedClassCount[0][0]

def file2matrix(filename):
	fr = open(filename)
	arrayOflines = fr.readlines()
	numberOfLines = len(arrayOflines)
	returnMat = zeros((numberOfLines,3))
	classLabelVector = []
	index = 0
	for line in arrayOflines:
		line = line.strip()
		listFromLine = line.split('\t')
		returnMat[index,:] = listFromLine[0:3]
		classLabelVector.append(int(listFromLine[-1]))
		index += 1
	return returnMat,classLabelVector
	
def autoNorm(dateSet):
	minVals = dateSet.min(0)
	maxVals = dateSet.max(0)
	ranges = maxVals - minVals
	normDataSet = zeros(shape(dateSet))
	m = dateSet.shape[0]
	normDataSet = dateSet - tile(minVals,(m,1))
	normDataSet = normDataSet/tile(ranges,(m,1))
	return normDataSet,ranges,minVals
	
def datingClassTest():
	hoRatio = 0.10
	datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')
	normMat, ranges, minVals = autoNorm(datingDataMat)
	m = normMat.shape[0]
	numTestVecs = int(m*hoRatio)
	errorCount = 0.0
	for i in range(numTestVecs):
		classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
		print "the classifier came back with:%d,the real answer is:%d" % (classifierResult,datingLabels[i])
		if(classifierResult != datingLabels[i]):
			errorCount += 1
	print "the total error rate is: %f"  % (errorCount/float(numTestVecs))
	
def classifyPerson():
	resultList = ['not at all','in small doses','in laarge doses']
	percentTats = float(raw_input("percentage of time spent playing cideo games?"))
	ffMiles = float(raw_input("frequent fliter miles earned per year?"))
	iceCream = float(raw_input("liters of ice cream consumed per year?"))
	
	datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')
	normMat, ranges, minVals = autoNorm(datingDataMat)
	inArr = array([ffMiles,percentTats,iceCream])
	classifierResult = classify0((inArr-minVals)/ranges,normMat,datingLabels,3)
	
	print ("you will probably like this person:%s" % resultList[classifierResult-1])

def img2vector(filename):
    returnVect = zeros((1,1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0,32*i+j] = int(lineStr[j])
    return returnVect

def handwritingClassTest():
    hwLabels = []
    trainingFileList = listdir('trainingDigits')           #load the training set
    m = len(trainingFileList)
    trainingMat = zeros((m,1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]     #take off .txt
        classNumStr = int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:] = img2vector('trainingDigits/%s' % fileNameStr)
    testFileList = listdir('testDigits')        #iterate through the test set
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]     #take off .txt
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = img2vector('testDigits/%s' % fileNameStr)
        classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, 3)
        print "the classifier came back with: %d, the real answer is: %d" % (classifierResult, classNumStr)
        if (classifierResult != classNumStr): errorCount += 1.0
    print "\nthe total number of errors is: %d" % errorCount
    print "\nthe total error rate is: %f" % (errorCount/float(mTest))
#print img2vector('testDigits/0_13.txt')[0:10]
	
if (__name__ == "__main__"):
	handwritingClassTest()
	
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.scatter(datingDataMat[:,1],datingDataMat[:,2],15.0*array(datingLabels),15.0*array(datingLabels))
# plt.show()

def createDataSet():
	group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
	lables = ['A','A','B','B']
	return group,lables
	

	
# if __name__ == "__main__":
	# group,lables = createDataSet()
	# print classify0([0,0],group,lables,3)
	
#group,lables = createDataSet()
#print group,lables

raw_input('please enter')