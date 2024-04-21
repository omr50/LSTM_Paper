import pandas as pd

# Load the CSV file
df = pd.read_csv('output_files/results/next_activity_and_time_helpdesk.csv')

# Display the first few rows of the dataframe to understand its structure
print(df.head())

# Calculate the average Levenshtein similarity (assuming it's between 0 and 1 where 1 is identical)
levenshtein_accuracy = df['Levenshtein'].mean()

# Calculate the average Damerau-Levenshtein similarity (assuming similar scale)
damerau_levenshtein_accuracy = df['Damerau'].mean()

# Calculate the average Jaccard similarity
jaccard_accuracy = df['Jaccard'].mean()

# Calculate the average MAE for time predictions
mae_time_accuracy = df['MAE'].mean()

# Print the results
print("Average Levenshtein Accuracy:", levenshtein_accuracy)
print("Average Damerau-Levenshtein Accuracy:", damerau_levenshtein_accuracy)
print("Average Jaccard Accuracy:", jaccard_accuracy)
print("Average Mean Absolute Error (MAE) for Time in seconds:", mae_time_accuracy)
print("Average Mean Absolute Error (MAE) for Time in days:", mae_time_accuracy/60/60/24)
