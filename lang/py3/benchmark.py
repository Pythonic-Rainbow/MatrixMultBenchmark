from multiprocessing import Pool
import pyopencl as ocl
import pyopencl.array
import numpy as np
import time
from random import randint

with open('../../gpu/opencl.cl') as f:
    cl_prg = ''.join(f.readlines())

class Matrix:

    def __init__(self):
        self.data = [[]]
        self.rows = 0
        self.cols = 0

    def print(self):
        for row in self.data:
            print(' '.join(str(c) for c in row) + ';\n')
        print(f'{self.rows}x{self.cols}')

    @staticmethod
    def __gen__(col):
        return [randint(0, 1000) for _ in range(col)]

    def resize(self, row , col):
        if self.rows != row or self.cols != col:
            with Pool() as pool:
                self.data = pool.map(self.__gen__, map(lambda r: col, range(row)))
            self.rows = row
            self.cols = col


class Matrices:

    def __init__(self):
        self.a = Matrix()
        self.b = Matrix()

    def resize(self, np, m):
        self.a.resize(np, m)
        self.b.resize(m, np)


class Stopwatch:

    def __init__(self):
        self.msgs = []
        self.start = time.perf_counter()

    def lap(self, msg: str):
        t = time.perf_counter()
        duration = t - self.start
        self.start = t
        self.msgs.append(f'{msg}: {duration:.4f}s')

    def print(self):
        print('\n'.join(self.msgs))


def __row__(row, b):
    cl = []
    for column in range(len(b[0])):
        s = 0
        for i, otr in enumerate(b):
            s += row[i] * otr[column]
        cl.append(s)
    return cl


def single(m: Matrices) -> [[int]]:
    """Multiplies using single core"""
    start = time.perf_counter()
    n = []
    for row in m.a.data:
        n.append(__row__(row, m.b.data))
    duration = time.perf_counter() - start
    print(f'Single-core: {duration:.4f}s')
    return n


def multiple(m: Matrices) -> [[int]]:
    """Multiplies using multiple-core"""
    start = time.perf_counter()
    with Pool() as p:
        result = p.starmap(__row__, map(lambda row: (row, m.b.data), m.a.data))
    duration = time.perf_counter() - start
    print(f'Multi-core: {duration:.4f}s')
    return result


def opencl(m: Matrices, dev: ocl.Device) -> [[int]]:
    """Multiplies using OpenCL"""
    ctx = ocl.Context(devices=(dev,))
    sw = Stopwatch()
    with ocl.CommandQueue(ctx) as q:
        a = ocl.array.to_device(q, np.array(m.a.data))
        b = ocl.array.to_device(q, np.array(m.b.data))
        s = ocl.array.Array(q, m.a.rows ** 2, np.int32)
        sw.lap('->GPU')

        prg = ocl.Program(ctx, cl_prg).build()
        prg.multiply(q, s.shape, None,
                     np.int32(m.a.rows), np.int32(m.a.cols), np.int32(m.b.cols),
                     a.data, b.data, s.data)
        s = s.reshape(m.a.rows, m.b.cols)
        q.finish()
        sw.lap('GPU compute')

        result = s.map_to_host().tolist()
    sw.lap('->CPU')
    sw.print()
    return result
