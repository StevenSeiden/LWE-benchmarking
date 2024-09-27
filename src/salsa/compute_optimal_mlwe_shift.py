""""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.

This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import numpy as np
import argparse


def get_parser():
    parser = argparse.ArgumentParser(allow_abbrev=False)

    parser.add_argument("--secret_path", type=str, help="secret path")
    parser.add_argument("--k", type=int, default=1, help="k=1 for RLWE and k>1 for Module-LWE")
    parser.add_argument("--nu", type=int, help="Cliff size: number of unreduced entries of A")
    return parser

def compute_minhi_mlwe(s, n, k, cruel_bits, step=1):
    assert k*n == len(s)
    s = (s!=0).astype(int)
    s = s.reshape((k,n)).T
    u = cruel_bits//k
    hi = s[:u].sum(axis=0).sum()
    minhi = hi
    argmin = 0

    for i in range(0, n, step):
        hi -= s[i].sum()
        hi += s[(i+u)%n].sum()
        if hi < minhi:
            minhi = hi
            argmin = i+1

    optimal_shift = (-u-argmin)%n
    return optimal_shift, argmin, minhi


if __name__ == '__main__':
    parser = get_parser()
    params = parser.parse_args()
    assert params.k > 0 and params.secret_path
    
    secret = np.load(params.secret_path)
    n = len(secret)//params.k

    optimal_shift, argmin, minhi = compute_minhi_mlwe(secret, n, params.k, params.nu)
    print(
        f"Optimal shift of A is A_shift={optimal_shift}" + 
        f" corresponds to secret window start at secret_window={argmin}"+
        f" with Min_i hw(s)={minhi} cruel secret bits"
    )
