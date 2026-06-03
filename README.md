# Cool It - Linux Fan Control for MSI Laptops

A GUI application to control CPU and GPU fan speeds on MSI laptops running Linux.

⚠️ **SECURITY WARNING**: This application requires root privileges to control hardware. Review the code before running.

## Features

- **5 Fan Modes**: Auto, Silent, Balanced, Performance, Extreme
- **Real-time Monitoring**: Live GPU and CPU temperature display  
- **12 Beautiful Themes**: Dark, Blue, Purple, Red, Cyan, Orange, Green, Pink, Amber, Indigo, Matrix, Neon
- **Modern GUI**: Clean, draggable interface
- **Manual Control**: Override automatic fan curves with custom speeds

## Requirements

- MSI Laptop with NVIDIA GPU
- Linux (tested on Ubuntu/Fedora-based distributions)
- Python 3.6+
- NVIDIA drivers and tools
- Hardware monitoring support

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/shadowoulse827/Coolit.git
cd coolit
```

### 2. Install Dependencies

#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install python3-pyqt5 lm-sensors nvidia-settings
```

#### Fedora/RHEL:
```bash
sudo dnf install python3-qt5 lm_sensors nvidia-settings
```

#### Using pip:
```bash
pip3 install -r requirements.txt
```

### 3. Setup Hardware Monitoring

```bash
sudo sensors-detect  # Follow prompts and accept defaults
```

### 4. Make Scripts Executable

```bash
chmod +x coolit-launcher.sh
```

## Usage

### Command Line

```bash
sudo python3 coolit.py
```

### Desktop Launcher

1. Copy desktop file:
```bash
cp coolit.desktop ~/Desktop/
chmod +x ~/Desktop/coolit.desktop
```

2. Trust and launch the application

## Fan Modes

| Mode | GPU Fan | CPU Curve | Description |
|------|---------|-----------|-------------|
| **Auto** | System | System | Default behavior |
| **Silent** | 30% | Quiet | Low noise, moderate cooling |
| **Balanced** | 50% | Balanced | Good balance of cooling/noise |
| **Performance** | 75% | Aggressive | High cooling, more noise |
| **Extreme** | 100% | Maximum | Maximum cooling, loud |

## Troubleshooting

**Dependencies missing:**
```bash
pip3 install PyQt5>=5.15.0
```

**GPU fan not working:**
- Ensure NVIDIA drivers: `nvidia-smi`
- Check nvidia-settings: `which nvidia-settings`

**CPU fan not working:**
- Check hwmon path: `ls /sys/class/hwmon/`
- Adjust `CPU_PWM_PATH` in code if needed

**Permission denied:**
- Ensure script has sudo privileges
- Run: `sudo python3 coolit.py`

## Hardware Compatibility

- Tested on MSI laptops
- Requires NVIDIA GPU for GPU fan control
- CPU fan control via standard Linux hwmon interface

## Security Notes

- **Root access required** for hardware control
- **Review code** before running with sudo
- Application automatically restores Auto mode on exit
- No network connections made

## Contributing

Pull requests welcome! Please:
1. Test on your hardware
2. Follow existing code style
3. Update documentation

## License

MIT License - see LICENSE file

## Disclaimer

**Use at your own risk.** Improper fan control can cause hardware damage from overheating. Monitor temperatures and ensure adequate cooling.
