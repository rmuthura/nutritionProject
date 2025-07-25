import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
import numpy as np


pd.set_option("display.max_rows", 100)

pd.set_option("display.max_columns", 50)

pd.set_option("display.max_colwidth", None)

pd.set_option("display.width", None)
data = pd.read_csv("MacroFactor.csv")
data = data.dropna(subset= ['Trend Weight (lbs)'])
data['Date'] = pd.to_datetime(data['Date'])

# Days I went to NY and Philly and ate horrible (good) food
replacements = {
    '2025-06-21': {'Calories (kcal)': 2000, 'Protein (g)': 100, 'Fat (g)': 85,  'Carbs (g)': 150},
    '2025-07-04': {'Calories (kcal)': 2000, 'Protein (g)': 75,  'Fat (g)': 105, 'Carbs (g)': 150},
    '2025-07-05': {'Calories (kcal)': 3000, 'Protein (g)': 55,  'Fat (g)': 160, 'Carbs (g)': 155},
    '2025-07-12': {'Calories (kcal)': 1800, 'Protein (g)': 62,  'Fat (g)': 84,  'Carbs (g)': 135},
}

# Apply replacements
for date_str, new_vals in replacements.items():
    date = pd.to_datetime(date_str)
    for col, val in new_vals.items():
        data.loc[data['Date'] == date, col] = val

#total weight loss
weightLoss = data['Weight (lbs)'].iloc[0] - data['Weight (lbs)'].iloc[-1]
print(f"True Weight Loss ≈ {weightLoss:.2f}")
caloriesLost = weightLoss * 3500
print(f"True Calories Loss ≈ {caloriesLost:.2f}")
valid_energy_data = data.dropna(subset=['Calories (kcal)', 'Expenditure'])
days = (data['Date'].iloc[-1] - data['Date'].iloc[0]).days
avg_deficit_from_scale = (weightLoss * 3500) / days
print(f"True Deficit Loss ≈ {avg_deficit_from_scale:.2f}")

data['Date'] = pd.to_datetime(data['Date'])
num_days = (data['Date'].max() - data['Date'].min()).days
avg_cals_in = data['Calories (kcal)'].mean(skipna=True)

weight_loss = data['Weight (lbs)'].iloc[0] - data['Weight (lbs)'].iloc[-1]
daily_weight_loss = weight_loss / num_days

true_tdee = avg_cals_in + (daily_weight_loss * 3500)

print(f"True TDEE ≈ {true_tdee:.2f} kcal/day")

allegedCaloriesLost = valid_energy_data['Expenditure'].sum() - valid_energy_data['Calories (kcal)'].sum()
print(f"What I should have lost if I locked in ≈ {allegedCaloriesLost /3500:.2f}")
data = data.drop(columns = ['Target Calories (kcal)','Target Protein (g)','Target Fat (g)','Target Carbs (g)'])
data = data.drop(columns = ['Weight (lbs)'])
#data = data.fillna(data.mean(numeric_only=True))
data = data.reset_index(drop=True)
data = data.iloc[4:]

#Exclude partial days
data = data[data['Date'] != '6/21/25']
data = data[data['Date'] != '7/4/25']
data = data[data['Date'] != '7/5/25']
data = data[data['Date'] != '7/12/25']

data = data.drop(columns = ['Date'])
#print(data.columns)

y = data['Trend Weight (lbs)']
X = data.drop(columns = ['Trend Weight (lbs)','Expenditure'])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

model = XGBRegressor()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)

rmse = np.sqrt(mse)
print("RMSE:", rmse)
print(y_pred)
importance = pd.Series(model.feature_importances_, index=X.columns)

#print(importance.sort_values(ascending=False))
from xgboost import plot_importance
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 6))
plot_importance(model, ax=ax)
plt.tight_layout()
plt.savefig("feature_importance.png", dpi=300)
plt.close()

import shap

explainer = shap.Explainer(model)
shap_values = explainer(X)

shap.summary_plot(shap_values, X, show=False)
plt.savefig("shap_summary_plot_train.png", dpi=300, bbox_inches='tight')
plt.close()


