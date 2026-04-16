### RelNet-ASP 
RelNet-ASP is an ASP Counting based network reliability estimator. The related publication is [here](https://easychair.org/publications/paper/8zhh).

### Clone the repo
```
git clone --recurse-submodules git@github.com:meelgroup/RelNet-ASP.git
```

### Dependencies
You need to install cmake, g++, re2c, and bison.
```
sudo apt-get install bison
sudo apt-get install re2c
sudo apt install build-essential cmake
```


### ASP Counter: ApproxASP
We used [ApproxASP](https://github.com/meelgroup/ApproxASP) as the ASP counter. It is added as a submodule. 

## Compile ApproxASP
Run `build.sh` to compile approxasp:
```
chmod +x build.sh
./build.sh
```
You will see approxasp is copied to scripts directory.

## Run RelNet-ASP

First `cd scripts` directory.

The input graph format is a list of edges with probabilities plus source and destination nodes. For example in `graph_molise.pl` file, the line
```
edge(1,2) 1 3
```
means that there is an edge between nodes 1 and 2 with probability $\frac{1}{2^3}$ (here $k=1, m=3$).
```
first 1 
last 100
```
means that source is node 1 and destination is node 100.

Now run RelNet-ASP on `graph_molise.pl` as follows:
```
python run-relnet-asp.py -i graph_molise.pl
```
it should output the reliability as follows:
```
The network reliability: a X 2^b / 2^c
```

### Benchmark 
The artifact and benchmark of RelNet-ASP is available [here](https://zenodo.org/records/19609416).

### Contributor
- [Mohimenul Kabir](https://mahi045.github.io/)
- [Kuldeep S Meel](https://www.comp.nus.edu.sg/~meel/)

### Acknowledgements
- [Anna Latour](https://latower.github.io/)
- [Roger Paredes](https://paredesroger.github.io/)

### Issue
If you face any issue, create a new issue or email to [mahibuet045@gmail.com](mailto:mahibuet045@gmail.com).

### How to cite
```
@inproceedings{KM2023,
  title={A Fast and Accurate ASP Counting Based Network Reliability Estimator.},
  author={Kabir, Mohimenul and Meel, Kuldeep S},
  booktitle={LPAR},
  volume={94},
  pages={270--287},
  year={2023}
}
```
