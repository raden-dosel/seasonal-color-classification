import colorsys
import json
import csv

def rgb_to_hsv(r, g, b):
    """Converts RGB values to HSV values."""
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return h, s, v

# Read RGB values from CSV
rgb_colors = []
with open('color_names.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        r, g, b = int(row['Red (8 bit)']), int(row['Green (8 bit)']), int(row['Blue (8 bit)'])
        rgb_colors.append((r, g, b))

# Convert RGB to HSV
hsv_colors = []
for r, g, b in rgb_colors:
    h, s, v = rgb_to_hsv(r, g, b)
    hsv_colors.append((h, s, v))

# Save to JSON
with open('hsv_colors.json', 'w') as f:
    json.dump(hsv_colors, f)

# Save to CSV
with open('hsv_colors.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Hue', 'Saturation', 'Value'])
    writer.writerows(hsv_colors)