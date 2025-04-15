import uiautomator2 as u2
import xmltodict
import json
import os

def get_ui_hierarchy(device):
    """获取UI层次结构并保存为XML和JSON文件
    
    Args:
        device: uiautomator2设备实例
    
    Returns:
        bool: 操作是否成功
    """
    try:
        # 获取UI层次结构
        ui_tree = device.dump_hierarchy(compressed=True, pretty=True)
        
        # 确保test目录存在
        test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '')
        
        # 保存UI层次结构为XML文件
        xml_path = os.path.join(test_dir, 'ui_hierarchy.xml')
        with open(xml_path, 'w', encoding='utf-8') as f:
            f.write(ui_tree)
        
        # 读取XML文件并转换为JSON
        with open(xml_path, 'r', encoding='utf-8') as xml_file:
            # 将XML转换为字典
            data_dict = xmltodict.parse(xml_file.read())
            
            # 将字典转换为JSON字符串
            data_str = json.dumps(data_dict, indent=4, ensure_ascii=False)
        
        # 将JSON字符串写入到文件
        json_path = os.path.join(test_dir, 'ui_hierarchy.json')
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json_file.write(data_str)
        return True
    
    except Exception as e:
        print(f"处理UI层次结构时发生错误: {str(e)}")
        return False

def main():
    # 这里仅作为示例，实际使用时应该从其他文件调用get_ui_hierarchy函数
    device = u2.connect("emulator-5554")
    if device:
        get_ui_hierarchy(device)
    else:
        print("设备连接失败，请检查设备名称或连接状态。")

if __name__ == '__main__':
    main()