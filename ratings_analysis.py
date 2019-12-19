#%%
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

#%%
with open('ratings.csv', 'r', encoding='mac_roman', newline='') as csvfile:
    df = pd.read_csv(csvfile)

# %%
plt.scatter(df['IMDb Rating'], df['Your Rating'])
plt.title('IMDb Rating vs. My Rating')
plt.xlabel('IMDb Rating')
plt.ylabel('My Rating')
plt.show()

# %%
