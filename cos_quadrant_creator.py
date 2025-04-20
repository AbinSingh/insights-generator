import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import zscore
import os

output_dir = r'C:\Stored Files\Abin\Machine Learning\Projects\Pycharm\insights-generator\data_output'

def cos_quadrant_creator(df_claims):

    # Step 1: Group by Cause of Loss Theme
    grouped = df_claims.groupby('CauseOfLossTheme').agg(
        Frequency=('ClaimKey', 'count'),
        TotalPaidAmount=('TotalPaidAmount', 'sum')
    ).reset_index()

    # Step 2: Apply log normalization for better scale visualization
    grouped['LogFrequency'] = np.log1p(grouped['Frequency'])
    grouped['LogTotalPaidAmount'] = np.log1p(grouped['TotalPaidAmount'])

    # ✅ Step 3: Calculate Z-scores on log-transformed values
    grouped['FreqZ'] = zscore(grouped['LogFrequency'])
    grouped['PaidZ'] = zscore(grouped['LogTotalPaidAmount'])

    # Step 4: Define 2-bin categories for Frequency and Paid Amount
    grouped['FreqCategory'] = grouped['FreqZ'].apply(lambda x: 'High' if x > 0 else 'Low')
    grouped['PaidCategory'] = grouped['PaidZ'].apply(lambda x: 'High' if x > 0 else 'Low')

    # Step 5: Combine to form quadrant labels
    grouped['Quadrant'] = grouped['FreqCategory'].str[0] + 'F-' + grouped['PaidCategory'].str[0] + 'P'

    # Step 6: Visualizations - distribution before and after log
    fig, axs = plt.subplots(3, 2, figsize=(14, 14))  # 3 rows now

    sns.histplot(grouped['Frequency'], bins=10, kde=True, ax=axs[0, 0])
    axs[0, 0].set_title('Distribution of Frequency (Raw)')

    sns.histplot(grouped['TotalPaidAmount'], bins=10, kde=True, ax=axs[0, 1])
    axs[0, 1].set_title('Distribution of Total Paid Amount (Raw)')

    sns.histplot(grouped['LogFrequency'], bins=10, kde=True, ax=axs[1, 0], color='orange')
    axs[1, 0].set_title('Distribution of Frequency (Log)')

    sns.histplot(grouped['LogTotalPaidAmount'], bins=10, kde=True, ax=axs[1, 1], color='orange')
    axs[1, 1].set_title('Distribution of Total Paid Amount (Log)')

    # Row 3: Z-score distribution
    sns.histplot(grouped['FreqZ'], bins=10, kde=True, ax=axs[2, 0], color='green')
    axs[2, 0].axvline(0, linestyle='--', color='black')
    axs[2, 0].set_title('Distribution of Frequency (Z-Score)')

    sns.histplot(grouped['PaidZ'], bins=10, kde=True, ax=axs[2, 1], color='green')
    axs[2, 1].axvline(0, linestyle='--', color='black')
    axs[2, 1].set_title('Distribution of Total Paid Amount (Z-Score)')

    # ➕ Add ±1σ lines to highlight high/low regions
    for ax in [axs[2, 0], axs[2, 1]]:
        ax.axvline(-1, linestyle='--', color='red', alpha=0.6, label='-1σ')
        ax.axvline(1, linestyle='--', color='blue', alpha=0.6, label='+1σ')
        ax.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'cos_quadrant_distributions.png'))
    plt.show()

    # Step 7: Quadrant Chart
    plt.figure(figsize=(10, 7))
    palette = {'HF-HP': 'red', 'HF-LP': 'orange', 'LF-HP': 'blue', 'LF-LP': 'green'}

    # Plotting each point with category color
    sns.scatterplot(
        data=grouped,
        x='Frequency',
        y='TotalPaidAmount',
        hue='Quadrant',
        palette=palette,
        s=100,
        edgecolor='black'
    )

    # Annotate points with CauseOfLossTheme
    for i, row in grouped.iterrows():
        plt.text(row['Frequency'] + 0.2, row['TotalPaidAmount'], row['CauseOfLossTheme'], fontsize=9)

    # Add gridlines to show mean-based threshold lines
    plt.axvline(grouped['Frequency'].mean(), color='gray', linestyle='--')
    plt.axhline(grouped['TotalPaidAmount'].mean(), color='gray', linestyle='--')

    plt.title('Cause of Loss Theme - Quadrant Chart (Z-Score on Log Values)')
    plt.xlabel('Frequency')
    plt.ylabel('Total Paid Amount')
    plt.legend(title='Category (Quadrant)')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'cos_quadrant_scatter.png'))
    plt.show()

    # Step 8: Rename 'Quadrant' in grouped for clarity
    grouped.rename(columns={'Quadrant': 'CauseOfLossQuadrant'}, inplace=True)

    # Step 9: Merge quadrant info back into the original claims data
    df_claims = df_claims.merge(
        grouped[['CauseOfLossTheme', 'CauseOfLossQuadrant']],
        on='CauseOfLossTheme',
        how='left'
    )

    return df_claims
