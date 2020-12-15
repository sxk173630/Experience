import random as rd
import re
import math
import string

#Function for preprocessing the tweets.
def Preprocessing(url):
    f = open(url, "r", encoding="utf8")
    #Creating a list of the tweets.
    tweet = list(f)
    tweetList = []

    for i in range(len(tweet)):
        #Converting the tweets from a string type to a list of strings.
        tweetList.append(tweet[i].split(' '))

        #Removing the tweet-id and timestamp.
        tweet[i] = tweet[i][23:]

        #Removing any word that starts with the symbol @.
        tweet[i] = " ".join(filter(lambda x: x[0] != '@', tweet[i].split()))

        #Removing any hashtag symbols.
        tweet[i] = tweet[i].replace('#', '')

        #Removing any URL.
        tweet[i] = re.sub(r"http\S+", "", tweet[i])
        tweet[i] = re.sub(r"www\S+", "", tweet[i])

        #Converting every word to lowercase.
        tweet[i] = tweet[i].lower()
    #Closing cnnhealth.txt.
    f.close()
    #Returning the list of newly formatted tweets.
    return tweetList

#Function for performing K-means clustering on the resulting tweets using at least 5 different values of K.
def KMeans(tweet, k=5, max_iterations=5):
    centroids = []

    #Assigning tweets as centroids randonmly by creating a dict() and a while loop to iterate throughh the tweets.
    count = 0
    hashMap = dict()

    while count < k:
        #Randomizing the tweets.
        tweetIndex = rd.randint(0, len(tweet) - 1)

        if tweetIndex not in hashMap:
            count += 1
            hashMap[tweetIndex] = True
            centroids.append(tweet[tweetIndex])

    iterations = 0
    previousCentriod = []
    #Stop when iterations converged or max iteration is reached.
    while (Convergance(previousCentriod, centroids)) == False and (iterations < max_iterations):
        print("Iteration: " + str(iterations))
        #Assigning the tweet to the closest centroids.
        clusters = assign_cluster(tweet, centroids)
        #Check to see if the K-means converges.
        previousCentriod = centroids
        #Updates the centroids using the formed clusters.
        centroids = UpdateCentroid(clusters)
        iterations = iterations + 1

    if (iterations == max_iterations):
        print("K-means not converged")
    else:
        print("K-means converged")

    sse = getSSE(clusters)

    return clusters, sse

#Function for checking convergance.
def Convergance(prev_centroid, new_centroids):
    #If statement for determining if centroid lenghts are equal.
    if len(prev_centroid) != len(new_centroids):
        return False
    else:
        for count in range(len(new_centroids)):
            if " ".join(new_centroids[count]) != " ".join(prev_centroid[count]):
                return False
    return True

#Assigns the closest centroid to each tweet iteration.
def assign_cluster(tweet, centroids):
    clusters = dict()
    count = 1

    for i in range(len(tweet)):
        minDistance = math.inf
        clusterIndex = -1

        #Finds the nearest centroid for a given tweet.
        for count in range(len(centroids)):
            dis = jaccardDistance(centroids[count], tweet[i])
            if centroids[count] == tweet[i]:
                clusterIndex = count
                minDistance = 0
                break
            else:
                if dis < minDistance:
                    clusterIndex = count
                minDistance = dis
        if minDistance == 1:
            clusterIndex = rd.randint(0, len(centroids) - 1)
        #Assignment process
        clusters.setdefault(clusterIndex, []).append([tweet[i]])

        #Finds the distance betwen the closest centroid to tweet in order to calculate the SSE.
        last_tweet_idx = len(clusters.setdefault(clusterIndex, [])) - 1
        clusters.setdefault(clusterIndex, [])[last_tweet_idx].append(minDistance)

    return clusters

#Updates the centroid by iterating every cluster and finds the closest tweet distance in the same cluster.
def UpdateCentroid(clusters):
    centroids = []
    count = 1

    for count in range(len(clusters)):
        minDistancePoints = []
        minDistanceSum = math.inf
        centroidIndex = -1
        #Finds the sum of distances from each tweet1 and tweet2 in a same cluster.
        for tweet1 in range(len(clusters[count])):
            minDistancePoints.append([])
            sumOfDistances = 0

            for tweet2 in range(len(clusters[count])):
                if tweet1 != tweet2:
                    if tweet2 < tweet1:
                        distance = minDistancePoints[tweet2][tweet1]
                    else:
                        distance = jaccardDistance(clusters[count][tweet1][0], clusters[count][tweet2][0])

                    minDistancePoints[tweet1].append(distance)
                    sumOfDistances += distance
                else:
                    minDistancePoints[tweet1].append(0)

            #Finds the tweet with the least sum of distances and uses that as the centroid for the cluster.
            if sumOfDistances < minDistanceSum:
                minDistanceSum = sumOfDistances
                centroidIndex = tweet1

        centroids.append(clusters[count][centroidIndex][0])

    return centroids

#Returns the Jaccard Distance of the intersection from tweet1 and tweet2/length of union from tweet1 and tweet2.
def jaccardDistance(tweet1, tweet2):
    #Finds the intersection between tweet1 and tweet2.
    intersection = set(tweet1).intersection(tweet2)
    #Finds the union between tweet1 and tweet2.
    union = set().union(tweet1, tweet2)
    #returns the Jaccard Distance
    return 1 - (len(intersection) / len(union))

#Iterates every count of cluster and finds the SSE.
def getSSE(clusters):
    sse = 0
    count = 1
    #Calculates the SSE.
    for count in range(len(clusters)):
        for t in range(len(clusters[count])):
            sse = sse + (clusters[count][t][1] * clusters[count][t][1])

    return sse

#Reads in the .txt and sets the trials to be performed.
if __name__ == '__main__':

    data_url = 'cnnhealth.txt'
    tweet = Preprocessing(data_url)
    count = 1
    trial = 3
    #K-means value
    k = 5
    #Runs K-means for each trial.
    for t in range(trial):
        print("Trial: " + str((t + 1)) + " for K = " + str(k))
        clusters, sse = KMeans(tweet, k)
        # for every cluster 'c', print size of each cluster
        for count in range(len(clusters)):
            print(str(count + 1) + ": ", str(len(clusters[count])) + " tweets")
        print("--> SSE : " + str(sse))
        print('\n')
        k = k + 1