# 3*3 categorization
# def zscore_to_category(z):
#     if z < -1:
#         return 'Low'
#     elif z > 1:
#         return 'High'
#     else:
#         return 'Medium'
#
# grouped['FreqCategory'] = grouped['FreqZ'].apply(zscore_to_category)
# grouped['PaidCategory'] = grouped['PaidZ'].apply(zscore_to_category)
#
# # Combine into descriptive multi-bin category
# grouped['Category'] = grouped['FreqCategory'].str[0] + 'F-' + grouped['PaidCategory'].str[0] + 'P'


# 3*3 plot
#
#
# import matplotlib.pyplot as plt
# import seaborn as sns
#
# plt.figure(figsize=(10, 7))
#
# palette = {
#     'LF-LP': 'green', 'LF-MP': 'lightgreen', 'LF-HP': 'yellowgreen',
#     'MF-LP': 'gold', 'MF-MP': 'gray', 'MF-HP': 'orange',
#     'HF-LP': 'lightskyblue', 'HF-MP': 'dodgerblue', 'HF-HP': 'red'
# }
#
# sns.scatterplot(
#     data=grouped,
#     x='FreqZ', y='PaidZ',
#     hue='Category',
#     palette=palette,
#     s=100, edgecolor='black'
# )
#
# # Add vertical and horizontal lines for -1, 0, +1 z-score
# for val in [-1, 0, 1]:
#     plt.axvline(val, color='gray', linestyle='--')
#     plt.axhline(val, color='gray', linestyle='--')
#
# plt.title('3x3 Categorization Plot (Z-Score Grid)')
# plt.xlabel('Frequency (Z-Score)')
# plt.ylabel('Total Paid Amount (Z-Score)')
# plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
# plt.tight_layout()
# plt.show()
