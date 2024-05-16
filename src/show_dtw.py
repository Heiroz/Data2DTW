import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random

def generate_images(input_folder, output_folder, image_num):
    # 创建输出文件夹（如果不存在）
    os.makedirs(output_folder, exist_ok=True)

    # 获取文件夹中的所有文件
    files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
    
    # 如果文件数量小于 image_num，生成所有文件的图像
    if len(files) < image_num:
        selected_files = files
    else:
        selected_files = random.sample(files, image_num)
    
    # 遍历选中的文件并生成图像
    counter = 0
    for filename in selected_files:
        file_path = os.path.join(input_folder, filename)
        merge_data = pd.read_csv(file_path)
        
        # 设置柱状图的透明度
        opacity = 0.4
        
        # 设置 X 轴位置
        indices = np.arange(len(merge_data['ElapsedTime']))
        
        # 绘制柱状图
        plt.figure(figsize=(10, 6))
        
        bar1 = plt.bar(indices, merge_data['PacketSize_synthetic'], alpha=opacity, color='b', label='Synthetic Flow')
        bar2 = plt.bar(indices, merge_data['PacketSize_actual'], alpha=opacity, color='r', label='Actual Flow')
        
        # 设置标签和标题
        plt.xlabel('Time(ms)')
        plt.ylabel('Bytes')
        plt.title('Packet Size Comparison')
        plt.xticks(indices, merge_data['ElapsedTime'])
        plt.legend()
        plt.grid(False)
        
        # 保存图像
        graph_filename = f"Comparison_{counter}.png"
        plt.savefig(os.path.join(output_folder, graph_filename))
        plt.close()
        
        counter += 1