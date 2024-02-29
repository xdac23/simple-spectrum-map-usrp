# Simple spectrum mapping

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Contributing](../CONTRIBUTING.md)

## About <a name = "about"></a>

A collection of GNU Radio block diagrams and python scripts to capture and plot frequency spectrum.

Two specific frequencies bands were measured for this project: LoRa and N77. 

The SDR device used was the USRP X310, with a UBX-160 board. For this case a 1G ethernet interface was used, which limited the bandwidth to 20 MHz (and therefore 20 MS/s).



## Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

Install UHD drivers for USRP. For this case, installing from source is optional as the standard packet works fine

```
sudo apt-get install libuhd-dev uhd-host
```

If your device is not updated, download the firmware images

```
sudo python3 uhd_images_downloader.py 
uhd_image_loader --args="type=x300,addr=192.168.10.2,fpga=HG"
```

Then install GNU Radio, visit the official page in order to install all the dependencies (which are a lot). Then run the next commmand

```
sudo apt install gnuradio
```

If the device is brand new, it may be necesary to perfom some calibration, run the following command from the UHD library

```
uhd_cal_rx_iq_balance --verbose --args="type=x300,addr=192.168.10.2,fpga=HG"
```

### Installing

For the Fosphor sink block, it is necessary to install OpenCL, check the respective for your system. For ubuntu 22, i7 10gen, the following command was used:

```
sudo apt-get install intel-opencl-icd
```

Then run the next commands, check the official page for the dependencies needed
```
git clone https://gitea.osmocom.org/sdr/gr-fosphor.git
cd gr-fosphor
mkdir build
cd build
cmake ..
make
sudo make install
sudo ldconfig
```

## Usage <a name = "usage"></a>

### LoRa

The LoRa band was measured and plotted on a single run, setting the sample rate to 10 MS/s and therefore the bandwidth at 10 MHz. For individual measurements below the maximum deviced bandwidth, all the utilities for LoRa may be used.

The next files are the utilites used for LoRa spectrum plotting:

* lora_plotter.grc/.py: Block diagram for real time plotting using Fosphor
* lora_simple_exporter.grc/.py: Block diagram for export the IQ raw data over a given duration. Note: the Head block control the measurment time.
* spectrogram_fft.py: Plots the waterfall diagram and the raw data after applying FFT
* 3d_spectrum.py: Plots the waterfall diagram and the 3D spectrum map (time-frequency-power)
* comparator.py: Creates a FFT plot comparing different signals. In this case, 4 signals were compared.

### N77

Regarding the N77 band, ranging from 3.3 GHz to 4.2 GHz, all the utilites were modified in order to incorporate frequency span.
For our case, we used 45 spans of 20 MHz each. So as it can be noticed, all the utilites incorporate the variable ```span``` which will control the exact frequency we want to measure.

The script n77_runner.py is in charge of execute the n77_ exporter.py from span X to span Y. The usage of this runner is simply by:

```
python3 n77_runner.py X Y`
```

Warning: Do not run the block diagram for n77_exporter in GNU radio because the python script will be overwritten and and the runner will not longer work

An extra utility called plot_joiner.py is included, this utility simply was used to created the full spectrum image by joining all the individual spans plots.

## Work to do
The N77 sweeper works only by executing the python program for each span. This is obviously not the correct approach as each time we need to initialize the device and therefore is resource and time consumming. The correct way should be implement frequency sweep procedure directly in GNU Radio or in python/c++. The OOT block of habets38 are an great way to do that.



