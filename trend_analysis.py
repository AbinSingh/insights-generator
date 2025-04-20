import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import os

output_dir = r'C:\Stored Files\Abin\Machine Learning\Projects\Pycharm\insights-generator\data_output'


# 4. Function to fit a linear regression and get the slope
def calculate_slope(theme_data):
    theme_data = theme_data.copy()
    theme_data['Month_Num'] = np.arange(len(theme_data))

    X = theme_data['Month_Num'].values.reshape(-1, 1)
    y = theme_data['TotalPaidAmount'].values

    model = LinearRegression().fit(X, y)
    return model.coef_[0]

def generate_trend(df_claims):
    # 1. Filter: Only HF-HP from both quadrants
    df_claims_filtered = df_claims[
        (df_claims['CauseOfLossQuadrant'] == 'HF-HP') &
        (df_claims['HazardQuadrant'] == 'HF-HP')
        ].copy()

    # 2. Ensure LossDate is datetime
    df_claims_filtered['LossDate'] = pd.to_datetime(df_claims_filtered['LossDate'])

    # 3. Create Month column
    df_claims_filtered['Month'] = df_claims_filtered['LossDate'].dt.to_period('M')

    # 4. Group and aggregate
    monthly_data = (
        df_claims_filtered
        .groupby(['CauseOfLossQuadrant', 'HazardQuadrant', 'HazardSignalTheme', 'Month'])['TotalPaidAmount']
        .sum()
        .reset_index()
    )

    # 5. Calculate slopes for each unique combination
    slopes = []
    group_cols = ['CauseOfLossQuadrant', 'HazardQuadrant', 'HazardSignalTheme']

    for combo, group in monthly_data.groupby(group_cols):
        slope = calculate_slope(group)
        slopes.append((*combo, slope))

    # 6. Create slope_df with all three keys
    slope_df = pd.DataFrame(slopes, columns=group_cols + ['Slope'])

    # 7. Merge back on all three columns
    df_claims = df_claims.merge(slope_df, on=group_cols, how='left')

    # Visualization with trend line
    for combo, group in monthly_data.groupby(group_cols):
        group = group.copy()
        group['Month_Num'] = np.arange(len(group))

        X = group['Month_Num'].values.reshape(-1, 1)
        y = group['TotalPaidAmount'].values

        model = LinearRegression().fit(X, y)
        trend_line = model.predict(X)

        plt.figure(figsize=(10, 6))
        plt.plot(group['Month'].astype(str), y, marker='o', label='Total Paid Amount')
        plt.plot(group['Month'].astype(str), trend_line, color='red', linestyle='--', label='Trend Line')

        plt.title(f"Trend: {combo[0]} / {combo[1]} / {combo[2]}")
        plt.xlabel("Month")
        plt.ylabel("Total Paid Amount")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        filename = f"{combo[0]}_{combo[1]}_{combo[2]}".replace(" ", "_").replace("/", "-") + ".png"
        plt.savefig(os.path.join(output_dir, filename))
        plt.show()
        #plt.close()
    return df_claims