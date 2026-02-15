import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import math
import numpy as np

plt.rcParams['font.sans-serif'] = 'SimHei'  # 确保中文显示
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

#计算供需匹配度λ和匹配环境Ф
def cal(d,s):
    # 计算余弦值
    cos_val = d/math.sqrt(d**2+s**2)
    # 计算反余弦，得到弧度值
    radian = math.acos(cos_val)
    # 将弧度转换为角度
    angle = math.degrees(radian)
    # 计算供需匹配度
    radians = math.radians(angle - 45)
    λ = math.cos(radians)
    # 计算匹配环境Ф
    Ф = 1
    if angle>45:
        Ф = -1
    # 返回计算结果并保留3位有效数字
    return float(str(λ)[:6]),Ф

# 1、培训级别供需以及可视化
support1 = [91.76,77.65,34.35,9.41]
demand1 = [35.06,50.59,71.76,45.53]
label1 = ['园本培训','区县级培训','省市级培训','国家级培训']
print('#'*50)
print('一级指标: {}\n'.format('培训级别'))
for i in range(len(support1)):
    λ, Ф = cal(demand1[i]/100.0,support1[i]/100.0)
    print('二级指标 {} 的匹配度为: {} 匹配环境为:{}'.format(label1[i],λ, Ф))

# 可视化
# 创建图形
fig, ax = plt.subplots(figsize=(5, 5))
# 绘制45度参考线（y = x）
x_line = np.linspace(-10, max(support1) + 10, 100)
plt.plot(x_line, x_line, 'k-', lw=1)
# 绘制数据点
ax.scatter(demand1, support1, color='black', s=30, zorder=5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_position(('data', 0))   # 左轴移到x=0
ax.spines['bottom'].set_position(('data', 0)) # 下轴移到y=0
ax.spines['bottom'].set_capstyle('round')
ax.spines['left'].set_capstyle('round')
ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)  # X轴箭头
ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)  # Y轴箭头
ax.set_xticks([])
ax.set_yticks([])
ax.text(max(demand1) + 15, 0, 'X', fontweight='bold',fontsize=14, ha='center', va='center')
ax.text(0, max(support1) + 15, 'Y', fontweight='bold',fontsize=14, ha='center', va='center')
x_min, x_max = -10, max(demand1) + 10
y_min, y_max = -10, max(support1) + 10
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_xlabel('')
ax.set_ylabel('')
ax.set_title('')
ax.grid(False)
plt.savefig('培训级别供需.png',dpi=300,bbox_inches='tight',facecolor='white')
plt.show()

# 2、培训频次供需以及可视化
support1 = [1.41,48.24,27.29,8.47,14.59]
demand1 = [0,47.06,37.18,8.47,7.29]
label1 = ['0次(未参与)','1-2 次','3-4次','5-6次','6次及以上']
print('\n'+'#'*50)
print('一级指标: {}\n'.format('年培训频次'))
for i in range(len(support1)):
    λ, Ф = cal(demand1[i],support1[i])
    print('二级指标 {} 的匹配度为: {} 匹配环境为:{}'.format(label1[i],λ, Ф))

# 可视化
# 创建图形
fig, ax = plt.subplots(figsize=(5, 5))
# 绘制45度参考线（y = x）
x_line = np.linspace(-10, max(support1) + 10, 100)
plt.plot(x_line, x_line, 'k-', lw=1)
# 绘制数据点
ax.scatter(demand1, support1, color='black', s=30, zorder=5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_position(('data', 0))   # 左轴移到x=0
ax.spines['bottom'].set_position(('data', 0)) # 下轴移到y=0
ax.spines['bottom'].set_capstyle('round')
ax.spines['left'].set_capstyle('round')
ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)  # X轴箭头
ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)  # Y轴箭头
ax.set_xticks([])
ax.set_yticks([])
ax.text(max(demand1) + 15, 0, 'X', fontweight='bold',fontsize=14, ha='center', va='center')
ax.text(0, max(support1) + 15, 'Y', fontweight='bold',fontsize=14, ha='center', va='center')
x_min, x_max = -10, max(demand1) + 10
y_min, y_max = -10, max(support1) + 10
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_xlabel('')
ax.set_ylabel('')
ax.set_title('')
ax.grid(False)
plt.savefig('培训频次供需.png',dpi=300,bbox_inches='tight',facecolor='white')
plt.show()

# 3、培训地点供需以及可视化
support1 = [88.94,89.18,38.82,16.94,8.24,5.18,22.82]
demand1 = [60.47,70.12,57.41,43.76,30.12,20.47,23.29]
label1 = ['本园内部','本地(县/区内)的其他学校(幼儿园)或培训中心',
          '本地(如S市)内的培训基地或教科研机构',
          '本省内的城市(如省会)的培训场所',
          '省外其他城市','高等院校/科研机构的校园内',
          '通过互联网在线进行(远程培训/网络研修)']
print('\n'+'#'*50)
print('一级指标: {}\n'.format('培训地点'))
for i in range(len(support1)):
    λ, Ф = cal(demand1[i],support1[i])
    print('二级指标 {} 的匹配度为: {} 匹配环境为:{}'.format(label1[i],λ, Ф))

# 可视化
# 创建图形
fig, ax = plt.subplots(figsize=(5, 5))
# 绘制45度参考线（y = x）
x_line = np.linspace(-10, max(support1) + 10, 100)
plt.plot(x_line, x_line, 'k-', lw=1)
# 绘制数据点
ax.scatter(demand1, support1, color='black', s=30, zorder=5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_position(('data', 0))   # 左轴移到x=0
ax.spines['bottom'].set_position(('data', 0)) # 下轴移到y=0
ax.spines['bottom'].set_capstyle('round')
ax.spines['left'].set_capstyle('round')
ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)  # X轴箭头
ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)  # Y轴箭头
ax.set_xticks([])
ax.set_yticks([])
ax.text(max(demand1) + 15, 0, 'X', fontweight='bold',fontsize=14, ha='center', va='center')
ax.text(0, max(support1) + 15, 'Y', fontweight='bold',fontsize=14, ha='center', va='center')
x_min, x_max = -10, max(demand1) + 10
y_min, y_max = -10, max(support1) + 10
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_xlabel('')
ax.set_ylabel('')
ax.set_title('')
ax.grid(False)
plt.savefig('培训地点供需.png',dpi=300,bbox_inches='tight',facecolor='white')
plt.show()

# 4、培训时间供需以及可视化
support1 = [66.12,9.65,71.29,62.12,5.18,16.47]
demand1 = [67.76,5.18,21.41,32.71,4,38.59]
label1 = ['工作日白天','工作日晚上',
          '周末全天或部分时间',
          '寒陆暑假期间',
          '其他法定节假日期间',
          '时间灵活(可自主安排学习进程)']
print('\n'+'#'*50)
print('一级指标: {}\n'.format('培训时间'))
for i in range(len(support1)):
    λ, Ф = cal(demand1[i],support1[i])
    print('二级指标 {} 的匹配度为: {} 匹配环境为:{}'.format(label1[i],λ, Ф))

# 可视化
# 创建图形
fig, ax = plt.subplots(figsize=(5, 5))
# 绘制45度参考线（y = x）
x_line = np.linspace(-10, max(support1) + 10, 100)
plt.plot(x_line, x_line, 'k-', lw=1)
# 绘制数据点
ax.scatter(demand1, support1, color='black', s=30, zorder=5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_position(('data', 0))   # 左轴移到x=0
ax.spines['bottom'].set_position(('data', 0)) # 下轴移到y=0
ax.spines['bottom'].set_capstyle('round')
ax.spines['left'].set_capstyle('round')
ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)  # X轴箭头
ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)  # Y轴箭头
ax.set_xticks([])
ax.set_yticks([])
ax.text(max(demand1) + 15, 0, 'X', fontweight='bold',fontsize=14, ha='center', va='center')
ax.text(0, max(support1) + 15, 'Y', fontweight='bold',fontsize=14, ha='center', va='center')
x_min, x_max = -10, max(demand1) + 10
y_min, y_max = -10, max(support1) + 10
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_xlabel('')
ax.set_ylabel('')
ax.set_title('')
ax.grid(False)
plt.savefig('培训时间供需.png',dpi=300,bbox_inches='tight',facecolor='white')
plt.show()

# 5、培训内容供需以及可视化
support1 = [59.29,80.00,45.18,66.35,38.59,78.59,59.76,43.29]
demand1 = [61.88,68.71,62.82,78.35,56.47,75.53,71.06,59.29]
label1 = ['教育政策法规知识','教师职业道德规范',
          '托班保育技能',
          '家园沟通技巧',
          '数字技术深度应用',
          '游戏活动设计与实施','幼儿心理健康教育',
          '幼小衔接实践策略']
print('\n'+'#'*50)
print('一级指标: {}\n'.format('培训内容'))
for i in range(len(support1)):
    λ, Ф = cal(demand1[i],support1[i])
    print('二级指标 {} 的匹配度为: {} 匹配环境为:{}'.format(label1[i],λ, Ф))

# 可视化
# 创建图形
fig, ax = plt.subplots(figsize=(5, 5))
# 绘制45度参考线（y = x）
x_line = np.linspace(-10, max(support1) + 10, 100)
plt.plot(x_line, x_line, 'k-', lw=1)
# 绘制数据点
ax.scatter(demand1, support1, color='black', s=30, zorder=5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_position(('data', 0))   # 左轴移到x=0
ax.spines['bottom'].set_position(('data', 0)) # 下轴移到y=0
ax.spines['bottom'].set_capstyle('round')
ax.spines['left'].set_capstyle('round')
ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)  # X轴箭头
ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)  # Y轴箭头
ax.set_xticks([])
ax.set_yticks([])
ax.text(max(demand1) + 15, 0, 'X', fontweight='bold',fontsize=14, ha='center', va='center')
ax.text(0, max(support1) + 15, 'Y', fontweight='bold',fontsize=14, ha='center', va='center')
x_min, x_max = -10, max(demand1) + 10
y_min, y_max = -10, max(support1) + 10
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_xlabel('')
ax.set_ylabel('')
ax.set_title('')
ax.grid(False)
plt.savefig('培训内容供需.png',dpi=300,bbox_inches='tight',facecolor='white')
plt.show()

# 6、培训师资供需以及可视化
support1 = [68.71,87.29,58.82,46.59,49.88]
demand1 = [79.76,88.71,54.12,51.29,61.18]
label1 = ['某领域的专家教授','一线优秀教师/园长',
          '教育行政人员(如教育局等相关单位的工作人员)',
          '教育培训机构的培训人员',
          '优秀教研员']
print('\n'+'#'*50)
print('一级指标: {}\n'.format('培训师资'))
for i in range(len(support1)):
    λ, Ф = cal(demand1[i],support1[i])
    print('二级指标 {} 的匹配度为: {} 匹配环境为:{}'.format(label1[i],λ, Ф))

# 可视化
# 创建图形
fig, ax = plt.subplots(figsize=(5, 5))
# 绘制45度参考线（y = x）
x_line = np.linspace(-10, max(support1) + 10, 100)
plt.plot(x_line, x_line, 'k-', lw=1)
# 绘制数据点
ax.scatter(demand1, support1, color='black', s=30, zorder=5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_position(('data', 0))   # 左轴移到x=0
ax.spines['bottom'].set_position(('data', 0)) # 下轴移到y=0
ax.spines['bottom'].set_capstyle('round')
ax.spines['left'].set_capstyle('round')
ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)  # X轴箭头
ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)  # Y轴箭头
ax.set_xticks([])
ax.set_yticks([])
ax.text(max(demand1) + 15, 0, 'X', fontweight='bold',fontsize=14, ha='center', va='center')
ax.text(0, max(support1) + 15, 'Y', fontweight='bold',fontsize=14, ha='center', va='center')
x_min, x_max = -10, max(demand1) + 10
y_min, y_max = -10, max(support1) + 10
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_xlabel('')
ax.set_ylabel('')
ax.set_title('')
ax.grid(False)
plt.savefig('培训师资供需.png',dpi=300,bbox_inches='tight',facecolor='white')
plt.show()





