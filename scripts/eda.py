import pandas as pd
from scipy.stats import zscore


def drop_missing_values(data, threshold=0.5):
    missing_percentage = data.isnull().mean()

    # If the overall missing percentage is less than the threshold, drop rows with missing values
    if missing_percentage.mean() < threshold:
        data = data.dropna()
    else:
        # Drop columns where the percentage of missing values exceeds the threshold
        data = data.loc[:, missing_percentage < threshold]
    
    return data


def drop_outliers_zscore(df, column_name, z_threshold=3):

    # Calculate Z-scores
    df['z_score'] = zscore(df[column_name])

    # Identify outliers
    outliers = df[df['z_score'].abs() > z_threshold]
    print("Outliers identified:\n", outliers)

    # Drop outliers
    df_cleaned = df[df['z_score'].abs() <= z_threshold].copy()

    # Drop the z_score column
    df_cleaned.drop(columns=['z_score'], inplace=True)

    return df_cleaned
