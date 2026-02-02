import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv("All_Diets.csv")
print("Dataset loaded successfully.")
print("Shape:", df.shape)
print(df.head())

numeric_cols = ["Protein(g)", "Carbs(g)", "Fat(g)"]
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
print("Missing values handled.")
print(df[numeric_cols].isnull().sum())

avg_macros = df.groupby("Diet_type")[["Protein(g)", "Carbs(g)", "Fat(g)"]].mean()
print("--- Average Macronutrients by Diet Type ---")
print(avg_macros)

top_protein = df.sort_values("Protein(g)", ascending=False).groupby("Diet_type").head(5)
print("--- Top 5 Protein-Rich Recipes per Diet Type ---")
print(top_protein[["Diet_type", "Recipe_name", "Protein(g)"]])

highest_protein_diet = avg_macros["Protein(g)"].idxmax()
print("--- Diet with Highest Protein:", highest_protein_diet, "---")

most_common_cuisine = df.groupby("Diet_type")["Cuisine_type"].agg(lambda x: x.value_counts().index[0])
print("--- Most Common Cuisine per Diet Type ---")
print(most_common_cuisine)

df["Protein_to_Carbs_ratio"] = df["Protein(g)"] / df["Carbs(g)"]
df["Carbs_to_Fat_ratio"] = df["Carbs(g)"] / df["Fat(g)"]
print("--- New Metrics (first 5 rows) ---")
print(df[["Recipe_name", "Protein_to_Carbs_ratio", "Carbs_to_Fat_ratio"]].head())

fig, ax = plt.subplots(figsize=(12, 6))
avg_macros.plot(kind="bar", ax=ax, color=["#2ecc71", "#3498db", "#e74c3c"], edgecolor="black")
ax.set_title("Average Macronutrient Content by Diet Type", fontsize=14, fontweight="bold")
ax.set_xlabel("Diet Type", fontsize=12)
ax.set_ylabel("Grams (g)", fontsize=12)
ax.legend(title="Macronutrient")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("chart_bar_macros.png", dpi=150)
print("Bar chart saved.")

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(avg_macros, annot=True, fmt=".1f", cmap="YlOrRd", linewidths=0.5, ax=ax)
ax.set_title("Heatmap: Macronutrient Content by Diet Type", fontsize=14, fontweight="bold")
ax.set_xlabel("Macronutrient", fontsize=12)
ax.set_ylabel("Diet Type", fontsize=12)
plt.tight_layout()
plt.savefig("chart_heatmap.png", dpi=150)
print("Heatmap saved.")

fig, ax = plt.subplots(figsize=(12, 7))
cuisines = top_protein["Cuisine_type"].unique()
colors = sns.color_palette("tab10", n_colors=len(cuisines))
for cuisine, color in zip(cuisines, colors):
    subset = top_protein[top_protein["Cuisine_type"] == cuisine]
    ax.scatter(subset["Diet_type"], subset["Protein(g)"], label=cuisine, color=color, s=80, edgecolors="black", zorder=3)
ax.set_title("Top 5 Protein-Rich Recipes by Diet Type (colored by Cuisine)", fontsize=14, fontweight="bold")
ax.set_xlabel("Diet Type", fontsize=12)
ax.set_ylabel("Protein (g)", fontsize=12)
ax.legend(title="Cuisine", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.xticks(rotation=45, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("chart_scatter_protein.png", dpi=150)
print("Scatter plot saved.")

print("=== ALL TASKS COMPLETE ===")