import keyboard
import pyautogui
import random
import locale
import time
from screeninfo import get_monitors
import numpy as np
from datetime import datetime
import pyaudio
import tkinter as tk


def is_chinese_language():
    default_language, _ = locale.getdefaultlocale()
    if default_language.startswith('zh'):
        return True
    else:
        return False


is_chinese = is_chinese_language()


# 获取屏幕分辨率大小
def get_screen_resolution():
    monitors = get_monitors()
    if monitors:
        monitor = monitors[0]  # 假设只有一个显示器
        width = monitor.width
        height = monitor.height
        return width, height
    else:
        return None


def alert(content_text):
    # 创建顶层窗口
    window = tk.Toplevel()

    # 设置窗口属性
    window.overrideredirect(True)  # 移除窗口边框
    window.attributes('-alpha', 0.8)  # 设置窗口透明度
    window.attributes("-topmost", True)  # 置顶窗口

    # 获取屏幕尺寸
    tkscreen_width = window.winfo_screenwidth()
    tkscreen_height = window.winfo_screenheight()

    # 设置窗口大小和位置
    window_width = 450
    window_height = 120
    x = (tkscreen_width - window_width) // 2
    y = 75
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # 创建标签
    label = tk.Label(window, text=content_text, fg="white", bg="black", font=("汉仪文黑", 16, 'bold'))
    label.pack(fill=tk.BOTH, expand=True)

    # 设置定时器，3秒后关闭窗口
    window.after(1500, close_window, window)

    # 显示窗口
    window.deiconify()
    window.mainloop()


def close_window(window):
    window.withdraw()  # 隐藏窗口
    window.quit()  # 销毁窗口对象


def beep(duration, frequency):
    # 定义播放参数
    # 声音持续时间（秒）
    # 声音频率（Hz）

    # 创建Pyaudio对象
    audio = pyaudio.PyAudio()

    # 打开音频输出流
    stream = audio.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=44100,
                        output=True)

    # 生成短促的哔声信号
    t = np.linspace(0, duration, int(duration * 44100), False)
    signal = np.sin(frequency * 2 * np.pi * t)

    # 播放哔声
    stream.write(signal.astype(np.float32).tobytes())

    # 关闭音频输出流
    stream.stop_stream()
    stream.close()

    # 关闭Pyaudio对象
    audio.terminate()


def close_window(window):
    window.withdraw()  # 隐藏窗口
    window.quit()  # 销毁窗口对象


mainLoop = True


def actively_exit():
    global mainLoop
    mainLoop = False


# 调用函数获取屏幕分辨率
resolution = get_screen_resolution()
if resolution:
    screen_width, screen_height = resolution
    print(f"屏幕分辨率/Resolution：{screen_width}x{screen_height}")
else:
    screen_width = 100
    screen_height = 100
    print("无法获取屏幕分辨率/Can not get resolution")


detecting = False


def detect_switcher():
    global detecting
    if detecting:
        detecting = False
        alert('已停止')
    else:
        alert('将开始')
        detecting = True


reload = False
reload_time = datetime.now()


def click_ctrl():
    global reload, reload_time
    reload = True
    print('ctrl!', reload)
    beep(0.05, 1200)
    reload_time = datetime.now()
    time.sleep(random.uniform(0.0, 0.1))
    keyboard.press('ctrl')
    time.sleep(random.uniform(0.05, 0.10))
    keyboard.release('ctrl')


def click_ctrl_delay():
    global reload, reload_time
    reload = True
    print('ctrl!', reload)
    beep(0.05, 1200)
    reload_time = datetime.now()
    time.sleep(random.uniform(0.0, 0.1))
    keyboard.press('ctrl')
    time.sleep(random.uniform(0.05, 0.10))
    keyboard.release('ctrl')
    for i in range(0, 12):
        reload = True
        time.sleep(0.125)


def detect_0():
    global reload, reload_time
    icon_position = pyautogui.locateOnScreen('./00.png', confidence=0.90, grayscale=True,
                                             region=(screen_width-490, screen_height-180, screen_width, screen_height))
    if icon_position is not None:
        if not reload:
            print('弹匣空，开始换弹', reload)
            reload = True
            click_ctrl()
        else:
            print("弹匣空，换弹中", reload)
    elif icon_position is None:
        if(datetime.now()-reload_time).total_seconds() > 1:
            reload = False
            print('未探测到空弹匣', reload)
            detect_low()
        else:
            print('空弹匣探测缓冲', reload)


def detect_low():
    icon_position = pyautogui.locateOnScreen('./0.png', confidence=0.90, grayscale=False,
                                             region=(screen_width-200, screen_height-200, screen_width, screen_height))
    if icon_position and not reload:
        beep(0.02, 2500)
        beep(0.02, 2500)
    else:
        time.sleep(0.05)


def detect_enemy():
    icon_position = pyautogui.locateOnScreen('./red.png', confidence=0.90, grayscale=False,
                                             region=(screen_width-650, 0, screen_width, 650))
    if icon_position and not reload:
        beep(0.05, 300)
    else:
        time.sleep(0.05)


# 注册按键事件处理函数
keyboard.add_hotkey('f12', actively_exit)

# 注册按键组合 f9 开关
keyboard.add_hotkey('f9', detect_switcher)

# 注册按键组合 r 主动换弹
def on_key_press(event):
    if event.name == 'r':
        click_ctrl_delay()


keyboard.on_press(on_key_press)

print('----说明|Instruction----')
if is_chinese:
    print("f12-退出/重启程序")
else:
    print("f12 to exit/restart")

# 循环执行程序
while mainLoop:
    if detecting:
        detect_0()
        detect_enemy()
    time.sleep(0.12)
print('exited')
