import sys
import subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

current_mode = "Auto"
current_theme = "Dark"
CPU_PWM_PATH = "/sys/class/hwmon/hwmon4"

MODES = {
    "Auto": {"gpu": 0},
    "Silent": {"gpu": 30},
    "Balanced": {"gpu": 50},
    "Performance": {"gpu": 75},
    "Extreme": {"gpu": 100}
}

CPU_CURVES = {
    "Auto": {"pwms": None},
    "Silent": {"pwms": [60, 80, 100, 120, 140, 160]},
    "Balanced": {"pwms": [80, 100, 130, 160, 190, 220]},
    "Performance": {"pwms": [120, 140, 170, 200, 230, 255]},
    "Extreme": {"pwms": [160, 180, 210, 230, 245, 255]}
}

THEMES = {
    "Dark": {
        "bg": "#0d1117", "title_bg": "#161b22", "title_text": "#e6edf3",
        "status_bg": "#238636", "status_text": "#ffffff",
        "monitor_bg": "#161b22", "monitor_border": "#30363d", "monitor_text": "#58a6ff",
        "btn_bg": "#21262d", "btn_text": "#e6edf3", "btn_border": "#30363d",
        "btn_hover": "#30363d", "btn_active": "#238636", "label_text": "#7d8590"
    },
    "Blue": {
        "bg": "#0a1929", "title_bg": "#132f4c", "title_text": "#b2d4ff",
        "status_bg": "#0072e5", "status_text": "#ffffff",
        "monitor_bg": "#132f4c", "monitor_border": "#1e4976", "monitor_text": "#66b2ff",
        "btn_bg": "#1e4976", "btn_text": "#b2d4ff", "btn_border": "#2d5f8d",
        "btn_hover": "#2d5f8d", "btn_active": "#0072e5", "label_text": "#5090d3"
    },
    "Purple": {
        "bg": "#1a0d2e", "title_bg": "#2d1b4e", "title_text": "#d4b2ff",
        "status_bg": "#7c3aed", "status_text": "#ffffff",
        "monitor_bg": "#2d1b4e", "monitor_border": "#4c2f76", "monitor_text": "#c084fc",
        "btn_bg": "#4c2f76", "btn_text": "#d4b2ff", "btn_border": "#6d4a8d",
        "btn_hover": "#6d4a8d", "btn_active": "#7c3aed", "label_text": "#9d6fd3"
    },
    "Red": {
        "bg": "#1f0d0d", "title_bg": "#3d1a1a", "title_text": "#ffb2b2",
        "status_bg": "#dc2626", "status_text": "#ffffff",
        "monitor_bg": "#3d1a1a", "monitor_border": "#5c2f2f", "monitor_text": "#ff8080",
        "btn_bg": "#5c2f2f", "btn_text": "#ffb2b2", "btn_border": "#7d4a4a",
        "btn_hover": "#7d4a4a", "btn_active": "#dc2626", "label_text": "#d37d7d"
    },
    "Cyan": {
        "bg": "#0a2e2e", "title_bg": "#134e4a", "title_text": "#99f6e4",
        "status_bg": "#14b8a6", "status_text": "#ffffff",
        "monitor_bg": "#134e4a", "monitor_border": "#0f766e", "monitor_text": "#5eead4",
        "btn_bg": "#0f766e", "btn_text": "#99f6e4", "btn_border": "#14b8a6",
        "btn_hover": "#14b8a6", "btn_active": "#14b8a6", "label_text": "#5eead4"
    },
    "Orange": {
        "bg": "#1f1108", "title_bg": "#3d2108", "title_text": "#ffd4a3",
        "status_bg": "#f97316", "status_text": "#ffffff",
        "monitor_bg": "#3d2108", "monitor_border": "#7c2d12", "monitor_text": "#fdba74",
        "btn_bg": "#7c2d12", "btn_text": "#ffd4a3", "btn_border": "#c2410c",
        "btn_hover": "#c2410c", "btn_active": "#f97316", "label_text": "#fdba74"
    },
    "Green": {
        "bg": "#0a1f0f", "title_bg": "#14532d", "title_text": "#bbf7d0",
        "status_bg": "#22c55e", "status_text": "#ffffff",
        "monitor_bg": "#14532d", "monitor_border": "#166534", "monitor_text": "#86efac",
        "btn_bg": "#166534", "btn_text": "#bbf7d0", "btn_border": "#16a34a",
        "btn_hover": "#16a34a", "btn_active": "#22c55e", "label_text": "#86efac"
    },
    "Pink": {
        "bg": "#2e0a1f", "title_bg": "#4a1942", "title_text": "#ffc4e1",
        "status_bg": "#ec4899", "status_text": "#ffffff",
        "monitor_bg": "#4a1942", "monitor_border": "#831843", "monitor_text": "#f9a8d4",
        "btn_bg": "#831843", "btn_text": "#ffc4e1", "btn_border": "#be185d",
        "btn_hover": "#be185d", "btn_active": "#ec4899", "label_text": "#f9a8d4"
    },
    "Amber": {
        "bg": "#1f1508", "title_bg": "#451a03", "title_text": "#fde68a",
        "status_bg": "#f59e0b", "status_text": "#ffffff",
        "monitor_bg": "#451a03", "monitor_border": "#78350f", "monitor_text": "#fcd34d",
        "btn_bg": "#78350f", "btn_text": "#fde68a", "btn_border": "#b45309",
        "btn_hover": "#b45309", "btn_active": "#f59e0b", "label_text": "#fcd34d"
    },
    "Indigo": {
        "bg": "#0f0a2e", "title_bg": "#1e1b4b", "title_text": "#c7d2fe",
        "status_bg": "#6366f1", "status_text": "#ffffff",
        "monitor_bg": "#1e1b4b", "monitor_border": "#312e81", "monitor_text": "#a5b4fc",
        "btn_bg": "#312e81", "btn_text": "#c7d2fe", "btn_border": "#4338ca",
        "btn_hover": "#4338ca", "btn_active": "#6366f1", "label_text": "#a5b4fc"
    },
    "Matrix": {
        "bg": "#000000", "title_bg": "#001a00", "title_text": "#00ff00",
        "status_bg": "#003300", "status_text": "#00ff00",
        "monitor_bg": "#001100", "monitor_border": "#003300", "monitor_text": "#00ff00",
        "btn_bg": "#002200", "btn_text": "#00ff00", "btn_border": "#003300",
        "btn_hover": "#003300", "btn_active": "#00ff00", "label_text": "#00cc00"
    },
    "Neon": {
        "bg": "#0a0a0a", "title_bg": "#1a1a2e", "title_text": "#00ffff",
        "status_bg": "#ff00ff", "status_text": "#000000",
        "monitor_bg": "#16213e", "monitor_border": "#ff00ff", "monitor_text": "#00ffff",
        "btn_bg": "#1a1a2e", "btn_text": "#00ffff", "btn_border": "#ff00ff",
        "btn_hover": "#ff00ff", "btn_active": "#ff00ff", "label_text": "#00ffff"
    }
}

def get_stylesheet(theme):
    t = THEMES[theme]
    return f"""
QWidget#MainWindow {{
    background: {t['bg']};
    border-radius: 16px;
}}
QLabel#Title {{
    color: {t['title_text']};
    font-size: 14px;
    font-weight: 600;
    padding: 12px;
}}
QLabel#ModeStatus {{
    background: {t['status_bg']};
    color: {t['status_text']};
    border-radius: 10px;
    padding: 18px 24px;
    margin: 18px 18px 12px 18px;
    font-size: 18px;
    font-weight: 600;
    min-height: 50px;
}}
QLabel#Monitor {{
    background: {t['monitor_bg']};
    border: 1px solid {t['monitor_border']};
    border-radius: 10px;
    padding: 24px;
    margin: 12px 18px 18px 18px;
    color: {t['monitor_text']};
    font-family: 'Monospace';
    font-size: 14px;
    line-height: 2.2;
}}
QPushButton {{
    background: {t['btn_bg']};
    color: {t['btn_text']};
    border: 1px solid {t['btn_border']};
    border-radius: 10px;
    padding: 18px 32px;
    font-size: 16px;
    font-weight: 500;
    margin: 8px 16px;
    min-height: 20px;
    text-align: center;
}}
QPushButton:hover {{
    background: {t['btn_hover']};
    border: 1px solid {t['btn_border']};
}}
QPushButton#Active {{
    background: {t['btn_active']};
    color: {t['status_text']};
    border: 1px solid {t['btn_active']};
    font-weight: 600;
}}
QPushButton#MinBtn {{
    background: transparent;
    color: {t['title_text']};
    font-size: 20px;
    padding: 10px;
    margin: 0px;
    border: none;
    border-radius: 8px;
    min-width: 36px;
    max-width: 36px;
}}
QPushButton#MinBtn:hover {{
    background: {t['btn_hover']};
}}
QPushButton#CloseBtn {{
    background: transparent;
    color: {t['title_text']};
    font-size: 20px;
    padding: 10px;
    margin: 0px;
    border: none;
    border-radius: 8px;
    min-width: 36px;
    max-width: 36px;
}}
QPushButton#CloseBtn:hover {{
    background: #da3633;
}}
QLabel#ThemeLabel {{
    color: {t['label_text']};
    font-size: 11px;
    font-weight: 600;
    margin: 0px 0px 8px 20px;
}}
"""

class FanControlApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cool It - Fan Control")
        self.setStyleSheet("background-color: #000000;")
        self.mode_buttons = {}
        self.dragging = False
        self.drag_position = QPoint()
        self.setup_ui()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_display)
        self.timer.start(2000)
        self.update_display()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        if hasattr(self, 'dragging') and self.dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        if hasattr(self, 'dragging'):
            self.dragging = False
        event.accept()
    
    def setup_ui(self):
        self.container = QWidget()
        self.container.setStyleSheet(get_stylesheet(current_theme))
        
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        # Title bar
        title_bar = QWidget()
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(10, 5, 10, 5)
        
        title = QLabel("Cool It - Fan Control")
        title.setStyleSheet(f"color: {THEMES[current_theme]['title_text']}; font-size: 16px; font-weight: bold;")
        title_layout.addWidget(title, stretch=1)
        
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
        
        # Theme cycle button
        self.theme_btn = QPushButton(f"🎨 Theme: {current_theme}")
        self.theme_btn.setCursor(Qt.PointingHandCursor)
        self.theme_btn.clicked.connect(self.cycle_theme)
        layout.addWidget(self.theme_btn)
        
        # Mode buttons
        layout.addSpacing(12)
        mode_label = QLabel("  SELECT MODE")
        mode_label.setObjectName("ThemeLabel")
        layout.addWidget(mode_label)
        
        for mode_name in MODES.keys():
            btn = QPushButton(mode_name)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked, m=mode_name: self.change_mode(m))
            self.mode_buttons[mode_name] = btn
            layout.addWidget(btn)
        
        self.update_button_styles()
        
        # Footer
        footer = QLabel("Fan Control • v2.0")
        footer.setStyleSheet("color: #484f58; font-size: 10px; padding: 5px;")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.container)
        
        self.setMinimumSize(400, 550)
        self.resize(450, 650)

    def update_button_styles(self):
        stylesheet = get_stylesheet(current_theme)
        for name, btn in self.mode_buttons.items():
            btn.setObjectName("Active" if name == current_mode else "")
            btn.setStyleSheet(stylesheet)
    
    def cycle_theme(self):
        global current_theme
        themes = list(THEMES.keys())
        idx = themes.index(current_theme)
        current_theme = themes[(idx + 1) % len(themes)]
        self.theme_btn.setText(f"🎨 Theme: {current_theme}")
        self.container.setStyleSheet(get_stylesheet(current_theme))
        self.update_button_styles()
    
    def change_mode(self, mode):
        global current_mode
        current_mode = mode
        self.update_button_styles()
        self.apply_mode()
        self.update_display()
    
    def update_display(self):
        try:
            mode_text = f"{current_mode} Mode"
            self.mode_status.setText(mode_text)
            
            gpu_temp = self.get_gpu_temp()
            cpu_temp = self.get_cpu_temp()
            gpu_usage = self.get_gpu_usage()
            cpu_usage = self.get_cpu_usage()
            
            if current_mode == "Auto":
                gpu_fan = "Auto"
                cpu_fan = "Auto"
            else:
                gpu_fan = f"{MODES[current_mode]['gpu']}%"
                cpu_fan = "Manual"
            
            line1 = f"GPU: {gpu_temp}°C ({gpu_usage}%)  |  CPU: {cpu_temp}°C ({cpu_usage}%)"
            line2 = f"GPU Fan: {gpu_fan}  |  CPU Fan: {cpu_fan}"
            self.monitor.setText(f"{line1}\n{line2}")
            
            self.monitor.update()
            QApplication.processEvents()
        except Exception as e:
            print(f"ERROR: {e}")
    
    def apply_mode(self):
        if current_mode == "Auto":
            self.restore_auto()
        else:
            self.set_gpu_fan(MODES[current_mode]["gpu"])
            self.set_cpu_fan(current_mode)
    
    def get_gpu_temp(self):
        try:
            result = subprocess.run(["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader,nounits"],
                                  capture_output=True, text=True, timeout=3)
            if result.returncode == 0:
                return int(result.stdout.strip())
        except:
            pass
        return 0
    
    def get_gpu_usage(self):
        try:
            result = subprocess.run(["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"],
                                  capture_output=True, text=True, timeout=3)
            if result.returncode == 0:
                return int(result.stdout.strip())
        except:
            pass
        return 0
    
    def get_cpu_usage(self):
        try:
            result = subprocess.run(["top", "-bn1"], capture_output=True, text=True, timeout=3)
            for line in result.stdout.split('\n'):
                if 'Cpu(s)' in line:
                    idle = float(line.split('id,')[0].split()[-1])
                    return int(100 - idle)
        except:
            pass
        return 0
    
    def get_cpu_temp(self):
        try:
            result = subprocess.run(["cat", "/sys/class/hwmon/hwmon4/temp1_input"],
                                  capture_output=True, text=True, timeout=3)
            if result.returncode == 0:
                return int(result.stdout.strip()) // 1000
        except:
            pass
        try:
            result = subprocess.run(["cat", "/sys/class/hwmon/hwmon0/temp1_input"],
                                  capture_output=True, text=True, timeout=3)
            if result.returncode == 0:
                return int(result.stdout.strip()) // 1000
        except:
            pass
        try:
            result = subprocess.run(["sensors"], capture_output=True, text=True, timeout=3)
            for line in result.stdout.split('\n'):
                if 'Package id 0' in line or 'Tctl' in line:
                    temp_str = line.split('+')[1].split('°')[0].strip()
                    return int(float(temp_str))
        except:
            pass
        return 0
    
    def set_gpu_fan(self, speed):
        try:
            subprocess.run(["nvidia-settings", "-a", "[gpu:0]/GPUFanControlState=1"], 
                          capture_output=True, timeout=5)
            subprocess.run(["nvidia-settings", "-a", f"[fan:0]/GPUTargetFanSpeed={speed}"], 
                          capture_output=True, timeout=5)
        except:
            pass
    
    def set_cpu_fan(self, mode):
        pwms = CPU_CURVES[mode]["pwms"]
        if pwms is None:
            return
        try:
            with open(f"{CPU_PWM_PATH}/pwm1_enable", "w") as f:
                f.write("1\n")
            for i, pwm in enumerate(pwms, start=1):
                with open(f"{CPU_PWM_PATH}/pwm1_auto_point{i}_pwm", "w") as f:
                    f.write(f"{pwm}\n")
        except:
            pass
    
    def restore_auto(self):
        try:
            with open(f"{CPU_PWM_PATH}/pwm1_enable", "w") as f:
                f.write("2\n")
            subprocess.run(["nvidia-settings", "-a", "[gpu:0]/GPUFanControlState=0"], 
                          capture_output=True, timeout=5)
        except:
            pass
    
    def closeEvent(self, event):
        self.restore_auto()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FanControlApp()
    window.show()
    sys.exit(app.exec_())