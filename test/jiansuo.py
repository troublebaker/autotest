import json
import os

def process_ui_hierarchy_and_save():
    # 确保当前目录是脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 读取JSON文件
    ui_hierarchy_path = os.path.join(script_dir, 'ui_hierarchy.json')
    with open(ui_hierarchy_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    clickable_components = {}
    
    def traverse_node(node):
        # 如果是字典类型，检查是否有@clickable属性
        if isinstance(node, dict):
            # 检查是否是可点击的组件
            if node.get('@clickable') == 'true':
                # 获取组件名称（可能在@text或其他属性中）
                name = node.get('@text', '')
                if not name:
                    name = node.get('@content-desc', '')
                if not name:
                    name = node.get('@resource-id', '')
                
                # 获取bounds信息
                bounds = node.get('@bounds', '')
                
                # 如果有bounds信息，将组件添加到字典中
                if bounds:
                    # 使用名称作为键，如果名称为空则使用bounds作为键
                    key = name if name else bounds
                    clickable_components[key] = bounds
            
            # 递归遍历所有子节点
            for value in node.values():
                traverse_node(value)
        # 如果是列表类型，遍历列表中的每个元素
        elif isinstance(node, list):
            for item in node:
                traverse_node(item)
    
    # 开始遍历
    traverse_node(data)
    
    # 将结果保存到jiansuo.json文件
    jiansuo_path = os.path.join(script_dir, 'jiansuo.json')
    with open(jiansuo_path, 'w', encoding='utf-8') as f:
        json.dump(clickable_components, f, ensure_ascii=False, indent=4)

def main():
    # 处理UI层次结构并保存结果
    process_ui_hierarchy_and_save()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    jiansuo_path = os.path.join(script_dir, 'jiansuo.json')
    # print(f"处理完成，结果已保存到{jiansuo_path}文件中。")

if __name__ == '__main__':
    main()