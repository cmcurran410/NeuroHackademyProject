# Function that creates two plots from a dataframe: stacked bar for group, sex and sample size, and an error bar plot for group, sex and age (age mean and range)
# Needed input variables in the dataframe: Groups  Sex  Sample size  Age mean  Age sd  Age min  Age max
# Usage example:
# file_path = '/path/input_data.xlsx'
# df = pd.read_excel(file_path)
# plot_charts(df)

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def plot_charts(df):
    # Display the DataFrame to verify it's loaded correctly
    #print(df.head())  # This prints the first five rows of the DataFrame

    # Create stacked bar plot for group, sex and sample size
    # Create a pivot table for plotting
    
    
    #df = df.pivot(index=df.index, columns=df.columns, values=df.value)

    # Plotting the stacked bar chart
    ax = df.plot(kind='bar', stacked=True, color=['#ff9999', '#66b3ff'])  # Colors for Female and Male

    # Adding text annotations inside the bars and on top
    for i, (name, row) in enumerate(df.iterrows()):
        cum_val = 0  # Keep track of cumulative total to stack the labels correctly
        for j, val in enumerate(row):
            val = int(val)
            ax.text(i, cum_val + val/2, int(val), color='black', ha='center', va='center')
            cum_val += val
        # Display the total sample size above the bar
        ax.text(i, cum_val, f'Total: {int(cum_val)}', color='black', ha='center', va='bottom')

    # Set labels and title
    plt.title('Sample size by Sex and Group')
    plt.xlabel('Groups')
    plt.ylabel('Sample Size')
    plt.xticks(rotation=0)  # Keeps the labels horizontal
    plt.legend(title='Sex')

    # Adjust the legend to be outside the plot
    plt.legend(title='Sex', loc='upper left', bbox_to_anchor=(1,1))

    # Show the plot
    plt.show()

    # Create an error bar plot for group, sex and age
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = {'Female': '#ff9999', 'Male': '#66b3ff'}  # Define colors for Female and Male

    # Dictionary to keep track of the labels to ensure they are added only once to the legend
    labels_added = {}

    # Define a small offset to separate Female and Male within each group
    offset = 0.1  # Adjust this value to increase or decrease the separation
    group_positions = {group: i for i, group in enumerate(df['Groups'].unique())}

    # Iterate over the DataFrame to plot each point
    for i, row in df.iterrows():
        group_position = group_positions[row['Groups']]
        # Adjust position based on Sex
        if row['Sex'] == 'Male':
            position = group_position + offset
        else:
            position = group_position - offset

        # Correcting the errorbar call by properly closing the parentheses
        if row['Sex'] not in labels_added:
            ax.errorbar(position, row['Age mean'],
                        yerr=[[row['Age mean'] - row['Age min']], [row['Age max'] - row['Age mean']]],
                        fmt='o', color=colors[row['Sex']], label=row['Sex'], capsize=5, elinewidth=2, markeredgewidth=2)
            labels_added[row['Sex']] = True  # Mark this label as added
        else:
            ax.errorbar(position, row['Age mean'],
                        yerr=[[row['Age mean'] - row['Age min']], [row['Age max'] - row['Age mean']]],
                        fmt='o', color=colors[row['Sex']], capsize=5, elinewidth=2, markeredgewidth=2)

    # Customizations
    ax.set_xticks(list(group_positions.values()))
    ax.set_xticklabels(df['Groups'].unique())
    ax.set_xlabel('Groups')
    ax.set_ylabel('Age')
    ax.set_title('Age Mean and Range by Group and Sex')

    # Adjust x-axis limits to center the error bars
    ax.set_xlim(-0.5, len(group_positions) - 0.5)

    # Place legend outside the plot
    ax.legend(title='Sex', loc='upper left', bbox_to_anchor=(1, 1))

    plt.show()