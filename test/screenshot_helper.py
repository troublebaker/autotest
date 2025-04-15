import os
import subprocess
import time
from PIL import Image, ImageDraw
import re

class ScreenshotHelper:
    """
    用于在执行adb点击命令时截取屏幕并在点击位置绘制圆形标记的工具类
    支持普通adb命令和指定设备ID的adb命令
    """
    
    def __init__(self, test_name):
        """
        初始化ScreenshotHelper类
        
        Args:
            test_name (str): 测试名称，用于创建保存截图的目录
        """
        if not test_name:
            raise ValueError("测试名称不能为空")
            
        self.test_name = test_name
        self.screenshot_dir = os.path.join("test", "screenshot", test_name)
        
        # 确保截图目录存在
        os.makedirs(self.screenshot_dir, exist_ok=True)
    
    def execute_tap_command(self, cmd):
        """
        先截取屏幕，然后执行adb命令（支持点击和返回键），并在点击位置绘制标记
        
        Args:
            cmd (str): adb命令，支持以下格式：
                - "adb shell input tap {x} {y}"
                - "adb shell input keyevent 4"（返回键）
            
        Returns:
            bool: 操作是否成功
        """
        try:
            # 检查是否是返回键命令
            back_match = re.search(r'adb(?:\s+-s\s+[\w\.:]*)? shell input keyevent 4', cmd)
            if back_match:
                # 对于返回键，我们只需要截图，不需要绘制标记
                timestamp = time.strftime("%Y%m%d_%H_%M_%S")
                screenshot_path = os.path.join(self.screenshot_dir, f"{timestamp}.png")
                
                # 使用adb命令截图并保存到本地
                subprocess.run(f"adb exec-out screencap -p > {screenshot_path}", shell=True, check=True)
                
                # 执行返回键命令
                print(f"执行命令: {cmd}")
                subprocess.run(cmd, shell=True, check=True)
                
                # 等待一小段时间确保操作完成
                time.sleep(0.5)
                
                print(f"截图已保存到: {screenshot_path}")
                return True
            
            # 如果不是返回键命令，则尝试解析点击坐标
            tap_match = re.search(r'adb(?:\s+-s\s+[\w\.:]*)? shell input tap (\d+) (\d+)', cmd)
            if not tap_match:
                print("无效的adb命令格式")
                return False
                
            x, y = map(int, tap_match.groups())
            
            # 先截取屏幕
            # 使用简洁的时间格式：年月日_时_分_秒
            timestamp = time.strftime("%Y%m%d_%H_%M_%S")
            screenshot_path = os.path.join(self.screenshot_dir, f"{timestamp}.png")
            
            # 使用adb命令截图并保存到本地
            subprocess.run(f"adb exec-out screencap -p > {screenshot_path}", shell=True, check=True)
            
            # 在截图上绘制圆形标记
            self._draw_circle_on_screenshot(screenshot_path, x, y, 50)
            
            # 执行adb命令
            print(f"执行命令: {cmd}")
            subprocess.run(cmd, shell=True, check=True)
            
            # 等待一小段时间确保点击操作完成
            time.sleep(0.5)
            
            print(f"截图已保存到: {screenshot_path}")
            return True
            
        except Exception as e:
            print(f"执行点击命令时发生错误: {str(e)}")
            return False
    
    def _draw_circle_on_screenshot(self, image_path, x, y, radius):
        """
        在截图上绘制圆形标记
        
        Args:
            image_path (str): 截图文件路径
            x (int): 圆心x坐标
            y (int): 圆心y坐标
            radius (int): 圆形半径
        """
        try:
            # 打开图片
            img = Image.open(image_path)
            draw = ImageDraw.Draw(img)
            
            # 绘制圆形
            draw.ellipse((x-radius, y-radius, x+radius, y+radius), outline="red", width=8)
            
            # 保存修改后的图片
            img.save(image_path)
            
        except Exception as e:
            print(f"在截图上绘制圆形时发生错误: {str(e)}")

# 使用示例
if __name__ == "__main__":
    try:
        # 导入uiautomator2库
        import uiautomator2 as u2
        
        # 连接到127.0.0.1:7555模拟器
        print("正在连接到127.0.0.1:7555模拟器...")
        d = u2.connect("127.0.0.1:7555")
        print(f"成功连接到设备: {d.device_info['model']}")
        
        # 创建ScreenshotHelper实例
        helper = ScreenshotHelper("test1")
        
        # 执行adb点击命令
        # 可以执行多个点击命令进行测试
        print("开始执行测试点击操作...")
        cmd = "adb -s 127.0.0.1:7555 shell input tap 500 800"
        helper.execute_tap_command(cmd)
        
        # 可以添加更多的测试点击
        # cmd = "adb -s 127.0.0.1:7555 shell input tap 300 500"
        # helper.execute_tap_command(cmd)
        
        print("测试完成!")
        
    except Exception as e:
        print(f"测试过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()