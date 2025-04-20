import numpy as np
import pandas as pd
from scipy.stats import zscore
import seaborn as sns
import matplotlib.pyplot as plt
import os
output_dir = r'C:\Stored Files\Abin\Machine Learning\Projects\Pycharm\insights-generator\data_output'


def hazard_quadrant_creator(df_claims):

    # Optional: Filter to only HF-HP claims if not already done
    hf_hp_claims = df_claims[df_claims['CauseOfLossQuadrant'] == 'HF-HP'].copy()

    # Step 1: Group by HazardSignalTheme
    hazard_grouped = hf_hp_claims.groupby('HazardSignalTheme').agg(
        Frequency=('ClaimKey', 'count'),
        TotalPaidAmount=('TotalPaidAmount', 'sum')
    ).reset_index()

    # Step 2: Log transformation
    hazard_grouped['LogFrequency'] = np.log1p(hazard_grouped['Frequency'])
    hazard_grouped['LogTotalPaidAmount'] = np.log1p(hazard_grouped['TotalPaidAmount'])

    # Step 3: Z-score calculation on log-transformed values
    hazard_grouped['FreqZ'] = zscore(hazard_grouped['LogFrequency'])
    hazard_grouped['PaidZ'] = zscore(hazard_grouped['LogTotalPaidAmount'])

    # Step 4: Binning into High / Low
    hazard_grouped['FreqCategory'] = hazard_grouped['FreqZ'].apply(lambda x: 'High' if x > 0 else 'Low')
    hazard_grouped['PaidCategory'] = hazard_grouped['PaidZ'].apply(lambda x: 'High' if x > 0 else 'Low')

    # Step 5: Create Quadrant Label
    hazard_grouped['HazardQuadrant'] = hazard_grouped['FreqCategory'].str[0] + 'F-' + hazard_grouped['PaidCategory'].str[0] + 'P'

    # Step 6: Merge back into main data
    # hf_hp_claims = hf_hp_claims.merge(
    #     hazard_grouped[['HazardSignalTheme', 'HazardQuadrant']],
    #     on='HazardSignalTheme',
    #     how='left'
    # )

    df_claims = df_claims.merge(
        hazard_grouped[['HazardSignalTheme', 'HazardQuadrant']],
        on='HazardSignalTheme',
        how='left'
    )

    # ✅ Now hf_hp_claims has: CauseOfLossTheme, CauseOfLossQuadrant, HazardSignalTheme, HazardQuadrant

    # Step 7: Plot distribution (optional)
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))

    sns.histplot(hazard_grouped['Frequency'], bins=10, kde=True, ax=axs[0, 0])
    axs[0, 0].set_title('Hazard Frequency (Raw)')

    sns.histplot(hazard_grouped['TotalPaidAmount'], bins=10, kde=True, ax=axs[0, 1])
    axs[0, 1].set_title('Hazard Paid Amount (Raw)')

    sns.histplot(hazard_grouped['LogFrequency'], bins=10, kde=True, ax=axs[1, 0], color='orange')
    axs[1, 0].set_title('Hazard Frequency (Log)')

    sns.histplot(hazard_grouped['LogTotalPaidAmount'], bins=10, kde=True, ax=axs[1, 1], color='orange')
    axs[1, 1].set_title('Hazard Paid Amount (Log)')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'hazard_quadrant.png'))
    plt.show()

    # Step 8: Plot Quadrant Chart for Hazard Signal Themes
    plt.figure(figsize=(10, 7))
    palette = {'HF-HP': 'red', 'HF-LP': 'orange', 'LF-HP': 'blue', 'LF-LP': 'green'}

    sns.scatterplot(
        data=hazard_grouped,
        x='Frequency',
        y='TotalPaidAmount',
        hue='HazardQuadrant',
        palette=palette,
        s=100,
        edgecolor='black'
    )

    # Annotate with hazard themes
    for i, row in hazard_grouped.iterrows():
        plt.text(row['Frequency'] + 0.2, row['TotalPaidAmount'], row['HazardSignalTheme'], fontsize=9)

    plt.axvline(hazard_grouped['Frequency'].mean(), color='gray', linestyle='--')
    plt.axhline(hazard_grouped['TotalPaidAmount'].mean(), color='gray', linestyle='--')

    plt.title('Hazard Signal Theme - Quadrant Chart (Z-score on Log Values)')
    plt.xlabel('Frequency')
    plt.ylabel('Total Paid Amount')
    plt.legend(title='Hazard Quadrant')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'hazard_quadrant_scatter.png'))
    plt.show()

    return df_claims
