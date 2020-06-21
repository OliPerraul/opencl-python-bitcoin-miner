
import math
import timeit
import argparse
import os

import gpu_worker
import parallel_worker
import sequential_worker
import util
import numpy as np


if __name__ == '__main__':
    parser = argparse.ArgumentParser()  # top level parser
    parser.add_argument('-difficulty', type=int, required=True)
    parser.add_argument('-worker', type=str, required=True)
    args = parser.parse_args()

    if args.worker == "sequential":
        sequential_worker.work(args.difficulty)
    elif args.worker == "parallel":
        parallel_worker.work(args.difficulty)
    elif args.worker == "gpu":
        gpu_worker.work(args.difficulty)

