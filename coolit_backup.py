import sys
import subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

current_mode = "Auto"
CPU_PWM_PATH = "/sys/class/hwmon/hwmon4"

MODES = {
    "Auto": {"gpu": 0, "icon": "[AUTO]"},
    "Silent": {"gpu": 30, "icon": "[SILENT]"},
    "Balanced": {"gpu": 50, "icon": "[BALANCED]"},
    "Performance": {"gpu": 75, "icon": "[PERF]"},
    "Extreme": {"gpu": 100, "icon": "[EXTREME]"}
}

CPU_CURVES = {
    "Auto": {"pwms": None},
    "Silent": {"pwms": [60, 80, 100, 120, 140, 160]},
    "Balanced": {"pwms": [80, 100, 130, 160, 190, 220]},
    "Performance": {"pwms": [120, 140, 170, 200, 230, 255]},
    "Extreme": {"pwms": [160, 180, 210, 230, 245, 255]}
}

STYLESHEET = """
QWidget#MainWindow {
    background: #0d1117;
    border-radius: 16px;
}
QLabel#Title {
    color: #e6edf3;
    font-size: 14px;
    font-weight: 600;
    padding: 12px;
}
QLabel#ModeStatus {
    background: #238636;
    color: #ffffff;
    border-radius: 10px;
    padding: 18px 24px;
    margin: 18px 18px 12px 18px;
    font-size: 18px;
    font-weight: 600;
    min-height: 50px;
}
QLabel#Monitor {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 24px;
    margin: 12px 18px 18px 18px;
    color: #58a6ff;
    font-family: 'Monospace';
    font-size: 14px;
    line-height: 2.2;
}
QPushButton {
    background: #21262d;
    color: #e6edf3;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 18px 32px;
    font-size: 16px;
    font-weight: 500;
    margin: 8px 16px;
    min-height: 20px;
    text-align: center;
}
QPushButton:hover {
    background: #30363d;
    border: 1px solid #484f58;
}
QPushButton#Active {
    background: #238636;
    color: #ffffff;
    border: 1px solid #2ea043;
    font-weight: 600;
}
QPushButton#MinBtn {
    background: transparent;
    color: #e6edf3;
    font-size: 20px;
    padding: 10px;
    margin: 0px;
    border: none;
    border-radius: 8px;
    min-width: 36px;
    max-width: 36px;
}
QPushButton#MinBtn:hover {
    background: #30363d;
}
QPushButton#CloseBtn {
    background: transparent;
    color: #e6edf3;
    font-size: 20px;
    padding: 10px;
    margin: 0px;
    border: none;
    border-radius: 8px;
    min-width: 36px;
    max-width: 36px;
}
QPushButton#CloseBtn:hover {
    background: #da3633;
}
"""

class FanControlApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.mode_buttons = {}
        self.dragging = False
        self.drag_position = QPoint()
        self.setup_ui()
        
        # Start monitoring timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_display)
        self.timer.start(2000)  # Update every 2 seconds
        
        # Force immediate update
        self.update_display()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        if self.dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        self.dragging = False
        event.accept()
    
    def setup_ui(self):
        self.setObjectName("MainWindow")
        
        container = QWidget()
        container.setObjectName("MainWindow")
        container.setStyleSheet(STYLESHEET)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 25)
        layout.setSpacing(0)
        
        # Title bar
        title_bar = QWidget()
        title_bar.setStyleSheet("background: #161b22; border-top-left-radius: 16px; border-top-right-radius: 16px; border-bottom: 1px solid #30363d;")
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(0, 0, 0, 0)
        
        title = QLabel("Cool It")
        title.setObjectName("Title")
        title_layout.addWidget(title, stretch=1)
        
        min_btn = QPushButton("−")
        min_btn.setObjectName("MinBtn")
        min_btn.clicked.connect(self.showMinimized)
        min_btn.setCursor(Qt.PointingHandCursor)
        title_layout.addWidget(min_btn)
        
        close_btn = QPushButton("✕")
        close_btn.setObjectName("CloseBtn")
        close_btn.clicked.connect(self.close)
        close_btn.setCursor(Qt.PointingHandCursor)
        title_layout.addWidget(close_btn)
        
        layout.addWidget(title_bar)
        
        # Mode status
        self.mode_status = QLabel("Auto Mode")
        self.mode_status.setObjectName("ModeStatus")
        self.mode_status.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.mode_status)
        
        # Monitor display
        self.monitor = QLabel("Loading...")
        self.monitor.setObjectName("Monitor")
        self.monitor.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(self.monitor)
        
        # Mode buttons
        layout.addSpacing(12)
        mode_label = QLabel("  SELECT MODE")
        mode_label.setStyleSheet("color: #7d8590; font-size: 11px; font-weight: 600; margin: 0px 0px 8px 20px;")
        layout.addWidget(mode_label)
        
        for mode_name, mode_data in MODES.items():
            btn = QPushButton(mode_name)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked, m=mode_name: self.change_mode(m))
            self.mode_buttons[mode_name] = btn
            layout.addWidget(btn)
        
        self.update_button_styles()
        
        # Footer
        footer = QLabel("Simplified Fan Control • v1.0")
        footer.setStyleSheet("color: #484f58; font-size: 10px; padding: 10px;")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)
        
        # Shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(0, 0, 0, 180))
        shadow.setOffset(0, 10)
        container.setGraphicsEffect(shadow)
        
        outer = QVBoxLayout(self)
        outer.setContentsMargins(15, 15, 15, 15)
        outer.addWidget(container)
        
        self.setMinimumSize(420, 640)
        self.resize(420, 640)
    
    def update_button_styles(self):
        for name, btn in self.mode_buttons.items():
            if name == current_mode:
                btn.setObjectName("Active")
            else:
                btn.setObjectName("")
            btn.setStyleSheet(STYLESHEET)
    
    def change_mode(self, mode):
        global current_mode
        current_mode = mode
        self.update_button_styles()
        self.apply_mode()
        self.update_display()
    
    def update_display(self):
        try:
            # Update mode status
            mode_text = f"{current_mode} Mode"
            self.mode_status.setText(mode_text)
            print(f"Mode status set to: {mode_text}")
            
            # Get temps
            gpu_temp = self.get_gpu_temp()
            cpu_temp = self.get_cpu_temp()
            
            # Get fan info
            if current_mode == "Auto":
                gpu_fan = "Auto"
                cpu_fan = "Auto"
            else:
                gpu_fan = f"{MODES[current_mode]['gpu']}%"
                cpu_fan = "Manual"
            
            # Build monitor text
            line1 = f"GPU: {gpu_temp}°C  |  CPU: {cpu_temp}°C"
            line2 = f"GPU Fan: {gpu_fan}  |  CPU Fan: {cpu_fan}"
            monitor_text = f"{line1}\n{line2}"
            
            # Update monitor
            self.monitor.setText(monitor_text)
            print(f"Monitor text set to: {monitor_text}")
            
            # Force update
            self.monitor.update()
            QApplication.processEvents()
            
        except Exception as e:
            print(f"ERROR in update_display: {e}")
            import traceback
            traceback.print_exc()
    
    def apply_mode(self):
        if current_mode == "Auto":
            self.restore_auto()
        else:
            self.set_gpu_fan(MODES[current_mode]["gpu"])
            self.set_cpu_fan(current_mode)
    
    def get_gpu_temp(self):
        try:
            result = subprocess.run(["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader,nounits"],
                                  capture_output=True, text=True, timeout=1)
            if result.returncode == 0:
                temp = int(result.stdout.strip())
                print(f"GPU Temp: {temp}°C")
                return temp
        except Exception as e:
            print(f"GPU temp error: {e}")
        return 0
    
    def get_cpu_temp(self):
        # Try multiple methods
        try:
            result = subprocess.run(["cat", "/sys/class/hwmon/hwmon4/temp1_input"],
                                  capture_output=True, text=True, timeout=1)
            if result.returncode == 0:
                temp = int(result.stdout.strip()) // 1000
                print(f"CPU Temp: {temp}°C")
                return temp
        except Exception as e:
            print(f"CPU temp method 1 error: {e}")
        
        # Try hwmon0
        try:
            result = subprocess.run(["cat", "/sys/class/hwmon/hwmon0/temp1_input"],
                                  capture_output=True, text=True, timeout=1)
            if result.returncode == 0:
                temp = int(result.stdout.strip()) // 1000
                print(f"CPU Temp (hwmon0): {temp}°C")
                return temp
        except:
            pass
        
        # Try sensors command
        try:
            result = subprocess.run(["sensors"], capture_output=True, text=True, timeout=1)
            for line in result.stdout.split('\n'):
                if 'Package id 0' in line or 'Tctl' in line:
                    temp_str = line.split('+')[1].split('°')[0].strip()
                    temp = int(float(temp_str))
                    print(f"CPU Temp (sensors): {temp}°C")
                    return temp
        except Exception as e:
            print(f"CPU temp sensors error: {e}")
        
        return 0
    
    def set_gpu_fan(self, speed):
        try:
            subprocess.run(["nvidia-settings", "-a", "[gpu:0]/GPUFanControlState=1"], capture_output=True)
            subprocess.run(["nvidia-settings", "-a", f"[fan:0]/GPUTargetFanSpeed={speed}"], capture_output=True)
            print(f"GPU fan set to {speed}%")
        except Exception as e:
            print(f"GPU fan error: {e}")
    
    def set_cpu_fan(self, mode):
        pwms = CPU_CURVES[mode]["pwms"]
        if pwms is None:
            return
        try:
            with open(f"{CPU_PWM_PATH}/pwm1_enable", "w") as f:
                f.write("1\n")
            print(f"Setting CPU fan curve for {mode}:")
            for i, pwm in enumerate(pwms, start=1):
                with open(f"{CPU_PWM_PATH}/pwm1_auto_point{i}_pwm", "w") as f:
                    f.write(f"{pwm}\n")
                print(f"  Point {i}: {pwm}")
        except Exception as e:
            print(f"CPU fan error: {e}")
    
    def restore_auto(self):
        try:
            with open(f"{CPU_PWM_PATH}/pwm1_enable", "w") as f:
                f.write("2\n")
            subprocess.run(["nvidia-settings", "-a", "[gpu:0]/GPUFanControlState=0"], capture_output=True)
            print("Restored automatic fan control")
        except Exception as e:
            print(f"Restore auto error: {e}")
    
    def closeEvent(self, event):
        self.restore_auto()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FanControlApp()
    window.show()
    sys.exit(app.exec_())
