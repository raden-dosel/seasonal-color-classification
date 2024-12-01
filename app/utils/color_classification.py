import pandas as pd
import numpy as np

def classify_seasonal_color(hue, saturation, value):
    """
    Classify colors into seasonal groups based on seasonal color theory.
    
    Args:
        hue (float): Hue value in degrees (0-360)
        saturation (float): Saturation percentage (0-100)
        value (float): Value/Brightness percentage (0-100)
    
    Returns:
        str: Seasonal color group
    """
    # Normalize inputs
    hue = float(hue)
    saturation = float(saturation)
    value = float(value)
    
    if saturation < 0.4:  # Low saturation
        if value > 0.7:
            return "Winter"  # Bright but low saturation
        else:
            return "Summer"  # Muted colors
    else:  # High saturation
        if hue < 60 or hue > 300:
            return "Autumn"  # Warm tones like reds, oranges
        elif 60 <= hue <= 180:
            return "Spring"  # Light and vibrant tones like greens and yellows
        else:
            return "Winter"  # Cool and high-contrast colors like blues


def classify_color_dataset(csv_path):
    """
    Process a CSV color dataset and add a seasonal color classification column.
    
    Args:
        csv_path (str): Path to the CSV file with color data
    
    Returns:
        pd.DataFrame: DataFrame with added seasonal color classification
    """
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # Apply seasonal classification
    df['Seasonal Group'] = df.apply(
        lambda row: classify_seasonal_color(
            row['Hue (degrees)'], 
            row['Saturation (percent)'], 
            row['Value (percent)']
        ), 
        axis=1
    )
    
    return df

def analyze_seasonal_color_distribution(classified_df):
    """
    Analyze and print distribution of seasonal color groups.
    
    Args:
        classified_df (pd.DataFrame): DataFrame with seasonal color classifications
    """
    # Calculate distribution of seasonal groups
    color_distribution = classified_df['Seasonal Group'].value_counts(normalize=True) * 100
    
    print("\nSeasonal Color Group Distribution:")
    for group, percentage in color_distribution.items():
        print(f"{group}: {percentage:.2f}%")
    
    return color_distribution


def main(csv_path):
    """
    Main function to process color dataset and analyze seasonal groups.
    
    Args:
        csv_path (str): Path to the CSV color dataset
    """
    # Classify colors
    classified_colors = classify_color_dataset(csv_path)
    
    # Analyze distribution
    color_distribution = analyze_seasonal_color_distribution(classified_colors)
    
    
    # Optional: Save classified dataset
    classified_colors.to_csv('seasonal_color_classified.csv', index=False)
    print("\nClassified dataset saved to 'seasonal_color_classified.csv'")

    return classified_colors

# Example usage
if __name__ == "__main__":
    main('color_names.csv')