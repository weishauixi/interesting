# -*- coding: utf-8 -*-
"""
Data Preprocessing for Diabetes Dataset
处理缺失值、异常值、数据标准化等
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
import sys
import io

# 设置标准输出编码为utf-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

def load_raw_data():
    """加载原始数据"""
    print("="*60)
    print("步骤1：加载原始数据")
    print("="*60)

    df = pd.read_csv("C:/Users/王晋华/Desktop/diabetes_data.csv")
    print(f"原始数据形状: {df.shape}")
    print(f"\n前5行数据:\n{df.head()}")

    return df

def analyze_data_quality(df):
    """分析数据质量"""
    print("\n" + "="*60)
    print("步骤2：数据质量分析")
    print("="*60)

    # 检查缺失值
    missing = df.isnull().sum()
    print(f"\n缺失值统计:\n{missing}")

    # 检查零值（医学上不合理的零值）
    zero_columns = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']

    print("\n医学上不合理的零值统计:")
    zero_stats = {}
    for col in zero_columns:
        zero_count = (df[col] == 0).sum()
        zero_percentage = (zero_count / len(df)) * 100
        zero_stats[col] = {'count': zero_count, 'percentage': zero_percentage}
        print(f"{col}: {zero_count} ({zero_percentage:.2f}%)")

    # 保存质量分析结果
    with open("C:/Users/王晋华/Desktop/data_quality_report.txt", "w", encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("数据质量分析报告\n")
        f.write("="*60 + "\n\n")

        f.write(f"总样本数: {len(df)}\n")
        f.write(f"特征数: {df.shape[1]}\n\n")

        f.write("缺失值统计:\n")
        f.write(str(missing) + "\n\n")

        f.write("不合理零值统计:\n")
        for col, stats in zero_stats.items():
            f.write(f"{col}: {stats['count']} ({stats['percentage']:.2f}%)\n")

    return zero_stats

def handle_zero_values(df):
    """处理不合理的零值"""
    print("\n" + "="*60)
    print("步骤3：处理不合理的零值")
    print("="*60)

    df_cleaned = df.copy()

    # 需要处理零值的列（排除Pregnancies和Outcome）
    zero_columns = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']

    replacement_values = {}
    for col in zero_columns:
        # 计算非零值的中位数
        non_zero_values = df_cleaned[df_cleaned[col] != 0][col]
        median_value = non_zero_values.median()
        replacement_values[col] = median_value

        # 用中位数替换零值
        zero_mask = df_cleaned[col] == 0
        df_cleaned.loc[zero_mask, col] = median_value

        replaced_count = zero_mask.sum()
        print(f"{col}: 替换 {replaced_count} 个零值，使用中位数 {median_value:.2f}")

    # 保存处理后的数据
    df_cleaned.to_csv("C:/Users/王晋华/Desktop/diabetes_data_cleaned.csv", index=False, encoding='utf-8-sig')
    print(f"\n清洗后的数据已保存到: diabetes_data_cleaned.csv")

    return df_cleaned, replacement_values

def detect_outliers(df):
    """检测异常值（使用IQR方法）"""
    print("\n" + "="*60)
    print("步骤4：异常值检测（IQR方法）")
    print("="*60)

    outlier_report = {}

    # 对数值型特征进行异常值检测
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    numeric_columns.remove('Outcome')  # 排除目标变量

    for col in numeric_columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        outlier_count = len(outliers)
        outlier_percentage = (outlier_count / len(df)) * 100

        outlier_report[col] = {
            'count': outlier_count,
            'percentage': outlier_percentage,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound
        }

        print(f"{col}: {outlier_count} 个异常值 ({outlier_percentage:.2f}%)")
        print(f"  正常范围: [{lower_bound:.2f}, {upper_bound:.2f}]")

    # 保存异常值检测报告
    with open("C:/Users/王晋华/Desktop/outlier_detection_report.txt", "w", encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("异常值检测报告（IQR方法）\n")
        f.write("="*60 + "\n\n")

        for col, report in outlier_report.items():
            f.write(f"\n{col}:\n")
            f.write(f"  异常值数量: {report['count']}\n")
            f.write(f"  异常值比例: {report['percentage']:.2f}%\n")
            f.write(f"  正常范围: [{report['lower_bound']:.2f}, {report['upper_bound']:.2f}]\n")

    return outlier_report

def create_preprocessing_visualizations(df_original, df_cleaned):
    """创建数据预处理前后对比可视化"""
    print("\n" + "="*60)
    print("步骤5：生成数据预处理可视化图")
    print("="*60)

    # 图1：数据清洗前后对比（零值处理）
    zero_columns = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 清洗前零值统计
    zero_counts_before = [((df_original[col] == 0).sum() / len(df_original) * 100) for col in zero_columns]
    # 清洗后零值统计（应该都是0）
    zero_counts_after = [((df_cleaned[col] == 0).sum() / len(df_cleaned) * 100) for col in zero_columns]

    x = np.arange(len(zero_columns))
    width = 0.35

    axes[0].bar(x - width/2, zero_counts_before, width, label='清洗前', color='#e74c3c', alpha=0.8)
    axes[0].bar(x + width/2, zero_counts_after, width, label='清洗后', color='#2ecc71', alpha=0.8)
    axes[0].set_xlabel('特征', fontsize=12)
    axes[0].set_ylabel('零值比例 (%)', fontsize=12)
    axes[0].set_title('数据清洗前后零值比例对比', fontsize=14, fontweight='bold')
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(zero_columns, rotation=45, ha='right')
    axes[0].legend()
    axes[0].grid(axis='y', alpha=0.3)

    # 数据完整性改善
    completeness_before = 100 - (df_original[zero_columns] == 0).any(axis=1).sum() / len(df_original) * 100
    completeness_after = 100

    categories = ['清洗前', '清洗后']
    completeness = [completeness_before, completeness_after]
    colors = ['#e74c3c', '#2ecc71']

    axes[1].bar(categories, completeness, color=colors, alpha=0.8, width=0.5)
    axes[1].set_ylabel('数据完整性 (%)', fontsize=12)
    axes[1].set_title('数据完整性提升情况', fontsize=14, fontweight='bold')
    axes[1].set_ylim([0, 105])
    axes[1].grid(axis='y', alpha=0.3)

    # 在柱子上添加数值标签
    for i, v in enumerate(completeness):
        axes[1].text(i, v + 1, f'{v:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')

    plt.tight_layout()
    plt.savefig('C:/Users/王晋华/Desktop/数据预处理_零值处理对比分析.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("已生成: 数据预处理_零值处理对比分析.png")

    # 图2：数据分布对比（处理前后）
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    axes = axes.flatten()

    comparison_features = ['Glucose', 'BloodPressure', 'BMI', 'Insulin', 'SkinThickness', 'Age']

    for idx, feature in enumerate(comparison_features):
        # 清洗前数据（移除零值以便可视化）
        data_before = df_original[df_original[feature] != 0][feature] if feature in zero_columns else df_original[feature]
        # 清洗后数据
        data_after = df_cleaned[feature]

        axes[idx].hist(data_before, bins=30, alpha=0.5, label='清洗前', color='#e74c3c', edgecolor='black')
        axes[idx].hist(data_after, bins=30, alpha=0.5, label='清洗后', color='#2ecc71', edgecolor='black')
        axes[idx].set_xlabel(feature, fontsize=10)
        axes[idx].set_ylabel('频数', fontsize=10)
        axes[idx].set_title(f'{feature} 分布对比', fontsize=11, fontweight='bold')
        axes[idx].legend()
        axes[idx].grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig('C:/Users/王晋华/Desktop/数据预处理_特征分布对比分析.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("已生成: 数据预处理_特征分布对比分析.png")

def generate_statistics_comparison(df_original, df_cleaned):
    """生成预处理前后的统计对比"""
    print("\n" + "="*60)
    print("步骤6：生成统计对比报告")
    print("="*60)

    numeric_columns = df_original.select_dtypes(include=[np.number]).columns.tolist()
    numeric_columns.remove('Outcome')

    with open("C:/Users/王晋华/Desktop/preprocessing_statistics_comparison.txt", "w", encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("数据预处理前后统计对比\n")
        f.write("="*60 + "\n\n")

        for col in numeric_columns:
            f.write(f"\n特征: {col}\n")
            f.write("-" * 40 + "\n")

            # 清洗前统计
            f.write("清洗前:\n")
            f.write(f"  均值: {df_original[col].mean():.2f}\n")
            f.write(f"  中位数: {df_original[col].median():.2f}\n")
            f.write(f"  标准差: {df_original[col].std():.2f}\n")
            f.write(f"  最小值: {df_original[col].min():.2f}\n")
            f.write(f"  最大值: {df_original[col].max():.2f}\n")

            # 清洗后统计
            f.write("\n清洗后:\n")
            f.write(f"  均值: {df_cleaned[col].mean():.2f}\n")
            f.write(f"  中位数: {df_cleaned[col].median():.2f}\n")
            f.write(f"  标准差: {df_cleaned[col].std():.2f}\n")
            f.write(f"  最小值: {df_cleaned[col].min():.2f}\n")
            f.write(f"  最大值: {df_cleaned[col].max():.2f}\n")

            # 变化情况
            mean_change = ((df_cleaned[col].mean() - df_original[col].mean()) / df_original[col].mean() * 100)
            f.write(f"\n均值变化: {mean_change:+.2f}%\n")

    print("统计对比报告已保存到: preprocessing_statistics_comparison.txt")

def main():
    """主函数"""
    print("\n" + "="*60)
    print("糖尿病数据集预处理程序")
    print("="*60 + "\n")

    # 1. 加载原始数据
    df_original = load_raw_data()

    # 2. 分析数据质量
    zero_stats = analyze_data_quality(df_original)

    # 3. 处理零值
    df_cleaned, replacement_values = handle_zero_values(df_original)

    # 4. 检测异常值
    outlier_report = detect_outliers(df_cleaned)

    # 5. 生成可视化
    create_preprocessing_visualizations(df_original, df_cleaned)

    # 6. 生成统计对比
    generate_statistics_comparison(df_original, df_cleaned)

    # 7. 输出最终摘要
    print("\n" + "="*60)
    print("数据预处理完成摘要")
    print("="*60)
    print(f"原始数据形状: {df_original.shape}")
    print(f"清洗后数据形状: {df_cleaned.shape}")
    print(f"\n处理的零值数量:")
    total_zeros = sum([stats['count'] for stats in zero_stats.values()])
    print(f"  总计: {total_zeros}")
    print(f"\n生成的文件:")
    print("  - diabetes_data_cleaned.csv (清洗后的数据)")
    print("  - data_quality_report.txt (数据质量报告)")
    print("  - outlier_detection_report.txt (异常值检测报告)")
    print("  - preprocessing_statistics_comparison.txt (统计对比)")
    print("  - 数据预处理_零值处理对比分析.png")
    print("  - 数据预处理_特征分布对比分析.png")
    print("\n" + "="*60)
    print("数据预处理流程全部完成！")
    print("="*60)

if __name__ == "__main__":
    main()
