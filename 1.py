import numpy as np
import pandas as pd
import torch

input = torch.tensor([[1, -0.5], [-1, 3]])
a = torch.reshape(input, (1, 1, 2, 2))
b = torch.reshape(input, (-1, 1, 2, 2))
print(a)
print(b)