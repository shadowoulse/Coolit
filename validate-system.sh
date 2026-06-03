#!/bin/bash

# Cool It System Validation Script
# Checks if the system meets requirements for fan control

echo "🔍 Cool It - System Validation"
echo "=============================="

EXIT_CODE=0

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "❌ Not running on Linux"
    EXIT_CODE=1
else
    echo "✅ Linux detected"
fi

# Check Python 3
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    echo "✅ Python 3 found: $PYTHON_VERSION"
else
    echo "❌ Python 3 not found"
    EXIT_CODE=1
fi

# Check PyQt5
if python3 -c "import PyQt5" 2>/dev/null; then
    echo "✅ PyQt5 available"
else
    echo "❌ PyQt5 not found - install with: pip3 install PyQt5"
    EXIT_CODE=1
fi

# Check NVIDIA tools
if command -v nvidia-smi &> /dev/null; then
    echo "✅ nvidia-smi found"
    
    # Test NVIDIA GPU access
    if nvidia-smi &>/dev/null; then
        echo "✅ NVIDIA GPU detected"
    else
        echo "⚠️  NVIDIA GPU not accessible or drivers not loaded"
    fi
else
    echo "⚠️  nvidia-smi not found - GPU fan control will not work"
fi

if command -v nvidia-settings &> /dev/null; then
    echo "✅ nvidia-settings found"
else
    echo "⚠️  nvidia-settings not found - install nvidia-utils package"
fi

# Check sensors
if command -v sensors &> /dev/null; then
    echo "✅ lm-sensors found"
else
    echo "⚠️  sensors command not found - install lm-sensors package"
fi

# Check hwmon paths
echo ""
echo "📁 Available hwmon paths:"
if ls /sys/class/hwmon/hwmon*/temp*_input 2>/dev/null; then
    echo "✅ Temperature sensors found"
else
    echo "❌ No temperature sensors found in /sys/class/hwmon/"
    EXIT_CODE=1
fi

if ls /sys/class/hwmon/hwmon*/pwm* 2>/dev/null; then
    echo "✅ PWM controls found"
else
    echo "⚠️  No PWM controls found - CPU fan control may not work"
fi

# Check sudo access
echo ""
echo "🔐 Checking privileges:"
if sudo -n true 2>/dev/null; then
    echo "✅ Sudo access available"
else
    echo "⚠️  Sudo access required for hardware control"
fi

echo ""
if [[ $EXIT_CODE -eq 0 ]]; then
    echo "🎉 System validation passed! Cool It should work on this system."
else
    echo "⚠️  System validation found issues. Some features may not work."
fi

echo ""
echo "💡 Tips:"
echo "  • Run 'sudo sensors-detect' to setup temperature monitoring"
echo "  • Install missing packages with your package manager"
echo "  • Check /sys/class/hwmon/ for available sensors"
echo "  • Ensure NVIDIA drivers are properly installed"

exit $EXIT_CODE