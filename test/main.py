import uiautomator2 as u2
# 将XML转换为JSON
import xmltodict
import json
import os

# 导入所需模块
from jiexiyemian import get_ui_hierarchy
from jiansuo import process_ui_hierarchy_and_save
from largemodel import SparkChat
from screenshot_helper import ScreenshotHelper
# 连接到指定设备
device = u2.connect("emulator-5554")  # 替换为你的设备名称

# 检查设备是否连接成功
if device:
    print("成功连接到设备:", device.serial)  # 打印设备序列号
    
    # 打印设备信息
    device_info = device.device_info
    print("设备信息:")
    print(device_info)
    #  创建并使用SparkChat实例进行对话
    print("\n 开始与大模型对话...")
    spark_chat = SparkChat()
    app_info = input("请输入要测试的Android应用名称: ")
    
    while True:  # 添加循环来持续执行测试
        # 加载历史记录
        # spark_chat.load_history()
        
        # 1. 调用jiexiyemian.py中的函数获取UI层次结构
        #$
        print("\n1. 开始获取UI层次结构...")
        get_ui_hierarchy(device)
    
        # 2. 调用jiansuo.py中的函数处理UI层次结构
        print("\n2. 开始处理UI层次结构...")
        process_ui_hierarchy_and_save()
        print("处理完成，结果已保存到jiansuo.json文件中。")
        
        # 读取jiansuo.json文件获取可点击组件信息
        with open('test/jiansuo.json', 'r', encoding='utf-8') as f:
            clickable_components = json.load(f)
        
        # 构造输入信息
        components_info = str(clickable_components)
        user_input = f"我们要测试的App是: {app_info}。可点击的组件有: {components_info}每次请随机选择不同组件的坐标。如果你的回答与上一次相同，请输出'adb shell input keyevent 4'用于返回上一界面。否则，请输入'adb shell input tap x y'，只输出一行adb code，请不要输出其他文本。"
        
        # 获取AI响应
        response = spark_chat.chat(user_input)
        print("AI响应:", response)
        spark_chat.save_history()
        
        # 从AI响应中提取adb命令
        import re
        # 查找adb shell input tap命令或返回键命令
        tap_pattern = r'adb shell input tap (\d+) (\d+)'
        back_pattern = r'adb shell input keyevent 4'
        tap_match = re.search(tap_pattern, response)
        back_match = re.search(back_pattern, response)
        
        # 获取测试名称
        test_name = app_info.strip()
        if not test_name:
            test_name = "default_test"  
        # 创建ScreenshotHelper实例
        screenshot_helper = ScreenshotHelper(test_name)
        
        if tap_match:
            x, y = tap_match.groups()
            cmd = f"adb shell input tap {x} {y}"
            screenshot_helper.execute_tap_command(cmd)
        elif back_match:
            cmd = "adb shell input keyevent 4"
            screenshot_helper.execute_tap_command(cmd)
        else:
            print("未在AI响应中找到有效的adb命令")
            cmd = ''
            
        # 等待用户输入是否继续
        user_choice = input("\n是否继续测试？(y/n): ")
        if user_choice.lower() != 'y':
            print("测试结束")
            break
       

else:
    print("设备连接失败，请检查设备名称或连接状态。")