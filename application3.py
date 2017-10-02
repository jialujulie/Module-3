
import matplotlib.pyplot as plt
import time
import Proj3_5functions
import random
import alg_cluster

def gen_random_clusters(num_clusters):
    cluster_list = []
    while num_clusters:
        cluster_list.append(alg_cluster.Cluster(set(), random.randrange(-1,1),random.randrange(-1,1),0,0))
        num_clusters -= 1
    return cluster_list



running_times = []
running_times_fast = []
for n in range(2,201,1):
    cluster_list = gen_random_clusters(n)
    time0 = time.time()
    Proj3_5functions.slow_closest_pair(cluster_list)
    time1 = time.time()

    running_times.append(time1-time0)

    time0_fast = time.time()
    Proj3_5functions.fast_closest_pair(cluster_list)
    time1_fast = time.time()

    running_times_fast.append(time1_fast-time0_fast)

# Plotting
plt.plot(list(range(2,201)),running_times,'-r',label = 'slow closest pair')
plt.plot(list(range(2,201)),running_times_fast,'-b', label = 'fast closest pair')
plt.legend(loc = 'upper right')

plt.title('Efficiency Comparision of two algorithms for finding the closest pair-desktop python')
plt.xlabel('Number of Clusters')
plt.ylabel('Running times')
#plt.scatter(indegree_distribution.keys(),normalize_dist)
plt.savefig('question1.png')
plt.show()