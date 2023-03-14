# MatrixMultBenchmark

This project benchmarks the matrix multiply algorithm against different hardware and language combinations.  
For hardware, there are 3 options: Single-core, Multi-core and GPU.

Adjust the matrix size so each run takes ~10s.


For CPU testing, take a screenshot of HWinfo when the benchmark is done.
For GPU testing, start logging when you choose the device for benchmark. stop logging when the benchmark is done.  
Make sure that there are at least 3 rows with 100% core utilization.

# Results
`Power` measures the clock speed and power consumption when under certain workloads.  
They are measured using the HWiNFO program.  

Bandwidth is measured in Gbps. It serves as a metric of data transfer rate: if the recorded bandwidth reaches the design limit, it hinders performance and the run should be disqualified.

For CPU:
* Power refers to the "Core+SoC power".
* Single-core frequency refers to the frequency of the core that is under stress.

GPU benchmarks are complicated because we need to copy data to/from the main memory.
I've decided to record the average/max of several data.  
Max shows the performance in a single event. For example, my dGPU clocks at 1.8-9GHz when it's doing actual computation.  
Average shows the performance with all factors considered. For example, dGPU clocks at just 300MHz when receiving data from main memory. The average clock from CPU sending data to CPU receiving results is ~1.5GHz. This gives an estimation of the relative performance over the entire test.
* Main memory bandwidth DOES NOT mean video RAM bandwidth, but rather the rate of the CPU pulling from/pushing to main memory.
* PCIe bandwidth: In this benchmark I am only counting uni-directional bandwidth. The equation is `Link speed * Encoding(128/130) * Lanes`.
* VRAM bandwidth: The equation is `Clock * Bus width * pump rate`.

For dGPU:
* Power is the sum of CPU "Core+SoC power" and "GPU power". Avg only.
* PCIe transfer rate: Much lower when idle. Avg&Max.
* VRAM bandwidth: Much lower when idle. Avg&Max.

For iGPU:
* Power refers to the "CPU Package power". [See this](https://www.hwinfo.com/forum/threads/how-to-read-apu-power-consumption-properly.8206/)
* Bandwidth: iGPU doesn't use PCIe (I think), it uses the main memory instead and the memory clock is constant.


# Tools
The `tool` folder contains some tools for processing benchmark results.
* calc.xlsx: A spreadsheet that computes the average of several runs. The data is my Python iGPU benchmark. Ignore the colored columns if you're just using this.
* bandwidth-calc.py: Calculates PCIe/VRAM bandwidth.
* efficiency-calc.py: Calculates computation per second and computation per joule.