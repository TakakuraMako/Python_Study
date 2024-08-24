import numpy as np
import pandas as pd

# Load the data again since the context is lost
sales_data_path = './问题一/品种日销量.xlsx'
prophet_latest_data_path = './问题二/Prophet模型的预测结果.xlsx'

# Read the contents of the Excel files
sales_data = pd.read_excel(sales_data_path, None)  # Load all sheets
prophet_latest_data = pd.read_excel(prophet_latest_data_path, None)  # Load all sheets

# Extract the necessary sheets
wholesale_prices = prophet_latest_data["Sheet2"]
sales_data_filtered = sales_data["Sheet1"]

# Initialize an empty dictionary to store results for each category
aligned_sales_data = {}

# List of categories based on Prophet's price predictions
categories = wholesale_prices.columns[1:]  # Exclude the "时间" column

# Filter and align the sales data for each category
for category in categories:
    category_sales = sales_data_filtered[sales_data_filtered['分类名称'] == category]['销量(千克)'].values[:5]  # Take first 5 days as representative
    aligned_sales_data[category] = category_sales

# Extend the data to predict for one more day (July 6, 2023)
# Define a function to extend the sales data for one more day based on the last known trend
def extend_sales_data(sales_data):
    trend = sales_data[-1] - sales_data[-2]  # Simplistic approach: use the difference between last two days
    extended_sales = np.append(sales_data, sales_data[-1] + trend)
    return extended_sales

# Extend the sales data for each category
extended_sales_data = {category: extend_sales_data(aligned_sales_data[category]) for category in categories}

# Define the simulated annealing function
def simulate_annealing_for_category(category_name, sales_data, price_data):
    # Define the combined cost function for this category
    def cost_function(replenishment, pricing, sales_data, price_elasticity):
        replenishment_cost = np.sum((replenishment - sales_data) ** 2)
        pricing_cost = -np.sum((pricing - price_elasticity * sales_data) * sales_data)
        total_cost = replenishment_cost + pricing_cost
        return total_cost

    # Assume a simple price elasticity for now
    price_elasticity = 1.5
    
    # Simulated annealing parameters
    T_max = 1000
    T_min = 1
    cooling_rate = 0.95
    max_iterations = 100
    
    # Initialize the predictions (random initial guesses)
    initial_replenishment = np.random.uniform(low=0.8 * sales_data, high=1.2 * sales_data)
    initial_pricing = np.random.uniform(low=0.8 * price_data, high=1.2 * price_data)
    
    current_replenishment = initial_replenishment
    current_pricing = initial_pricing
    current_cost = cost_function(current_replenishment, current_pricing, sales_data, price_elasticity)
    best_replenishment = np.copy(current_replenishment)
    best_pricing = np.copy(current_pricing)
    best_cost = current_cost
    
    T = T_max
    
    while T > T_min and max_iterations > 0:
        new_replenishment = current_replenishment + np.random.uniform(-1, 1, size=current_replenishment.shape)
        new_pricing = current_pricing + np.random.uniform(-1, 1, size=current_pricing.shape)
        
        new_cost = cost_function(new_replenishment, new_pricing, sales_data, price_elasticity)
        
        if new_cost < current_cost or np.random.rand() < np.exp((current_cost - new_cost) / T):
            current_replenishment = new_replenishment
            current_pricing = new_pricing
            current_cost = new_cost
            
            if current_cost < best_cost:
                best_replenishment = np.copy(current_replenishment)
                best_pricing = np.copy(current_pricing)
                best_cost = current_cost
        
        T *= cooling_rate
        max_iterations -= 1
    
    return best_replenishment, best_pricing, best_cost

# Re-run the simulated annealing process with the extended sales and price data
simulated_annealing_results_extended = {}

for category in categories:
    # Extend the price data similarly for one more day
    category_prices = np.append(wholesale_prices[category].values[:len(extended_sales_data[category]) - 1], wholesale_prices[category].values[-1])
    
    # Perform simulated annealing for this category
    replenishment, pricing, cost = simulate_annealing_for_category(category, extended_sales_data[category], category_prices)
    
    # Store the results
    simulated_annealing_results_extended[category] = {
        'replenishment': replenishment,
        'pricing': pricing,
        'cost': cost
    }

result = pd.DataFrame(simulated_annealing_results_extended)
result.to_excel('补货和定价策略.xlsx')