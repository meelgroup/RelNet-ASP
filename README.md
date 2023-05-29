### Directory structure
- `relnet-asp.py`: script to run RelNet-ASP
- `add_chain_formula.py`: script to compute chain ASP program
- `molise.pl`: an example graph instance

### Benchmark
The Benchmarks are available [here](https://zenodo.org/record/7737616#.ZGMVRtJByV4).

### Counter
The ApproxASP is publicly available here: [ApproxASP](https://github.com/meelgroup/ApproxASP2).
One binary is given in the current directory.

### Run RelNet-ASP
**Please check whether add_chain_formula.py, approxasp, molise.pl exist in your current directory, and approxasp is executable (chmod +x)**

There is a graph instance `molise.pl` in LP format. First compute the chain formula of `molise.pl` for edge probability `0.125`, by executing the following command:
```
python add_chain_formula.py -i molise.pl -p 0.125
```  
After successful execution, the command will show the following output:
```
Number of new rules added: 250
The multiplication factor: 375
```
We need to value of **The multiplication factor:** to compute the network reliability. More specifically, we divide the ASP count by $2^{375}$. 
The script `add_chain_formula.py` will generate two files to run ASP counter: chain formula augmented ASP program ($\mathcal{Q}$) in  `chain_molise.pl` and independent support  `IS_chain_molise.pl`. Independent support is useful for counting efficiently.

Now let run an ASP counter using the following command:
```
./approxasp --sparse --conf 0.35 --useind IS_chain_molise.pl --asp chain_molise.pl
```
The command will take few seconds to run and finally it shows the approximate count 
in line: **After the iteration, the (median) number of solution: 50 * 2 ^ 356**

So, the reliability is $\frac{50 \times 2^{356}}{2^{375}}$

### Contributor
- [Mohimenul Kabir](https://mahi045.github.io/)
- [Kuldeep S Meel](https://www.comp.nus.edu.sg/~meel/)

### Acknowledgements
- [Anna Latour](https://latower.github.io/)
- [Roger Paredes](https://paredesroger.github.io/)

### Issue
If you face any issue, create a new issue or email to [mahibuet045@gmail.com](mailto:mahibuet045@gmail.com).
