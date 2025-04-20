import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


# 4. Function to fit a linear regression and get the slope
def calculate_slope(theme_data):
    # Convert Month to numerical values (e.g., 0, 1, 2, ..., 47 for 48 months)
    theme_data['Month_Num'] = np.arange(len(theme_data))

    # Prepare X (month number) and Y (total paid amount)
    X = theme_data['Month_Num'].values.reshape(-1, 1)  # Reshaping for regression
    y = theme_data['TotalPaidAmount'].values

    # Fit linear regression model
    model = LinearRegression().fit(X, y)

    # Get the slope (coefficient) of the linear regression line
    slope = model.coef_[0]

    return slope


def generate_trend(df_claims):

    # Assuming df_claims is your DataFrame with columns: CauseOfLossQuadrant, HazardQuadrant, HazardSignalTheme, LossDate, TotalPaidAmount

    # 1. Filter: Only HF-HP from both CauseOfLossQuadrant and HazardQuadrant
    df_claims_filtered = df_claims[(df_claims['CauseOfLossQuadrant'] == 'HF-HP') & (df_claims['HazardQuadrant'] == 'HF-HP')]

    # 2. Ensure LossDate is in datetime format
    df_claims_filtered['LossDate'] = pd.to_datetime(df_claims_filtered['LossDate'])

    # 3. Aggregate by HazardSignalTheme and LossDate (monthly)
    df_claims_filtered['Month'] = df_claims_filtered['LossDate'].dt.to_period('M')

    monthly_data = df_claims_filtered.groupby(['HazardSignalTheme', 'Month'])['TotalPaidAmount'].sum().reset_index()


    # 5. Apply the linear regression function to each HazardSignalTheme
    slopes = []
    for theme in monthly_data['HazardSignalTheme'].unique():
        theme_data = monthly_data[monthly_data['HazardSignalTheme'] == theme]
        slope = calculate_slope(theme_data)
        slopes.append((theme, slope))

    # 6. Store slope values back into df_claims
    slope_df = pd.DataFrame(slopes, columns=['HazardSignalTheme', 'Slope'])
    df_claims = df_claims.merge(slope_df, on='HazardSignalTheme', how='left')

    # 7. Optional: Visualization
    for theme in monthly_data['HazardSignalTheme'].unique():
        theme_data = monthly_data[monthly_data['HazardSignalTheme'] == theme]
        plt.figure(figsize=(10, 6))
        plt.plot(theme_data['Month'].astype(str), theme_data['TotalPaidAmount'], label=f'{theme} - TotalPaidAmount')
        plt.title(f'Trend for {theme}')
        plt.xlabel('Month')
        plt.ylabel('Total Paid Amount')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    return df_claims
