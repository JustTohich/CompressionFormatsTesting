import time
import os
import numpy as np
from matplotlib import pyplot as plt
from shutil import copyfileobj
import bz2
import zipfile
import zlib
import zstd

import text_stat


class TestResult:
    def __init__(self, compression_time, input_size, output_size):
        self.compression_time = compression_time
        self.input_size = input_size
        self.output_size = output_size


def test_bz2(filename, postfix='.bz2'):
    times = []
    input_sizes = []
    output_sizes = []
    for level in range(1, 10):
        t_start = time.time()
        with open(filename, 'rb') as input:
            with bz2.BZ2File(filename + postfix, 'wb', compresslevel=level) as output:
                copyfileobj(input, output)
        t_end = time.time()
        times.append(t_end - t_start)
        input_sizes.append(os.path.getsize(filename))
        output_sizes.append(os.path.getsize(filename + postfix))
        time.sleep(1)
    return TestResult(np.array(times), np.array(input_sizes), np.array(output_sizes))


def test_zip_deflated(filename, postfix='.zip_deflated'):
    times = []
    input_sizes = []
    output_sizes = []
    for level in range(1, 10):
        t_start = time.time()
        jungle_zip = zipfile.ZipFile(filename + postfix, 'w')
        jungle_zip.write(filename, compress_type=zipfile.ZIP_DEFLATED, compresslevel=level)
        jungle_zip.close()
        t_end = time.time()
        times.append(t_end - t_start)
        input_sizes.append(os.path.getsize(filename))
        output_sizes.append(os.path.getsize(filename + postfix))
        time.sleep(1)
    return TestResult(np.array(times), np.array(input_sizes), np.array(output_sizes))


def test_zip_bzip2(filename, postfix='.zip_bzip2'):
    times = []
    input_sizes = []
    output_sizes = []
    for level in range(1, 10):
        t_start = time.time()
        jungle_zip = zipfile.ZipFile(filename + postfix, 'w')
        jungle_zip.write(filename, compress_type=zipfile.ZIP_BZIP2, compresslevel=level)
        jungle_zip.close()
        t_end = time.time()
        times.append(t_end - t_start)
        input_sizes.append(os.path.getsize(filename))
        output_sizes.append(os.path.getsize(filename + postfix))
        time.sleep(1)
    return TestResult(np.array(times), np.array(input_sizes), np.array(output_sizes))


def test_zip_lzma(filename, postfix='.zip_lzma'):
    times = []
    input_sizes = []
    output_sizes = []
    for level in range(1, 10):
        t_start = time.time()
        jungle_zip = zipfile.ZipFile(filename + postfix, 'w')
        jungle_zip.write(filename, compress_type=zipfile.ZIP_LZMA, compresslevel=level)
        jungle_zip.close()
        t_end = time.time()
        times.append(t_end - t_start)
        input_sizes.append(os.path.getsize(filename))
        output_sizes.append(os.path.getsize(filename + postfix))
        time.sleep(1)
    return TestResult(np.array(times), np.array(input_sizes), np.array(output_sizes))


def test_zlib(filename, postfix='.zlib'):
    times = []
    input_sizes = []
    output_sizes = []
    for level in range(1, 10):
        t_start = time.time()
        with open(filename, 'rb') as input:
            with open(filename + postfix, 'wb') as output:
                output.write(zlib.compress(input.read(), level=level))
        t_end = time.time()
        times.append(t_end - t_start)
        input_sizes.append(os.path.getsize(filename))
        output_sizes.append(os.path.getsize(filename + postfix))
        time.sleep(1)
    return TestResult(np.array(times), np.array(input_sizes), np.array(output_sizes))


def test_zstd(filename, postfix='.zstd'):
    times = []
    input_sizes = []
    output_sizes = []
    for level in range(1, 10):
        t_start = time.time()
        with open(filename, 'rb') as input:
            with open(filename + postfix, 'wb') as output:
                output.write(zstd.compress(input.read(), level))
        t_end = time.time()
        times.append(t_end - t_start)
        input_sizes.append(os.path.getsize(filename))
        output_sizes.append(os.path.getsize(filename + postfix))
        time.sleep(1)
    return TestResult(np.array(times), np.array(input_sizes), np.array(output_sizes))


def test_text_stat(filename, postfix='.text_stat'):
    times = []
    input_sizes = []
    output_sizes = []
    for level in range(1, 10):
        t_start = time.time()
        with open(filename, 'rb') as input:
            with open(filename + postfix, 'wb') as output:
                output.write(text_stat.compressor(input.read(), level))
        t_end = time.time()
        times.append(t_end - t_start)
        input_sizes.append(os.path.getsize(filename))
        output_sizes.append(os.path.getsize(filename + postfix))
        time.sleep(1)
    return TestResult(np.array(times), np.array(input_sizes), np.array(output_sizes))


def test_algorithms(algorithm_names, files):
    for f in files:
        plt.title(f+" with size "+str(os.path.getsize(f))+" bytes")
        plt.xlabel("Ratio")
        plt.ylabel("Time")
        for algo in algorithm_names:
            if algo == 'text_stat' and '.txt' != f[-4:]:
                continue
            color = np.random.rand(3)
            plt.legend()
            res = eval("test_"+algo)(f)
            print(algo, f)
            plt.plot(res.input_size/res.output_size, res.compression_time, "*", color=color, label=algo)
            plt.legend()
        plt.show()


if __name__ == '__main__':
    algo_names = [
        'bz2',
        'zip_bzip2',
        'zip_deflated',
        'zip_lzma',
        'zlib',
        'zstd',
        'text_stat'
    ]
    files = [
        # 'АК Алгоритмы сжатия.pdf',
        # 'Blur.exe',
        'ГарриПоттер.txt']
    test_algorithms(algo_names, files)

