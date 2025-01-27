This code is slightly modified and extended
from https://github.com/johngardenghi/ar4,
originally written for the paper:

> E. G. Birgin, J. L. Gardenghi, J. M. Martínez, and S. A. Santos, On
  the use of third-order models with fourth-order regularization for
  unconstrained optimization, 2018.

The results obtained using this code are included in

> C. Cartis, R. A. Hauser, Y. Liu, K. Welzel, W. Zhu, Efficient
  Implementation of Third-order Tensor Methods with Adaptive
  Regularization for Unconstrained Optimization, 2025

## Compiling and running the code

Consider `$(AR3)` the root folder of this repository.

1. Go to `$(AR3)` folder and type
```
make
```

2. You can run the drivers to MGH problems and the Packing problem in
`$(AR3)/bin` folder by running `mgh` and `pack` binaries files,
respectively. Follow the instructions given by these programs to run
the tests.

## Algencan and HSL

The tests in the paper were run using MA57 and BLAS
subroutines. Algencan does not need these files to work, but in order
to reproduce the tests in the paper, the user must include them. To
include them, follow these steps:

1. Obtain HSL_MA57 from Harwell Subroutine Library
[website](http://www.hsl.rl.ac.uk/).

2. Obtain BLAS subroutine from Netlib
[website](http://www.netlib.org/blas/).

3. Copy the files in `$(AR3)/algencan/sources/hsl` folder:

   * From BLAS library: `dgemm.f`, `dgemv.f`, `dtpmv.f`, `dtpsv.f`,
     `idamax.f`, `lsame.f`, `xerbla.f`.

   * From HSL MA57 library: `hsl_ma57d.f90`, `hsl_zd11d.f90`,
     `ma57ad.f`, `mc21ad.f`, `mc34ad.f`, `mc47ad.f`, `mc59ad.f`,
     `mc64ad.f`, `mc71ad.f`. (Except `hsl_ma57d.f90`, all other
     routines usually comes inside files named `deps.f` and
     `deps90.f90`. The user may need to save them in files with these
     names.)

   * HSL MA57 requires MeTIS. You can use `fakemetis.f` that comes
     with HSL MA57 distribution.

4. Include `-lhsl` flag in variable `ALGENCAN_FLAGS` inside
`$(AR3)/Makefile` file.

## WandB upload

To upload the results of running this code to
[WandB](https://wandb.ai/), compile it as instructed above with the
HSL and BLAS files, use pip to install the `wandb` Python package,
open `$(AR3)/bin` in your terminal and run

```
./mgh -p 2 -pert 0 -subtol 1e-9 -prob 1:35 -pl 0 -track
mv *_rmp.txt experiments_p2
./mgh -p 3 -pert 0 -subtol 1e-9 -prob 1:35 -pl 0 -track
mv *_rmp.txt experiments_p3
python upload_to_wandb.py
```

The generated data can be found at
https://wandb.ai/ar3-project/all_experiments
in the Exp_Benchmark_3 group. It includes runs with and without the
`-subtol 1e-9` option (corresponding to
inner_stop_rule="First_Order" and inner_stop_rule="ARP_Theory"
respectively).
