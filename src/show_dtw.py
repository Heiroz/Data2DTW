import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
from scipy.interpolate import make_interp_spline
import seaborn as sns

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
    
    # 设置Seaborn样式
    sns.set(style="whitegrid")
    
    # 遍历选中的文件并生成图像
    counter = 0
    for filename in selected_files:
        file_path = os.path.join(input_folder, filename)
        merge_data = pd.read_csv(file_path)
        
        # 设置折线图的透明度
        opacity = 0.8
        
        # 获取数据
        x = merge_data['ElapsedTime']
        y_synthetic = merge_data['PacketSize_synthetic']
        y_actual = merge_data['PacketSize_actual']
        
        # 生成平滑曲线
        x_new = np.linspace(x.min(), x.max(), 300)
        spl_synthetic = make_interp_spline(x, y_synthetic, k=3)
        spl_actual = make_interp_spline(x, y_actual, k=3)
        y_synthetic_smooth = spl_synthetic(x_new)
        y_actual_smooth = spl_actual(x_new)
        
        # 绘制折线图
        plt.figure(figsize=(10, 6))
        
        plt.plot(x_new, y_synthetic_smooth, label='Synthetic Flow', linestyle='-', alpha=opacity, color='b')
        plt.plot(x_new, y_actual_smooth, label='Actual Flow', linestyle='-', alpha=opacity, color='r')
        
        # 设置标签和标题
        plt.xlabel('Time(ms)', fontsize=14)
        plt.ylabel('Bytes', fontsize=14)
        plt.title('Packet Size Comparison', fontsize=16)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        
        # 设置图例
        legend = plt.legend(fontsize=12)
        legend.get_frame().set_alpha(0.5)
        
        # 设置网格线
        plt.grid(True, linestyle='--', alpha=0.6)
        
        # 保存图像
        graph_filename = f"Comparison_{counter}.png"
        plt.savefig(os.path.join(output_folder, graph_filename), bbox_inches='tight')
        plt.close()
        
        counter += 1