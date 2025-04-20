
import seaborn as sns
from scipy.stats import zscore
import matplotlib.pyplot as plt
import numpy as np
from data_generator import data_gen

def cos_quadrant_creatorV2(df_claims):
    # Step 1: Group by Cause of Loss Theme
    grouped = df_claims.groupby('CauseOfLossTheme').agg(
        Frequency=('ClaimKey', 'count'),
        TotalPaidAmount=('TotalPaidAmount', 'sum')
    ).reset_index()

    # Step 2: Apply log normalization
    grouped['LogFrequency'] = np.log1p(grouped['Frequency'])
    grouped['LogTotalPaidAmount'] = np.log1p(grouped['TotalPaidAmount'])

    # Step 3: Calculate Z-scores on log-transformed values
    grouped['FreqZ'] = zscore(grouped['LogFrequency'])
    grouped['PaidZ'] = zscore(grouped['LogTotalPaidAmount'])

    # Step 4: Categorization using ±1σ
    def zscore_to_category(z):
        if z < -1:
            return 'Low'
        elif z > 1:
            return 'High'
        else:
            return 'Medium'

    grouped['FreqCategory'] = grouped['FreqZ'].apply(zscore_to_category)
    grouped['PaidCategory'] = grouped['PaidZ'].apply(zscore_to_category)
    grouped['Category'] = grouped['FreqCategory'].str[0] + 'F-' + grouped['PaidCategory'].str[0] + 'P'

    # Step 5: Add category to original df_claims
    df_claims = df_claims.merge(grouped[['CauseOfLossTheme', 'Category']], on='CauseOfLossTheme', how='left')

    # Step 6: Visualization - Distribution Plots with Z-score overlays
    fig, axs = plt.subplots(3, 2, figsize=(14, 12))

    # Raw distributions
    sns.histplot(grouped['Frequency'], bins=10, kde=True, ax=axs[0, 0])
    axs[0, 0].set_title('Distribution of Frequency (Raw)')

    sns.histplot(grouped['TotalPaidAmount'], bins=10, kde=True, ax=axs[0, 1])
    axs[0, 1].set_title('Distribution of Total Paid Amount (Raw)')

    # Log distributions
    sns.histplot(grouped['LogFrequency'], bins=10, kde=True, ax=axs[1, 0], color='orange')
    axs[1, 0].set_title('Distribution of Frequency (Log)')

    sns.histplot(grouped['LogTotalPaidAmount'], bins=10, kde=True, ax=axs[1, 1], color='orange')
    axs[1, 1].set_title('Distribution of Total Paid Amount (Log)')

    # Z-score distributions
    sns.histplot(grouped['FreqZ'], bins=10, kde=True, ax=axs[2, 0], color='purple')
    axs[2, 0].set_title('Z-Score of Frequency')

    sns.histplot(grouped['PaidZ'], bins=10, kde=True, ax=axs[2, 1], color='purple')
    axs[2, 1].set_title('Z-Score of Total Paid Amount')

    # Add ±1σ lines and labels
    for ax in [axs[2, 0], axs[2, 1]]:
        ax.axvline(-1, linestyle='--', color='red', alpha=0.6, label='-1σ')
        ax.axvline(1, linestyle='--', color='blue', alpha=0.6, label='+1σ')
        ax.legend()
        ax.text(-2.5, ax.get_ylim()[1] * 0.9, 'Low', color='red', fontsize=10, fontweight='bold')
        ax.text(1.5, ax.get_ylim()[1] * 0.9, 'High', color='blue', fontsize=10, fontweight='bold')

    plt.tight_layout()
    plt.show()

    # Step 7: 3x3 Grid Plot (Z-score based)
    plt.figure(figsize=(10, 7))
    palette = {
        'LF-LP': 'green', 'LF-MP': 'lightgreen', 'LF-HP': 'yellowgreen',
        'MF-LP': 'gold', 'MF-MP': 'gray', 'MF-HP': 'orange',
        'HF-LP': 'lightskyblue', 'HF-MP': 'dodgerblue', 'HF-HP': 'red'
    }

    sns.scatterplot(
        data=grouped,
        x='FreqZ', y='PaidZ',
        hue='Category', palette=palette,
        s=100, edgecolor='black'
    )

    # Gridlines for ±1σ and mean
    for val in [-1, 0, 1]:
        plt.axvline(val, color='gray', linestyle='--')
        plt.axhline(val, color='gray', linestyle='--')

    # Annotate each point
    for _, row in grouped.iterrows():
        plt.text(row['FreqZ'] + 0.05, row['PaidZ'], row['CauseOfLossTheme'], fontsize=9)

    plt.title('Cause of Loss Theme - 3x3 Z-Score Grid')
    plt.xlabel('Frequency (Z-Score)')
    plt.ylabel('Total Paid Amount (Z-Score)')
    plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

    return df_claims