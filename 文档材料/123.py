import os
import shutil

# 1. 定义分类标准（映射关系）
# 格式： "大类名称": ["小类1", "小类2", ...]
CATEGORY_MAP = {
    "农林牧渔大类": ["农业类", "林业类", "畜牧业类", "渔业类"],
    "资源环境与安全大类": ["资源勘查类", "地质类", "测绘地理信息类", "石油与天然气类", "煤炭类", "金属与非金属矿类", "环境保护类", "安全类"],
    "能源动力与材料大类": ["电力技术类", "热能与发电工程类", "新能源发电工程类", "黑色金属材料类", "有色金属材料类", "非金属材料类", "建筑材料类"],
    "土木建筑大类": ["建筑设计类", "城乡规划与管理类", "土建施工类", "建筑设备类", "建设工程管理类", "市政工程类", "房地产类"],
    "水利大类": ["水文水资源类", "水利工程与管理类", "水土保持与水环境类"],
    "装备制造大类": ["机械设计制造类", "机电设备类", "自动化类", "轨道装备类", "船舶与海洋工程装备类", "航空装备类", "汽车制造类"],
    "生物与化工大类": ["生物技术类", "化工技术类"],
    "轻工纺织大类": ["轻化工类", "印刷类", "纺织服装类"],
    "食品药品与粮食大类": ["食品类", "药品与医疗器械类", "粮食类"],
    "交通运输大类": ["铁道运输类", "道路运输类", "水上运输类", "航空运输类", "城市轨道交通类", "邮政类"],
    "电子与信息大类": ["电子信息类", "计算机类", "通信类"],
    "医药卫生大类": ["临床医学类", "护理类", "药学类", "中医药类", "医学技术类", "康复治疗类", "公共卫生与卫生管理类", "健康管理与促进类", "眼视光类"],
    "财经商贸大类": ["财政税务类", "金融类", "财务会计类", "统计类", "经济贸易类", "工商管理类", "电子商务类", "物流类"],
    "旅游大类": ["旅游类", "餐饮类"],
    "文化艺术大类": ["艺术设计类", "表演艺术类", "民族文化艺术类", "文化服务类"],
    "新闻传播大类": ["新闻出版类", "广播影视类"],
    "教育与体育大类": ["教育类", "语言类", "体育类"],
    "公安与司法大类": ["法律实务类", "法律执行类", "司法技术类", "安全防范类"],
    "公共管理与服务大类": ["公共事业类", "公共管理类", "公共服务类", "文秘类"]
}

# 源文件夹名称
SOURCE_FOLDER = "带划分文件"

def main():
    # 获取当前脚本所在的目录
    base_dir = os.getcwd()
    source_path = os.path.join(base_dir, SOURCE_FOLDER)

    # 检查源文件夹是否存在
    if not os.path.exists(source_path):
        print(f"错误：找不到文件夹 '{SOURCE_FOLDER}'，请确保脚本和该文件夹在同一目录下。")
        return

    print("正在构建索引...")
    
    # 构建一个反向查找字典： { "农业类": "农林牧渔大类", ... }
    small_to_big = {}
    for big_cat, small_list in CATEGORY_MAP.items():
        for small in small_list:
            small_to_big[small] = big_cat

    print(f"索引构建完成，准备开始整理 '{SOURCE_FOLDER}' 中的文件...")
    
    # 遍历“带划分文件”里的所有内容
    items = os.listdir(source_path)
    moved_count = 0

    for item_name in items:
        # 这里的 item_name 可能是 "农业类" (文件夹) 或者 "农业类.zip" (文件)
        # 我们需要匹配文件名中是否包含小类名称
        
        target_big_category = None
        
        # 尝试匹配
        # 优先全字匹配（防止“农业类”匹配到“现代农业类”等情况，虽然这里列表很标准）
        # 如果你的文件名带有后缀（如 .zip），需要去掉后缀再匹配
        name_without_ext = os.path.splitext(item_name)[0]
        
        if name_without_ext in small_to_big:
            target_big_category = small_to_big[name_without_ext]
        
        # 如果找到了归属的大类
        if target_big_category:
            # 构建源路径和目标路径
            src_item_path = os.path.join(source_path, item_name)
            dest_folder_path = os.path.join(base_dir, target_big_category)
            dest_item_path = os.path.join(dest_folder_path, item_name)

            # 检查大类文件夹是否存在，不存在则创建（虽然你说已经有了，但加个保险）
            if not os.path.exists(dest_folder_path):
                print(f"  [提示] 创建大类文件夹: {target_big_category}")
                os.makedirs(dest_folder_path)

            try:
                # 移动文件/文件夹
                shutil.move(src_item_path, dest_item_path)
                print(f"  [成功] 将 '{item_name}' 移动到 -> '{target_big_category}'")
                moved_count += 1
            except Exception as e:
                print(f"  [失败] 移动 '{item_name}' 时出错: {e}")
        else:
            print(f"  [跳过] '{item_name}' 不在分类列表中")

    print(f"\n整理完成！共移动了 {moved_count} 个项目。")

if __name__ == "__main__":
    main()