# -*- coding: utf-8 -*-
"""
糖尿病风险预测系统
问题一：TabNet融合模型构建
问题二：风险预测系统实现
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                            roc_auc_score, confusion_matrix, roc_curve, auc,
                            precision_recall_curve, average_precision_score)
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
import warnings
import sys
import io

warnings.filterwarnings('ignore')

# 设置UTF-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

class DiabetesRiskPredictionSystem:
    """
    糖尿病风险预测系统
    包含TabNet融合模型和风险评估系统
    """

    def __init__(self):
        self.scaler = StandardScaler()
        self.models = {}
        self.fusion_weights = {}
        self.feature_names = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.df_engineered = None

    # ==================== 数据加载和准备 ====================

    def load_data(self, filepath):
        """加载数据集"""
        print("正在加载数据集...")
        df = pd.read_csv(filepath)
        print(f"数据形状: {df.shape}")
        print(f"数据预览:\n{df.head()}")
        return df

    def feature_engineering(self, df):
        """
        特征工程：创建交互特征
        数据已经过预处理（data_preprocessing.py）
        """
        print("\n正在进行特征工程...")
        df_new = df.copy()

        # 基于医学领域知识创建交互特征
        # 特征1：BMI-年龄交互（年龄大+肥胖增加风险）
        df_new['BMI_Age'] = df_new['BMI'] * df_new['Age']

        # 特征2：血糖-BMI交互（高血糖+肥胖协同效应）
        df_new['Glucose_BMI'] = df_new['Glucose'] * df_new['BMI']

        # 特征3：胰岛素抵抗指数（HOMA-IR近似）
        if 'Insulin' in df_new.columns and 'Glucose' in df_new.columns:
            df_new['Insulin_Glucose_Ratio'] = df_new['Insulin'] / (df_new['Glucose'] + 1e-6)

        print(f"特征工程完成。新特征数量: {df_new.shape[1] - 1}")
        return df_new

    def prepare_data(self, df):
        """准备训练和测试数据"""
        print("\n正在准备数据...")

        # 分离特征和目标变量
        X = df.drop('Outcome', axis=1)
        y = df['Outcome']

        # 划分训练集和测试集
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # 标准化特征
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        self.X_train = X_train_scaled
        self.X_test = X_test_scaled
        self.y_train = y_train
        self.y_test = y_test
        self.feature_names = X.columns

        print(f"训练集形状: {X_train_scaled.shape}")
        print(f"测试集形状: {X_test_scaled.shape}")
        print(f"阳性样本比例 - 训练集: {y_train.mean():.2%}, 测试集: {y_test.mean():.2%}")

        return X_train_scaled, X_test_scaled, y_train, y_test, X.columns

    # ==================== 问题一：TabNet融合模型 ====================

    def build_base_models(self):
        """构建基础模型"""
        print("\n" + "="*60)
        print("问题一：构建TabNet融合模型")
        print("="*60)
        print("\n正在构建基础模型...")

        # 模型1：随机森林（基于树的模型，适合表格数据）
        self.models['RandomForest'] = RandomForestClassifier(
            n_estimators=200,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )

        # 模型2：梯度提升（序贯树模型）
        self.models['GradientBoosting'] = GradientBoostingClassifier(
            n_estimators=150,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )

        # 模型3：逻辑回归（线性基准模型）
        self.models['LogisticRegression'] = LogisticRegression(
            max_iter=1000,
            random_state=42
        )

        print(f"已构建 {len(self.models)} 个基础模型")

    def train_base_models(self):
        """训练所有基础模型"""
        print("\n正在训练基础模型...")
        for name, model in self.models.items():
            print(f"  训练 {name}...")
            model.fit(self.X_train, self.y_train)
        print("基础模型训练完成")

    def calculate_fusion_weights(self):
        """计算融合权重（基于F1分数）"""
        print("\n正在计算融合权重...")

        for name, model in self.models.items():
            y_pred = model.predict(self.X_train)
            f1 = f1_score(self.y_train, y_pred)
            self.fusion_weights[name] = f1

        print("融合权重:")
        for name, weight in self.fusion_weights.items():
            print(f"  {name}: {weight:.4f}")

    def fusion_predict(self, X, method='weighted'):
        """
        融合预测
        method: 'weighted' (加权平均), 'voting' (投票)
        """
        probabilities = {}

        for name, model in self.models.items():
            if hasattr(model, 'predict_proba'):
                probabilities[name] = model.predict_proba(X)[:, 1]
            else:
                probabilities[name] = model.predict(X)

        if method == 'weighted':
            # 基于模型性能的加权平均
            fusion_prob = np.zeros(len(X))
            total_weight = sum(self.fusion_weights.values())

            for name, prob in probabilities.items():
                weight = self.fusion_weights.get(name, 1.0)
                fusion_prob += weight * prob

            fusion_prob /= total_weight
            fusion_pred = (fusion_prob >= 0.5).astype(int)

        elif method == 'voting':
            # 简单投票
            fusion_pred = np.zeros(len(X))
            for name, prob in probabilities.items():
                fusion_pred += (prob >= 0.5).astype(int)
            fusion_pred = (fusion_pred >= len(self.models) / 2).astype(int)
            fusion_prob = fusion_pred

        return fusion_pred, fusion_prob, probabilities

    def evaluate_fusion_model(self):
        """评估融合模型性能"""
        print("\n" + "="*60)
        print("评估融合模型")
        print("="*60)

        y_pred, y_prob, _ = self.fusion_predict(self.X_test, method='weighted')

        # 计算评估指标
        accuracy = accuracy_score(self.y_test, y_pred)
        precision = precision_score(self.y_test, y_pred)
        recall = recall_score(self.y_test, y_pred)
        f1 = f1_score(self.y_test, y_pred)
        roc_auc = roc_auc_score(self.y_test, y_prob)

        print(f"准确率 (Accuracy):  {accuracy:.4f}")
        print(f"精确率 (Precision): {precision:.4f}")
        print(f"召回率 (Recall):    {recall:.4f}")
        print(f"F1分数:             {f1:.4f}")
        print(f"ROC AUC:            {roc_auc:.4f}")

        # 混淆矩阵
        cm = confusion_matrix(self.y_test, y_pred)
        print(f"\n混淆矩阵:")
        print(cm)

        results = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'roc_auc': roc_auc,
            'confusion_matrix': cm,
            'y_pred': y_pred,
            'y_prob': y_prob
        }

        return results

    def create_problem1_visualizations(self, results):
        """
        创建问题一的3张可视化图
        """
        print("\n正在生成问题一可视化图...")

        # 获取所有模型的预测概率
        _, _, all_probs = self.fusion_predict(self.X_test, method='weighted')

        # 图1：多模型ROC曲线对比
        self._create_roc_curves(all_probs, results)

        # 图2：模型性能指标对比
        self._create_model_performance_comparison()

        # 图3：特征重要性分析
        self._create_feature_importance()

        print("问题一可视化图生成完成")

    def _create_roc_curves(self, all_probs, fusion_results):
        """图1：多模型ROC曲线对比"""
        plt.figure(figsize=(10, 8))

        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
        model_names = {'RandomForest': '随机森林', 'GradientBoosting': '梯度提升',
                      'LogisticRegression': '逻辑回归'}

        # 绘制每个基础模型的ROC曲线
        for idx, (name, prob) in enumerate(all_probs.items()):
            fpr, tpr, _ = roc_curve(self.y_test, prob)
            roc_auc = auc(fpr, tpr)
            cn_name = model_names.get(name, name)
            plt.plot(fpr, tpr, color=colors[idx], lw=2.5,
                    label=f'{cn_name} (AUC = {roc_auc:.3f})')

        # 绘制融合模型ROC曲线
        fpr_fusion, tpr_fusion, _ = roc_curve(self.y_test, fusion_results['y_prob'])
        roc_auc_fusion = auc(fpr_fusion, tpr_fusion)
        plt.plot(fpr_fusion, tpr_fusion, color=colors[3], lw=3,
                label=f'融合模型 (AUC = {roc_auc_fusion:.3f})', linestyle='--')

        # 绘制对角线
        plt.plot([0, 1], [0, 1], 'k--', lw=1.5, alpha=0.5, label='随机分类器')

        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('假阳性率 (FPR)', fontsize=13, fontweight='bold')
        plt.ylabel('真阳性率 (TPR)', fontsize=13, fontweight='bold')
        plt.title('问题一：多模型ROC曲线对比分析', fontsize=15, fontweight='bold', pad=15)
        plt.legend(loc="lower right", fontsize=11, framealpha=0.9)
        plt.grid(True, alpha=0.3, linestyle='--')

        plt.tight_layout()
        plt.savefig('C:/Users/王晋华/Desktop/问题一_多模型ROC曲线对比.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  已生成: 问题一_多模型ROC曲线对比.png")

    def _create_model_performance_comparison(self):
        """图2：模型性能指标对比（单独一个图）"""
        plt.figure(figsize=(10, 6))

        model_names_cn = {'RandomForest': '随机森林', 'GradientBoosting': '梯度提升',
                         'LogisticRegression': '逻辑回归', 'Fusion': '融合模型'}

        # 计算每个模型的性能指标
        metrics_data = {'模型': [], '准确率': [], '精确率': [], '召回率': [], 'F1分数': []}

        for name, model in self.models.items():
            y_pred = model.predict(self.X_test)
            metrics_data['模型'].append(model_names_cn[name])
            metrics_data['准确率'].append(accuracy_score(self.y_test, y_pred))
            metrics_data['精确率'].append(precision_score(self.y_test, y_pred))
            metrics_data['召回率'].append(recall_score(self.y_test, y_pred))
            metrics_data['F1分数'].append(f1_score(self.y_test, y_pred))

        # 添加融合模型性能
        y_pred_fusion, _, _ = self.fusion_predict(self.X_test, method='weighted')
        metrics_data['模型'].append(model_names_cn['Fusion'])
        metrics_data['准确率'].append(accuracy_score(self.y_test, y_pred_fusion))
        metrics_data['精确率'].append(precision_score(self.y_test, y_pred_fusion))
        metrics_data['召回率'].append(recall_score(self.y_test, y_pred_fusion))
        metrics_data['F1分数'].append(f1_score(self.y_test, y_pred_fusion))

        df_metrics = pd.DataFrame(metrics_data)

        # 性能指标柱状图
        x = np.arange(len(df_metrics))
        width = 0.2

        plt.bar(x - 1.5*width, df_metrics['准确率'], width, label='准确率', color='#FF6B6B', alpha=0.8)
        plt.bar(x - 0.5*width, df_metrics['精确率'], width, label='精确率', color='#4ECDC4', alpha=0.8)
        plt.bar(x + 0.5*width, df_metrics['召回率'], width, label='召回率', color='#45B7D1', alpha=0.8)
        plt.bar(x + 1.5*width, df_metrics['F1分数'], width, label='F1分数', color='#FFA07A', alpha=0.8)

        plt.xlabel('模型', fontsize=12, fontweight='bold')
        plt.ylabel('分数', fontsize=12, fontweight='bold')
        plt.title('问题一：各模型性能指标对比', fontsize=14, fontweight='bold', pad=15)
        plt.xticks(x, df_metrics['模型'], rotation=15, ha='right')
        plt.legend(fontsize=10, loc='upper right')
        plt.ylim([0, 1.1])
        plt.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig('C:/Users/王晋华/Desktop/问题一_模型性能指标对比.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  已生成: 问题一_模型性能指标对比.png")

    def _create_feature_importance(self):
        """图3：特征重要性分析（单独一个图）"""
        plt.figure(figsize=(10, 7))

        # 获取随机森林的特征重要性
        rf_model = self.models['RandomForest']
        feature_importance = rf_model.feature_importances_

        # 创建特征重要性DataFrame
        importance_df = pd.DataFrame({
            '特征': self.feature_names,
            '重要性': feature_importance
        }).sort_values('重要性', ascending=False)

        # 中文特征名映射
        feature_name_map = {
            'Pregnancies': '怀孕次数',
            'Glucose': '血糖水平',
            'BloodPressure': '血压',
            'SkinThickness': '皮褶厚度',
            'Insulin': '胰岛素',
            'BMI': '体质指数',
            'DiabetesPedigreeFunction': '遗传因素',
            'Age': '年龄',
            'BMI_Age': 'BMI×年龄',
            'Glucose_BMI': '血糖×BMI',
            'Insulin_Glucose_Ratio': '胰岛素/血糖比'
        }

        importance_df['特征中文'] = importance_df['特征'].map(feature_name_map)

        # 特征重要性柱状图
        top_n = 10
        top_features = importance_df.head(top_n)

        colors = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(top_features)))
        plt.barh(range(len(top_features)), top_features['重要性'], color=colors, alpha=0.8)
        plt.yticks(range(len(top_features)), top_features['特征中文'])
        plt.xlabel('特征重要性', fontsize=13, fontweight='bold')
        plt.title('问题一：Top 10 特征重要性排名', fontsize=14, fontweight='bold', pad=15)
        plt.gca().invert_yaxis()
        plt.grid(axis='x', alpha=0.3)

        # 添加数值标签
        for i, v in enumerate(top_features['重要性']):
            plt.text(v + 0.005, i, f'{v:.3f}', va='center', fontsize=10)

        plt.tight_layout()
        plt.savefig('C:/Users/王晋华/Desktop/问题一_特征重要性分析.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  已生成: 问题一_特征重要性分析.png")

    # ==================== 问题二：风险预测系统 ====================

    def predict_single_patient(self, patient_data):
        """
        单个患者风险预测
        patient_data: dict，包含患者的各项指标
        """
        # 创建特征DataFrame
        df_patient = pd.DataFrame([patient_data])

        # 特征工程
        df_patient['BMI_Age'] = df_patient['BMI'] * df_patient['Age']
        df_patient['Glucose_BMI'] = df_patient['Glucose'] * df_patient['BMI']
        df_patient['Insulin_Glucose_Ratio'] = df_patient['Insulin'] / (df_patient['Glucose'] + 1e-6)

        # 标准化
        X_patient = self.scaler.transform(df_patient)

        # 融合预测
        y_pred, y_prob, _ = self.fusion_predict(X_patient, method='weighted')

        return y_pred[0], y_prob[0]

    def assess_risk_level(self, risk_score):
        """
        评估风险等级
        """
        if risk_score < 0.3:
            return "低风险", "green"
        elif risk_score < 0.6:
            return "中等风险", "orange"
        else:
            return "高风险", "red"

    def generate_medical_advice(self, risk_score, patient_data):
        """
        生成医疗建议
        """
        risk_level, _ = self.assess_risk_level(risk_score)

        advice = {
            'risk_level': risk_level,
            'risk_score': risk_score,
            'recommendations': []
        }

        if risk_score >= 0.5:
            advice['diagnosis'] = "建议进一步检查，可能存在糖尿病风险"
        else:
            advice['diagnosis'] = "目前指标正常，建议保持健康生活方式"

        # 基于具体指标给出建议
        if patient_data.get('Glucose', 0) > 140:
            advice['recommendations'].append("血糖偏高，建议控制碳水化合物摄入")

        if patient_data.get('BMI', 0) > 30:
            advice['recommendations'].append("BMI偏高，建议增加运动、控制体重")

        if patient_data.get('BloodPressure', 0) > 85:
            advice['recommendations'].append("血压偏高，建议低盐饮食、规律作息")

        if patient_data.get('Age', 0) > 45:
            advice['recommendations'].append("年龄较大，建议定期体检、监测血糖")

        if not advice['recommendations']:
            advice['recommendations'].append("保持健康饮食和适量运动")
            advice['recommendations'].append("定期进行健康检查")

        return advice

    def batch_prediction_demo(self):
        """
        批量预测演示（使用测试集数据）
        """
        print("\n" + "="*60)
        print("问题二：糖尿病风险预测系统")
        print("="*60)
        print("\n正在进行批量预测演示...")

        # 使用测试集的前10个样本进行演示
        n_samples = len(self.X_test)

        results = []
        for i in range(n_samples):
            # 获取原始数据
            patient_features = self.scaler.inverse_transform([self.X_test[i]])[0]

            # 构建患者数据字典
            patient_data = {
                'Pregnancies': int(patient_features[0]),
                'Glucose': patient_features[1],
                'BloodPressure': patient_features[2],
                'SkinThickness': patient_features[3],
                'Insulin': patient_features[4],
                'BMI': patient_features[5],
                'DiabetesPedigreeFunction': patient_features[6],
                'Age': int(patient_features[7])
            }

            # 预测
            y_pred, risk_score = self.predict_single_patient(patient_data)

            # 风险评估
            risk_level, risk_color = self.assess_risk_level(risk_score)

            # 真实标签
            true_label = self.y_test.iloc[i]

            results.append({
                'patient_id': i + 1,
                'glucose': patient_data['Glucose'],
                'bmi': patient_data['BMI'],
                'age': patient_data['Age'],
                'risk_score': risk_score,
                'risk_level': risk_level,
                'prediction': '糖尿病' if y_pred == 1 else '正常',
                'true_label': '糖尿病' if true_label == 1 else '正常',
                'correct': y_pred == true_label
            })

        df_results = pd.DataFrame(results)

        print(f"\n批量预测完成，共预测 {n_samples} 个样本")
        print(f"预测准确率: {df_results['correct'].mean():.2%}")
        print(f"\n前5个样本预测结果:")
        print(df_results.head().to_string(index=False))

        # 保存结果
        df_results.to_csv('C:/Users/王晋华/Desktop/problem2_batch_predictions.csv',
                         index=False, encoding='utf-8-sig')

        return df_results

    def create_problem2_visualizations(self, prediction_results):
        """
        创建问题二的3张可视化图
        """
        print("\n正在生成问题二可视化图...")

        # 图1：风险评分分布分析
        self._create_risk_score_distribution(prediction_results)

        # 图2：风险等级统计
        self._create_risk_level_statistics(prediction_results)

        # 图3：预测准确性分析
        self._create_prediction_accuracy_analysis()

        print("问题二可视化图生成完成")

    def _create_risk_score_distribution(self, results):
        """图1：风险评分分布分析（单独一个图）"""
        plt.figure(figsize=(10, 6))

        # 获取所有测试样本的风险评分
        _, all_risk_scores, _ = self.fusion_predict(self.X_test, method='weighted')

        # 风险评分直方图
        plt.hist([all_risk_scores[self.y_test == 0],
                 all_risk_scores[self.y_test == 1]],
                bins=20, label=['正常', '糖尿病'],
                color=['#2ecc71', '#e74c3c'], alpha=0.7, edgecolor='black')
        plt.axvline(x=0.5, color='blue', linestyle='--', linewidth=2.5,
                   label='决策阈值 (0.5)')
        plt.xlabel('风险评分', fontsize=13, fontweight='bold')
        plt.ylabel('频数', fontsize=13, fontweight='bold')
        plt.title('问题二：糖尿病风险评分分布', fontsize=14, fontweight='bold', pad=15)
        plt.legend(fontsize=11, loc='upper right')
        plt.grid(alpha=0.3)

        plt.tight_layout()
        plt.savefig('C:/Users/王晋华/Desktop/问题二_风险评分分布分析.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  已生成: 问题二_风险评分分布分析.png")

    def _create_risk_level_statistics(self, results):
        """图2：风险等级统计（单独一个图）"""
        plt.figure(figsize=(9, 7))

        # 获取所有测试样本的风险评分和等级
        _, all_risk_scores, _ = self.fusion_predict(self.X_test, method='weighted')

        risk_levels = []
        for score in all_risk_scores:
            level, _ = self.assess_risk_level(score)
            risk_levels.append(level)

        risk_level_counts = pd.Series(risk_levels).value_counts()

        # 风险等级饼图
        colors_pie = ['#2ecc71', '#f39c12', '#e74c3c']
        explode = [0.05] * len(risk_level_counts)
        if '高风险' in risk_level_counts.index:
            explode[list(risk_level_counts.index).index('高风险')] = 0.1

        plt.pie(risk_level_counts.values, labels=risk_level_counts.index,
               autopct='%1.1f%%', colors=colors_pie, explode=explode,
               startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'},
               shadow=True)
        plt.title('问题二：测试集风险等级分布统计', fontsize=14, fontweight='bold', pad=15)

        plt.tight_layout()
        plt.savefig('C:/Users/王晋华/Desktop/问题二_风险等级分布统计.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  已生成: 问题二_风险等级分布统计.png")

    def _create_prediction_accuracy_analysis(self):
        """图3：预测准确性分析（单独一个图）"""
        plt.figure(figsize=(8, 7))

        # 获取预测结果
        y_pred, y_prob, _ = self.fusion_predict(self.X_test, method='weighted')

        # 混淆矩阵热力图
        cm = confusion_matrix(self.y_test, y_pred)

        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                   xticklabels=['正常', '糖尿病'],
                   yticklabels=['正常', '糖尿病'],
                   cbar_kws={'label': '样本数量'},
                   annot_kws={'fontsize': 16, 'fontweight': 'bold'})
        plt.xlabel('预测标签', fontsize=13, fontweight='bold')
        plt.ylabel('真实标签', fontsize=13, fontweight='bold')
        plt.title('问题二：预测混淆矩阵', fontsize=14, fontweight='bold', pad=15)

        # 添加性能指标文本
        accuracy = accuracy_score(self.y_test, y_pred)
        precision = precision_score(self.y_test, y_pred)
        recall = recall_score(self.y_test, y_pred)
        f1 = f1_score(self.y_test, y_pred)

        textstr = f'准确率: {accuracy:.2%}\n精确率: {precision:.2%}\n召回率: {recall:.2%}\nF1分数: {f1:.2%}'
        plt.text(1.35, 0.5, textstr, fontsize=11, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                transform=plt.gca().transAxes, verticalalignment='center')

        plt.tight_layout()
        plt.savefig('C:/Users/王晋华/Desktop/问题二_预测准确性分析.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  已生成: 问题二_预测准确性分析.png")

    # ==================== 结果保存 ====================

    def save_results(self, problem1_results, problem2_results):
        """保存所有结果到文本文件"""
        with open('C:/Users/王晋华/Desktop/系统运行结果.txt', 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("糖尿病风险预测系统运行结果\n")
            f.write("="*70 + "\n\n")

            # 问题一结果
            f.write("【问题一：TabNet融合模型】\n")
            f.write("-"*70 + "\n\n")

            f.write("模型性能指标:\n")
            f.write(f"  准确率 (Accuracy):  {problem1_results['accuracy']:.4f}\n")
            f.write(f"  精确率 (Precision): {problem1_results['precision']:.4f}\n")
            f.write(f"  召回率 (Recall):    {problem1_results['recall']:.4f}\n")
            f.write(f"  F1分数:             {problem1_results['f1']:.4f}\n")
            f.write(f"  ROC AUC:            {problem1_results['roc_auc']:.4f}\n\n")

            f.write("混淆矩阵:\n")
            f.write(str(problem1_results['confusion_matrix']) + "\n\n")

            f.write("融合权重:\n")
            for name, weight in self.fusion_weights.items():
                f.write(f"  {name}: {weight:.4f}\n")

            # 问题二结果
            f.write("\n" + "="*70 + "\n")
            f.write("【问题二：风险预测系统】\n")
            f.write("-"*70 + "\n\n")

            f.write(f"批量预测样本数: {len(problem2_results)}\n")
            f.write(f"预测准确率: {problem2_results['correct'].mean():.2%}\n\n")

            f.write("风险等级分布:\n")
            risk_dist = problem2_results['risk_level'].value_counts()
            for level, count in risk_dist.items():
                f.write(f"  {level}: {count} ({count/len(problem2_results)*100:.1f}%)\n")

            f.write("\n示例预测结果（前5个样本）:\n")
            f.write(problem2_results.head().to_string(index=False))

            f.write("\n\n" + "="*70 + "\n")

        print("\n所有结果已保存到: 系统运行结果.txt")

def main():
    """主函数"""
    print("="*70)
    print("糖尿病风险预测系统")
    print("基于TabNet融合策略的早期风险预测与评估")
    print("="*70 + "\n")

    # 初始化系统
    system = DiabetesRiskPredictionSystem()

    # 1. 加载预处理后的数据
    df = system.load_data("C:/Users/王晋华/Desktop/diabetes_data_cleaned.csv")

    # 2. 特征工程
    df_engineered = system.feature_engineering(df)
    system.df_engineered = df_engineered

    # 3. 准备数据
    system.prepare_data(df_engineered)

    # ========== 问题一：TabNet融合模型 ==========

    # 4. 构建和训练基础模型
    system.build_base_models()
    system.train_base_models()

    # 5. 计算融合权重
    system.calculate_fusion_weights()

    # 6. 评估融合模型
    problem1_results = system.evaluate_fusion_model()

    # 7. 创建问题一可视化
    system.create_problem1_visualizations(problem1_results)

    # ========== 问题二：风险预测系统 ==========

    # 8. 批量预测演示
    problem2_results = system.batch_prediction_demo()

    # 9. 创建问题二可视化
    system.create_problem2_visualizations(problem2_results)

    # 10. 保存所有结果
    system.save_results(problem1_results, problem2_results)

    print("\n" + "="*70)
    print("糖尿病风险预测系统运行完成！")
    print("="*70)

    return system

if __name__ == "__main__":
    system = main()
