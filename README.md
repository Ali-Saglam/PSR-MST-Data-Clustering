# S-MST Data Clustering
A python adaptation from the method described in the paper [Sequential image segmentation based on minimum spanning tree representation](https://www.sciencedirect.com/science/article/abs/pii/S0167865516301192).


## Reference:

```
@article{SAGLAM2017155,
title = "Sequential image segmentation based on minimum spanning tree representation",
journal = "Pattern Recognition Letters",
volume = "87",
pages = "155-162",
year = "2017",
issn = "0167-8655",
doi = "https://doi.org/10.1016/j.patrec.2016.06.001",
url = "http://www.sciencedirect.com/science/article/pii/S0167865516301192",
author = "Ali Saglam and Nurdan Akhan Baykan"
}
```

<img src="./images/Fig_2.jpg" height="85%" width="85%">

### Dependence:
The code depends on the following third-party libraries:
- fibheap 0.2.1

```
pip install fibheap
```

### Run demo: 
```
python Demo_clustering.py
```

### Parameters:
*``m``* : The coefficient of the parameters *``c``* that calculated automatically using the differential of the PSR-MST in the [source paper](https://www.sciencedirect.com/science/article/abs/pii/S0167865516301192). If no value is given, the default value is ``3``.

*``l``* : The length of the scanning frame (sub-string) that scans through the PSR-MST. If no value is given, the default value is ``"scale"`` that computed by ``int( sqrt(datasize) / 2``).

### Segmentation  fuction:

 ``labels = sequential_clustering(data)`` -----> *m* = 3, *l* = "scale"

``labels = sequential_clustering(data, m = 4)`` -----> *l* = "scale"

``labels = sequential_clustering(data, m = 4, l = 10)``


## Reference:

```
@article{SAGLAM2017155,
title = "Sequential image segmentation based on minimum spanning tree representation",
journal = "Pattern Recognition Letters",
volume = "87",
pages = "155-162",
year = "2017",
issn = "0167-8655",
doi = "https://doi.org/10.1016/j.patrec.2016.06.001",
url = "http://www.sciencedirect.com/science/article/pii/S0167865516301192",
author = "Ali Saglam and Nurdan Akhan Baykan"
}
```
