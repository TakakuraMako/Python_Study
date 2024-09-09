import numpy as np
import pandas as pd

# 设置模拟次数
num_simulations = 10000

def monte_carlo_reject(p_actual, p_threshold, confidence_level, initial_sample_size=30):
    """
    蒙特卡洛模拟：判断在实际次品率大于标称值时，能否以指定的信度拒收该批次
    """
    sample_size = initial_sample_size
    while True:
        reject_count = 0
        for _ in range(num_simulations):
            # 随机生成次品情况
            defects = np.random.binomial(sample_size, p_actual)
            # 计算检测到的次品率
            detected_defect_rate = defects / sample_size
            # 判定为拒收（检测到的次品率超过标称值）
            if detected_defect_rate > p_threshold:
                reject_count += 1
        
        # 计算拒收概率
        reject_probability = reject_count / num_simulations
        
        # 判断拒收概率是否达到信度要求
        if reject_probability >= confidence_level:
            
            return sample_size, reject_probability
        else:
            # 增加样本大小继续测试
            sample_size += 1


def monte_carlo_accept(p_actual, p_threshold, confidence_level, initial_sample_size=30):
    """
    蒙特卡洛模拟：判断在实际次品率不超过标称值时，能否以指定的信度接收该批次
    """
    sample_size = initial_sample_size
    while True:
        accept_count = 0
        for _ in range(num_simulations):
            # 随机生成次品情况
            defects = np.random.binomial(sample_size, p_actual)
            # 计算检测到的次品率
            detected_defect_rate = defects / sample_size
            # 判定为接收（检测到的次品率不超过标称值）
            if detected_defect_rate <= p_threshold:
                accept_count += 1
        
        # 计算接收概率
        accept_probability = accept_count / num_simulations
        
        # 判断接收概率是否达到信度要求
        if accept_probability >= confidence_level:
            return sample_size, accept_probability
        else:
            # 增加样本大小继续测试
            sample_size += 1


# 情况1：95%的信度下认定次品率超过标称值（拒收）
p_actual_reject = 0.15  # 实际次品率大于标称值
p_threshold = 0.10  # 标称次品率
confidence_level_reject = 0.95  # 信度要求

sample_size_reject, reject_probability = monte_carlo_reject(
    p_actual_reject, p_threshold, confidence_level_reject
)

# 情况2：90%的信度下认定次品率不超过标称值（接收）
p_actual_accept = 0.07  # 实际次品率小于标称值
confidence_level_accept = 0.90  # 信度要求

sample_size_accept, accept_probability = monte_carlo_accept(
    p_actual_accept, p_threshold, confidence_level_accept
)

# 输出结果
# 将结果转换为 DataFrame
results_df = pd.DataFrame({
    'Condition': ['Reject at 95% Confidence', 'Accept at 90% Confidence'],
    'Sample Size': [sample_size_reject, sample_size_accept],
    'Probability': [reject_probability, accept_probability]
})
print(results_df)