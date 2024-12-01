import pandas as pd

def identify_top_10_colors(df):
  """Identifies the top 10 dominant colors in each seasonal group.

  Args:
    df: A pandas DataFrame containing color information.

  Returns:
    A dictionary where each key is a seasonal group and the value is a list of the top 10 dominant color hex codes.
  """

  dominant_colors = {}
  for group_name, group_df in df.groupby('Seasonal Group'):
    color_counts = group_df['Hex (24 bit)'].value_counts()
    top_10_colors = color_counts.head(10).index.tolist()
    dominant_colors[group_name] = top_10_colors
  return dominant_colors

# Read the CSV file
df = pd.read_csv('seasonal_color_classified.csv')

# Identify top 10 colors
top_10_colors = identify_top_10_colors(df)

# Print the results
for group, colors in top_10_colors.items():
  print(f"Top 10 colors for {group}:")
  for color in colors:
    print(color)
