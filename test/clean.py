import json
import os
import shutil
import datetime

def clean_chat():
    # 定义文件路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    chat_file = os.path.join(script_dir, 'chat.json')
    history_dir = os.path.join(script_dir, 'history')
    
    # 确保history目录存在
    if not os.path.exists(history_dir):
        os.makedirs(history_dir)
    
    # 读取当前的chat.json文件
    with open(chat_file, 'r', encoding='utf-8') as f:
        chat_data = json.load(f)
    
    # 找出system角色的消息
    system_messages = [msg for msg in chat_data if msg.get('role') == 'system']
    
    # 备份当前的chat.json到history目录
    # 使用当前时间创建文件名，格式为chat_MMDDHHMMSS_SS.json
    now = datetime.datetime.now()
    time_str = now.strftime("%m%d%H%M%S_%f")[:13]  # 取毫秒的前两位数字
    backup_file = os.path.join(history_dir, f'chat_{time_str}.json')
    
    # 复制文件到备份目录
    shutil.copy2(chat_file, backup_file)
    
    # 清空chat.json，只保留system角色的消息
    with open(chat_file, 'w', encoding='utf-8') as f:
        json.dump(system_messages, f, ensure_ascii=False, indent=4)
    
    print(f"已将chat.json备份到{backup_file}")
    print(f"已清空chat.json，只保留system角色的消息")

if __name__ == "__main__":
    clean_chat()