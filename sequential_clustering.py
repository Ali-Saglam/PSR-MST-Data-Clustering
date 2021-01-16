# -*- coding: utf-8 -*-
"""
@author:
    
Saglam, Ali, & Baykan, N. A. (2017).

"Sequential image segmentation based on min- imum spanning tree representation".

Pattern Recognition Letters, 87 , 155–162.

https://doi.org/10.1016/j.patrec.2016.06.001 .
"""

import numpy as np
from fibheap import *
import math
import sys

# --------------------------------------------------------------------------------
# Segment an image:
# Returns a color image representing the segmentation.
#
# Inputs:
#           in_image: image to segment.
#           sigma: to smooth the image.
#           k: constant for threshold function.
#           min_size: minimum component size (enforced by post-processing stage).
#
# Returns:
#           num_ccs: number of connected components in the segmentation.
# --------------------------------------------------------------------------------

def sequential_clustering(data, m = 3, l = "scale"):
    
    size = len(data)
    
    ###################################################
    
    labels, psr, mst = create_PSR_MST(data)
    
    ###################################################
    
    if l == "scale":
        l = int(math.sqrt(size) / 2)
        
    print("l : ",l)
    
    print("m : ",m)

    psrlen = len(psr)
    sumdiff = float(0)
    for i in range(1, psrlen):
        sumdiff += abs(psr[i][0] - psr[i - 1][0])
    c = float(sumdiff / (psrlen - 1))
    c *= m
        
    print("c : ",c)
    
    ###################################################
    
    labels = S_MST_segmentation(psr, mst, l, c)
    
    ###################################################
    
    return labels
    
    
def create_PSR_MST(data):
    datasize = len(data)

    labels = np.zeros(datasize, dtype=int);
    labels[:] = int(-1)
    edges = np.zeros(shape=(datasize, datasize, 3), dtype=float);

    # build graph
    nnum = int(0)
    enum = 0
    for x in range(datasize):
        for y in range(x, datasize):
            if x == y:
                edges[x,y,0] = -1
                continue
            
            edges[x,y,0] = np.linalg.norm(data[x] - data[y])
            edges[x,y,1] = x
            edges[x,y,2] = y
            
            edges[y,x,0] = edges[x,y,0]
            edges[y,x,1] = y
            edges[y,x,2] = x

    edges = edges.tolist()
    for i in range(datasize):
        for j in range(datasize):
            edges[i][j] = tuple(edges[i][j])
        
    psr_mst = np.zeros(datasize - 1, dtype=tuple)
    count = 0
    
    heap = makefheap()

    current = int(0)
    labels[current] = 0
    
    mst = [[]] * datasize
    
    for i in range(datasize):
        mst[i] = []
    
    while True:   
        for i in range(datasize):
            edge = edges[current][i]
            if edge[0] == -1:
                continue
            if labels[int(edge[2])] == -1:
                fheappush(heap, edge)
        
        psr_mst[count] = heap.extract_min().key
        
        while labels[int(psr_mst[count][2])] != -1 and heap.num_nodes != 0:
            psr_mst[count] = heap.extract_min().key
            
        if labels[int(psr_mst[count][2])] != -1:
            continue
            
        mst[int(psr_mst[count][1])].append(int(psr_mst[count][2]))
        mst[int(psr_mst[count][2])].append(int(psr_mst[count][1]))
        
        current = int(psr_mst[count][2])
        labels[current] = 0
        count += 1;
        
        if heap.num_nodes == 0 or count == datasize - 1:
            break
    
    psr_mst = psr_mst.tolist()
    
    return labels, psr_mst, mst


def S_MST_segmentation(psr, mst, l, c):
    maxin1 = -1
    maxin2 = -1
    max1 = -1000
    max2 = -1000
    
    psrlen = len(psr)
    
    sys.setrecursionlimit(len(mst))
    
    labels = np.zeros(len(mst), dtype=int)

    searchlen = 2 * l + 1;
    
    if psrlen < searchlen:
        return False
    
    seg_id = 1
    
    start = l
    finish = psrlen - l
    
    for i in range(start, finish):
        
        first = i - l
        last = i - 1
        
        
        if maxin1 < first:
            max1 = psr[first][0]
            maxin1 = first
            for j in range(first + 1, last + 1):
                if psr[j][0] > max1:
                    max1 = psr[j][0]
                    maxin1 = j
        elif psr[last][0] > max1:
                max1 = psr[last][0]
                maxin1 = last
                
        
        first = i + 1
        last = i + l
        
        
        if maxin2 < first:
            max2 = psr[first][0]
            maxin2 = first
            for j in range(first + 1, last + 1):
                if psr[j][0] > max2:
                    max2 = psr[j][0]
                    maxin2 = j
        elif psr[last][0] > max2:
                max2 = psr[last][0]
                maxin2 = last
                
        
        if psr[i][0] > min(max1, max2) + c:  
            segsize1 = 0
            segsize2 = 0
            
            segsize1, labels = labelNodes(labels, mst, psr[i][1], psr[i][2], seg_id, 0)
            seg_id += 1
            
            mst[int(psr[i][1])].remove(psr[i][2])
            mst[int(psr[i][2])].remove(psr[i][1])

    return labels


def labelNodes(labels, mst, nodein, prein, segid, segsize):
    labels[int(nodein)] = segid
    segsize += 1
    for i in range(len(mst[int(nodein)])):
        if mst[int(nodein)][i] != prein:
            segsize, labels = labelNodes(labels, mst, mst[int(nodein)][i], nodein, segid, segsize)
    return segsize, labels
    
