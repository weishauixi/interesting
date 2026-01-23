import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings

# 忽略一些无关紧要的警告
warnings.filterwarnings('ignore')

# 设置绘图风格 (支持中文)
sns.set(style="ticks", font_scale=1.1)
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
file_path = r"C:/Users/王晋华/Desktop/EMS-最终版（加对照+未纳入）.xlsx"
df = pd.read_excel(file_path)

# ==========================================
# 1. 数据清洗与变量构建
# ==========================================
data = pd.DataFrame()

# (1) 提取数值变量
# 强制转换为数字，非数字变为NaN
data['VD_Level'] = pd.to_numeric(df['血清VD水平ng/ml'], errors='coerce')
data['AFC'] = pd.to_numeric(df['双侧卵巢窦卵泡数'], errors='coerce')
data['Oocytes_Retrieved'] = pd.to_numeric(df['获卵总数'], errors='coerce')

# 卵子数 (优先用IVF+ICSI列，如果没有则用获卵数)
if '卵子数（IVF+ICSI）' in df.columns:
    data['Oocytes_Mature'] = pd.to_numeric(df['卵子数（IVF+ICSI）'], errors='coerce')
else:
    data['Oocytes_Mature'] = data['Oocytes_Retrieved']

# 2PN数 (IVF + ICSI)
ivf_2pn = pd.to_numeric(df['（IVF受精情况）2PN数'], errors='coerce').fillna(0)
icsi_2pn = pd.to_numeric(df['（ICSI受精情况）2PN数'], errors='coerce').fillna(0)
data['TwoPN'] = ivf_2pn + icsi_2pn

# 优质胚胎数
data['Good_Embryos'] = pd.to_numeric(df['优质胚胎数'], errors='coerce')


# 临床妊娠 (文本转 0/1)
def parse_pregnancy(x):
    if pd.isna(x): return np.nan
    s = str(x)
    if '是' in s or '宫内' in s or '临床妊娠' in s: return 1
    return 0


data['Clinical_Pregnancy'] = df['临床妊娠'].apply(parse_pregnancy)

# (2) 构建分组变量

# A. 总分组：对照组 vs 内异症组
# 逻辑：'内异症or腺肌症or合并' 列有值的为 EMS组，空的为对照组
data['Raw_Subtype'] = df['内异症or腺肌症or合并'].astype(str).replace('nan', '')
data['Group'] = data['Raw_Subtype'].apply(lambda x: 'EMS Group' if len(x.strip()) > 0 else 'Control Group')


# B. VD 分组 (3组国际标准)
def get_vd_status(x):
    if pd.isna(x): return np.nan
    if x < 20:
        return 'Deficiency (<20)'
    elif x < 30:
        return 'Insufficiency (20-30)'
    else:
        return 'Sufficiency (≥30)'


data['VD_Status'] = data['VD_Level'].apply(get_vd_status)
# 设定顺序
vd_order = ['Deficiency (<20)', 'Insufficiency (20-30)', 'Sufficiency (≥30)']


# C. 病症亚型 (清洗名称)
# 统一一下名称，防止空格等影响
def clean_subtype(x):
    if '内异症' in x and '合并' not in x and '腺肌症' not in x: return 'Endometriosis'
    if '腺肌症' in x and '合并' not in x and '内异症' not in x: return 'Adenomyosis'
    if '合并' in x: return 'Combined'
    return np.nan


data['Subtype'] = data['Raw_Subtype'].apply(clean_subtype)

# 定义要分析的结局指标列表
outcomes = ['AFC', 'Oocytes_Retrieved', 'TwoPN', 'Good_Embryos', 'Clinical_Pregnancy']
titles = ['AFC', 'Total Oocytes', '2PN Fertilized', 'Good Embryos', 'Pregnancy Rate']


# ==========================================
# 2. 绘图函数定义 (带P值)
# ==========================================
def add_p_val_bar(ax, df_sub, x, y, x_order=None):
    # 简单的两组比较 P值 (Mann-Whitney)
    if len(df_sub[x].unique()) == 2:
        g1 = df_sub[df_sub[x] == df_sub[x].unique()[0]][y].dropna()
        g2 = df_sub[df_sub[x] == df_sub[x].unique()[1]][y].dropna()
        if len(g1) > 0 and len(g2) > 0:
            s, p = stats.mannwhitneyu(g1, g2)
            y_max = df_sub.groupby(x)[y].mean().max()
            ax.text(0.5, 1.05, f'P={p:.3f}', transform=ax.transAxes, ha='center', color='red' if p < 0.05 else 'black')
    # 多组比较 (ANOVA)
    elif len(df_sub[x].unique()) > 2:
        groups = [d[y].dropna() for g, d in df_sub.groupby(x)]
        if len(groups) > 1:
            s, p = stats.f_oneway(*groups)
            ax.text(0.5, 1.05, f'ANOVA P={p:.3f}', transform=ax.transAxes, ha='center',
                    color='red' if p < 0.05 else 'black')


# ==========================================
# 3. 生成图表
# ==========================================

# --- Figure 1: Control vs EMS ---
fig1 = plt.figure(figsize=(20, 10))
# 布局：上面是VD比较，下面是结局比较
gs = fig1.add_gridspec(2, 5)

# 1.1 VD水平比较 (Boxplot)
ax_vd = fig1.add_subplot(gs[0, 1:4])  # 居中
sns.boxplot(x='Group', y='VD_Level', data=data, palette=['#bdc3c7', '#e74c3c'], ax=ax_vd, width=0.4)
add_p_val_bar(ax_vd, data, 'Group', 'VD_Level')
ax_vd.set_title('Serum Vitamin D Levels: Control vs EMS', fontsize=14)
ax_vd.set_ylabel('Vitamin D (ng/ml)')

# 1.2 结局指标比较 (Barplot)
for i, var in enumerate(outcomes):
    ax = fig1.add_subplot(gs[1, i])
    sns.barplot(x='Group', y=var, data=data, palette=['#bdc3c7', '#e74c3c'], ax=ax, capsize=.1, errorbar='se')

    # 特殊处理妊娠率的P值 (卡方)
    if var == 'Clinical_Pregnancy':
        ct = pd.crosstab(data['Group'], data[var])
        if ct.shape == (2, 2):
            c, p, d, e = stats.chi2_contingency(ct)
            ax.text(0.5, 1.05, f'P={p:.3f}', transform=ax.transAxes, ha='center')
    else:
        add_p_val_bar(ax, data, 'Group', var)

    ax.set_title(titles[i])
    ax.set_xlabel('')
    ax.set_xticklabels(['Control', 'EMS'])

plt.tight_layout()
plt.suptitle('Figure 1: Comparison between Control and EMS Group', y=1.02, fontsize=16, fontweight='bold')
plt.show()

# --- 筛选 EMS 组数据用于后续分析 ---
df_ems = data[data['Group'] == 'EMS Group'].copy()

# --- Figure 2: EMS Group - VD Status Analysis ---
fig2, axes = plt.subplots(1, 5, figsize=(20, 5))
for i, var in enumerate(outcomes):
    ax = axes[i]
    sns.barplot(x='VD_Status', y=var, data=df_ems, order=vd_order, ax=ax, palette='viridis', capsize=.1, errorbar='se')
    add_p_val_bar(ax, df_ems, 'VD_Status', var)
    ax.set_title(titles[i])
    ax.set_xlabel('')
    ax.set_xticklabels(['<20', '20-30', '≥30'])  # 简化标签

plt.tight_layout()
plt.suptitle('Figure 2: Outcomes by Vitamin D Status (EMS Patients Only)', y=1.05, fontsize=16, fontweight='bold')
plt.show()

# --- Figure 3: EMS Group - Disease Subtype Analysis ---
# 仅保留那三类
df_sub = df_ems[df_ems['Subtype'].notna()].copy()
sub_order = ['Endometriosis', 'Adenomyosis', 'Combined']

fig3, axes = plt.subplots(1, 5, figsize=(20, 5))
for i, var in enumerate(outcomes):
    ax = axes[i]
    sns.barplot(x='Subtype', y=var, data=df_sub, order=sub_order, ax=ax, palette='Set2', capsize=.1, errorbar='se')
    add_p_val_bar(ax, df_sub, 'Subtype', var)
    ax.set_title(titles[i])
    ax.set_xlabel('')

plt.tight_layout()
plt.suptitle('Figure 3: Outcomes by Disease Subtype', y=1.05, fontsize=16, fontweight='bold')
plt.show()

# --- Figure 4: Linear Regression Analysis ---
reg_vars = ['AFC', 'Oocytes_Retrieved', 'TwoPN', 'Good_Embryos']
fig4, axes = plt.subplots(1, 4, figsize=(20, 5))

for i, var in enumerate(reg_vars):
    ax = axes[i]
    # 散点 + 回归线
    sns.regplot(x='VD_Level', y=var, data=df_ems, ax=ax, scatter_kws={'alpha': 0.5, 's': 20}, line_kws={'color': 'red'})

    # 计算相关系数
    tmp = df_ems[['VD_Level', var]].dropna()
    if len(tmp) > 2:
        r, p = stats.pearsonr(tmp['VD_Level'], tmp[var])
        ax.text(0.05, 0.9, f'R={r:.3f}\nP={p:.3f}', transform=ax.transAxes,
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    ax.set_title(titles[i])

plt.tight_layout()
plt.suptitle('Figure 4: Correlation between Vitamin D and Outcomes', y=1.05, fontsize=16, fontweight='bold')
plt.show()