import Proj3_5functions
import alg_cluster


class test_class:
    def __init__(self, result):
        self.result = result

    def result(self):
        return self.result


# class_list = []
# for i in range(3,0,-1):
#     class_list.append(test_class(i))
#
# S = [1,2,3]
# S.sort(key=lambda kk: class_list[kk].result())
#
# cluster_num = 2
# for u in range(cluster_num - 1):
#     for v in range(u + 1, cluster_num):
#         print u, v

print Proj3_5functions.closest_pair_strip([alg_cluster.Cluster(set([]), 0, 0, 1, 0),
                    alg_cluster.Cluster(set([]), 1, 0, 1, 0),
                    alg_cluster.Cluster(set([]), 2, 0, 1, 0),
                    alg_cluster.Cluster(set([]), 3, 0, 1, 0)], 1.5, 1.0)

# print Proj3_5functions.slow_closest_pair([alg_cluster.Cluster(set([]), 0, 0, 1, 0), alg_cluster.Cluster(set([]), 1, 0, 1, 0)])