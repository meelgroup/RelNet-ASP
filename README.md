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
First you need to compile ApproxASP. cd to ApproxASP and see the readme in `ApproxASP` directory to compile ApproxASP. After sucessful compilation mv approxasp binary to `scripts` directory.

### Run RelNet-ASP

To run `RelNet-ASP`, cd to scripts directory. The directory has necessary scripts to run RelNet-ASP.

The input graph is `molise.pl` (LP format). The command to compute network reliability of `molise.pl` for $p = 0.125 = \frac{1}{2^3}$, (edge probability), that is $k=1, m=3$ is as follows:
```
python run-relnet-asp.py -i molise.pl -k 1 -m 3
```

### Benchmark 
The artifact and benchmark of RelNet-ASP is available [here](https://zenodo.org/records/19453575).

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
