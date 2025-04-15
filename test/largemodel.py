# coding: utf-8
import SparkApi
import time

class SparkChat:
    def load_history(self):
        """从chat.json文件加载对话历史"""
        import json
        import os
        
        # 获取当前文件所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'chat.json')
        
        # 如果文件存在，则从文件加载对话历史
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    loaded_history = json.load(f)
                    
                    # 保留初始system消息模板
                    system_template = next((msg for msg in self.conversation_history if msg["role"] == "system"), None)
                    
                    # 合并历史记录：保留文件中的用户对话，保持system模板在最前
                    self.conversation_history = [
                        msg for msg in loaded_history 
                        if msg.get("role") != "system"
                    ]
                    
                    if system_template:
                        self.conversation_history.insert(0, system_template)
                    
            except json.JSONDecodeError:
                # 如果文件格式错误，保持默认对话历史
                pass

    def __init__(self, appid="4f4cb296", api_secret="MjdmMTE3NGFkYzM4MjMwYjY4ZGUzM2Qw", 
                 api_key="44017742df23497f6a709e708f96986b", domain="4.0Ultra",
                 spark_url="wss://spark-api.xf-yun.com/v4.0/chat"):
        self.appid = appid
        self.api_secret = api_secret
        self.api_key = api_key
        self.domain = domain
        self.spark_url = spark_url
        #默认对话历史
        self.conversation_history = [
            {"role": "system",
             "content": "> Instruction: • Now that you are an automated testing program for Android software, what you have to do is test the functionality of the software as completely as possible. • I will tell you the information of the current program interface by asking questions and you will tell me the next step on the test by answering. > Prompt: • When you encounter components with similar names, you can look at them as the same category and test one or more of them. > In-Context Learning: • We want to test the App: {}. There are clickable components: {}. Return the bounds of the component. Use the adb code. • Return the option as the adb code like 'adb shell input tap x y'. Only return the adb code. Don't return other text."},
           
            {"role": "user", "content": "你会做什么"}
        ]
        #尝试加载历史对话记录
        self.load_history()

    def add_message(self, role, content):
        """添加新的对话消息到历史记录中"""
        message = {"role": role, "content": content}
        self.conversation_history.append(message)
        return self.conversation_history

    def get_history_length(self):
        """计算对话历史的总字符长度"""
        return sum(len(msg["content"]) for msg in self.conversation_history)

    def trim_history(self):
        """如果对话历史超过8000字符，从头开始删除消息"""
        while self.get_history_length() > 8000:
            del self.conversation_history[0]
        return self.conversation_history

    def chat(self, user_input):
        """处理用户输入并获取AI响应"""
        # 重新加载对话历史，确保获取最新记录
        self.load_history()
        # 添加用户输入到对话历史
        self.add_message("user", user_input)
        # 确保对话历史不超过限制
        self.trim_history()
        # 重置SparkApi的answer
        SparkApi.answer = ""
        # 调用SparkApi获取响应
        SparkApi.main(self.appid, self.api_key, self.api_secret, 
                     self.spark_url, self.domain, self.conversation_history)
        # 将AI的回答添加到对话历史
        self.add_message("assistant", SparkApi.answer)
        return SparkApi.answer

    def save_history(self):
        """将对话历史保存到chat.json文件中"""
        import json
        import os
        
        # 获取当前文件所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'chat.json')
        
        # 将对话历史保存到文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.conversation_history, f, ensure_ascii=False, indent=4)

def main():
    # 创建SparkChat实例
    spark_chat = SparkChat()
    
    # 开始对话循环
    while True:
        user_input = input("\n我:")
        print("星火:", end="")
        response = spark_chat.chat(user_input)
        # 保存对话历史
        spark_chat.save_history()

if __name__ == '__main__':
    main()




