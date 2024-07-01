import pandas as pd
data = pd.DataFrame(columns=['a','b'])
new = pd.DataFrame([[1,2]],columns=['a','b'])
data = pd.concat([data,new])
print(data)