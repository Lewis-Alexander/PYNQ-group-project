# FPGA-Accelerated Spirograph Generator 🌀
**Hardware/Software Co-Design Project for Epitrochoid/Hypotrochoid Visualization**

[![PYNQ-Z2](https://img.shields.io/badge/Platform-PYNQ_Z2_FPGA-blue)](http://www.pynq.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

![Example Hypotrochoid](https://via.placeholder.com/400x300?text=Sample+Hypotrochoid)  
*Example output from the FPGA-accelerated generator*

## 📖 Description
This project combines FPGA hardware acceleration with Python visualization to generate intricate **epitrochoids** and in future **hypotrochoids** - geometric curves created by tracing points on rolling circles. Key components:

- **Hardware Acceleration**: Custom VHDL IP core for parametric calculations (4.8× faster than software)
- **Interactive GUI**: ipycanvas interface with real-time parameter control
- **Jupyter Integration**: `spirograph_setup.ipynb` for FPGA configuration
- **Educational Focus**: Explores math behind spirographs and FPGA co-design

## ⚙️ Installation

### Prerequisites
- [PYNQ-Z2 Board](https://www.tul.com.tw/Products/PYNQ-Z2.html) with SD card
- Vivado 2021.1+ (for FPGA synthesis)
- Python 3.8+ with packages:  
  ```bash
  sudo apt pip3 install pynq numpy matplotlib ipywidgets ipycanvas
shh into Xilinx@{your boards ip address} default pass = xilinx
then:
  git clone https://gitlab.cis.strath.ac.uk/cxb22132/further-vhdl-project.git
  cd further-vhdl-project


### 🚀 Usage
Jupyter Notebook Setup
Connect to PYNQ via Jupyter Lab (http://<board-ip>:9090)

enter PYNQ-Group-Project folder

Run spirograph_setup.ipynb to:

Load FPGA overlay

Initialize DMA channels

Verify hardware/software communication

Launch GUI

Change values to see updating of graph

### Future work:
add hypotrochoid support by copying epitrochoids adding a section for euclids algorithm to be multiplied onto the max theta and swapping some of the additions subtractions and sin cos blocks around.

Allowing for a higher number of bits per input at the very least making num points be set at compile time to give more space in the 32 bit word for R r and d to allow for more interesting patterns

Increasing speed of gui to redraw

adding more examples of each type in the setup and a bit more text explaining what they actually are.
