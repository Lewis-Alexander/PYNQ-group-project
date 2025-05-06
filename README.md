# FPGA-Accelerated Spirograph Generator 🌀
**Hardware/Software Co-Design Project for Epitrochoid/Hypotrochoid Visualization**

[![PYNQ-Z2](https://img.shields.io/badge/Platform-PYNQ_Z2_FPGA-blue)](http://www.pynq.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

![Example Hypotrochoid](https://via.placeholder.com/400x300?text=Sample+Hypotrochoid)  
*Example output from the FPGA-accelerated generator*

## 📖 Description
This project combines FPGA hardware acceleration with Python visualization to generate intricate **epitrochoids** and **hypotrochoids** - geometric curves created by tracing points on rolling circles. Key components:

- **Hardware Acceleration**: Custom VHDL IP core for parametric calculations (4.8× faster than software)
- **Interactive GUI**: PyQt5 interface with real-time parameter control
- **Jupyter Integration**: `spirograph_setup.ipynb` for FPGA configuration
- **Educational Focus**: Explores math behind spirographs and FPGA co-design

Adapted from [pynq-juliabrot](https://github.com/FredKellerman/pynq-juliabrot) for PS-PL communication.

## ⚙️ Installation

### Prerequisites
- [PYNQ-Z2 Board](https://www.tul.com.tw/Products/PYNQ-Z2.html) with SD card
- Vivado 2021.1+ (for FPGA synthesis)
- Python 3.8+ with packages:  
  ```bash
  pip install pynq numpy matplotlib pyqt5 ipywidgets

git clone https://gitlab.cis.strath.ac.uk/cxb22132/further-vhdl-project.git
cd further-vhdl-project


### 🚀 Usage
Jupyter Notebook Setup
Connect to PYNQ via Jupyter Lab (http://<board-ip>:9090)

Run spirograph_setup.ipynb to:

Load FPGA overlay

Initialize DMA channels

Verify hardware/software communication

Launch GUI
