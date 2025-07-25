import pandas as pd
import chilis
import wendys
import popeyes

def get_top_html(df, name):
    # Extract top 5
    top_df = df.sort_values(by="proteinRatio", ascending=False).head(5)
    return f"<h2>{name} Top 5 High Protein-to-Calorie Items</h2>" + top_df.to_html(index=False, border=1, classes='table')

def main():
    html_parts = ['''
    <html>
    <head>
        <title>Top Protein-to-Calorie Fast Food Items</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            h2 { color: #444; }
            table { width: 80%; margin-bottom: 40px; border-collapse: collapse; }
            th, td { padding: 8px 12px; border: 1px solid #ccc; text-align: center; }
            th { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <h1>Top Protein-to-Calorie Items from Fast Food Chains</h1>
    ''']

    try:
        html_parts.append(get_top_html(chilis.get_top_protein_items(), "Chili's"))
    except Exception as e:
        html_parts.append(f"<p>Error loading Chili's data: {e}</p>")

    try:
        html_parts.append(get_top_html(wendys.get_top_protein_items(), "Wendy's"))
    except Exception as e:
        html_parts.append(f"<p>Error loading Wendy's data: {e}</p>")

    try:
        html_parts.append(get_top_html(popeyes.get_top_protein_items(), "Popeyes"))
    except Exception as e:
        html_parts.append(f"<p>Error loading Popeyes data: {e}</p>")

    try:
        html_parts.append(get_top_html(get_top_protein_items(), "McDonald's"))
    except Exception as e:
        html_parts.append(f"<p>Error loading McDonald's data: {e}</p>")

    html_parts.append("</body></html>")

    # Write to file
    with open("top_fast_food_items.html", "w") as f:
        f.write("".join(html_parts))

    print("✅ HTML file generated: top_fast_food_items.html")

if __name__ == "__main__":
    main()
