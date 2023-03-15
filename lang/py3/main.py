import os

import pyopencl as ocl

import benchmark

os.environ['PYOPENCL_NO_CACHE'] = '1'

if __name__ == '__main__':
    m = benchmark.Matrices()
    while True:
        hw_choice = int(input(
            '1. Single-core\n'
            '2. Multi-core\n'
            '3. GPU (OpenCL)\n'
        ))
        if hw_choice == 1:
            m.resize(1200, 100)
            input('Start')
            benchmark.single(m)
        elif hw_choice == 2:
            m.resize(1900, 190)
            input('Start')
            benchmark.multiple(m)
        else:
            m.resize(8250, 1500)
            devices = []
            print('The following devices in your system support OpenCL:')
            for platform in ocl.get_platforms():
                print(platform.name + ' | ' + platform.version)
                for device in platform.get_devices():
                    print(f'{len(devices)}. {device.name} | {device.version} | {device.max_compute_units} CU')
                    devices.append(device)
            device_choice = int(input('Enter device number to benchmark: '))
            device = devices[device_choice]

            benchmark.opencl(m, device)
