import pandas as pd


file_path = 'merged_reddit_data.csv'

data = pd.read_csv(file_path)


# print("First few rows of the dataset:")
# print(data.head())


# print("\nDataset Information:")
# print(data.info())

# print("\nSummary Statistics:")
# print(data.describe())

# Check for missing values
# print("Missing values per column:\n", data.isnull().sum())

# Handle missing values
# Drop rows with missing values in critical columns (e.g., ID, Text, Upvotes)
data_cleaned = data.dropna(subset=['ID', 'Text', 'Upvotes'])

# For non-critical columns, fill missing values with appropriate defaults
data_cleaned['Flair'] = data_cleaned['Flair'].fillna('Unknown')

# print("Missing values after cleaning:\n", data_cleaned.isnull().sum())


import matplotlib.pyplot as plt
import seaborn as sns

# Visualize outliers in 'Upvotes' column
# sns.boxplot(data_cleaned['Upvotes'])
# plt.title('Boxplot of Upvotes')
# plt.show()

# Handle outliers using the IQR method
Q1 = data_cleaned['Upvotes'].quantile(0.25)
Q3 = data_cleaned['Upvotes'].quantile(0.75)
IQR = Q3 - Q1

# Define acceptable range
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Remove outliers
data_no_outliers = data_cleaned[(data_cleaned['Upvotes'] >= lower_bound) & (data_cleaned['Upvotes'] <= upper_bound)]
# print(f"Dataset size after removing outliers: {data_no_outliers.shape}")


from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Normalize 'Upvotes' using MinMaxScaler
scaler = MinMaxScaler()
data_no_outliers['Upvotes_normalized'] = scaler.fit_transform(data_no_outliers[['Upvotes']])

# Standardize 'Upvotes' if needed
standard_scaler = StandardScaler()
data_no_outliers['Upvotes_standardized'] = standard_scaler.fit_transform(data_no_outliers[['Upvotes']])

# Check the result
print(data_no_outliers[['Upvotes', 'Upvotes_normalized', 'Upvotes_standardized']].head())


data_no_outliers.to_csv('cleaned_reddit_data.csv')