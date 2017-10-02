"""
Student template code for Project 3
Student will implement five functions:

slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a 2D list of clusters in the plane
"""

import math
import alg_cluster


######################################################
# Code for closest pairs of clusters

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a list

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices for two clusters

    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Input: cluster_list is the list of clusters

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.
    """
    dist = (float("inf"),-1,-1)

    cluster_num = len(cluster_list)
    for u_index in range(cluster_num-1):
        for v_index in range(u_index+1,cluster_num):
            dist_u_v = pair_distance(cluster_list,u_index,v_index)
            #print dist_u_v
            if dist_u_v[0] < dist[0]:
                dist = dist_u_v

    return dist


def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.
    """
    cluster_list.sort(key = lambda cluster: cluster.horiz_center())
    cluster_n = len(cluster_list)

    if cluster_n < 4:
        (dist,i_index,j_index) = slow_closest_pair(cluster_list)
    else:
    # divide
        m_index = cluster_n/2
        #pleft = cluster_list[:m_index]
        #pright = cluster_list[m_index:]
        (d_left, i_left, j_left) = fast_closest_pair(cluster_list[:m_index])
        (d_ri, i_ri, j_ri) = fast_closest_pair(cluster_list[m_index:])
    # merge
        (dist, i_index, j_index) = (d_left, i_left, j_left) if d_left < d_ri else (d_ri, i_ri + m_index, j_ri + m_index)

        mid = (cluster_list[m_index-1].horiz_center() + cluster_list[m_index].horiz_center())/2

        t_closest_pair_strip = closest_pair_strip(cluster_list, mid, dist)

        if dist > t_closest_pair_strip[0]:
            (dist, i_index, j_index) = t_closest_pair_strip


    return (dist, i_index, j_index)


def closest_pair_strip(cluster_list, horiz_center, half_width):
    # type: (object, object, object) -> object
    """
    Helper function to compute the closest pair of clusters in a vertical strip

    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.
    """

    slist = []
    for index_i in range(len(cluster_list)):
        if half_width + horiz_center > cluster_list[index_i].horiz_center() > horiz_center - half_width:
            slist.append(index_i)

    #print S_list
    slist.sort(key=lambda i: cluster_list[i].vert_center())

    #print S_list
    k_len = len(slist)

    (dist,i_index,j_index) = (float("inf"), -1, -1)

    for index_u in range(k_len-1):
        for index_v in range(index_u+1,min(index_u+3, k_len-1)+1):
            dist_uv = pair_distance(cluster_list, slist[index_u],slist[index_v])

            if dist_uv[0] < dist:
                (dist, i_index, j_index) = dist_uv

    return (dist, i_index, j_index)


######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list

    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    #cluster_n = len(cluster_list)
    c_list = [cluster.copy() for cluster in cluster_list]
    while len(c_list)>num_clusters:
        closestpair = fast_closest_pair(c_list)
        c_list[closestpair[1]].merge_clusters(c_list[closestpair[2]])
        c_list.pop(closestpair[2])

    return c_list


######################################################################
# Code for k-means clustering


def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list

    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """

    # position initial clusters at the location of clusters with largest populations
    new_cluster_list = [cluster.copy() for cluster in cluster_list]
    new_cluster_list.sort(key = lambda cluster: cluster.total_population(), reverse=True)


    n_cluster = len(new_cluster_list)
    miu_list = list(new_cluster_list[:num_clusters])
    #print miu_list
    #for i in range(num_clusters):
     #   miu_list.append(alg_cluster.Cluster())


    while num_iterations>0:
        c_buckets = []
        num_clusters1 = num_clusters
        while num_clusters1>0:
            c_buckets.append(alg_cluster.Cluster(set(),0,0,0,0))
            num_clusters1 -= 1

        #print len(c_buckets)
        for j_index in range(n_cluster):
            min_dist = float("inf")
            for f_index in range(num_clusters):
                dist = new_cluster_list[j_index].distance(miu_list[f_index])
                if dist < min_dist:
                    min_dist = dist
                    l_index = f_index
            #print "mindist", min_dist, l_index

            c_buckets[l_index].merge_clusters(new_cluster_list[j_index])
            #print c_buckets[:2]

        for f_index in range(num_clusters):
            x_pos = c_buckets[f_index].horiz_center()
            y_pos = c_buckets[f_index].vert_center()
            miu_list[f_index] = alg_cluster.Cluster(set(),x_pos,y_pos,0,0)

        num_iterations -= 1



    return c_buckets

