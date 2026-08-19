import os
import requests
import pandas as pd


def get_county_health_data():
    '''
    get county health data from Excel file 
    '''

    df = pd.read_excel('data/health_rankings_2025.xlsx', sheet_name='Health Groups', header=1)#

    # Remove whitespace on column names
    df.columns = df.columns.str.strip()

    # Rename z-score columns 
    df.rename(columns={
        'National Z-Score': 'Health_Z_Score', 
        'National Z-Score.1': 'Community_Z_Score'
    }, inplace=True)

    # Drop nan rows
    health_df = df.dropna(subset=['County', 'Health_Z_Score', 'Community_Z_Score']).copy()

    # Convert z-scores to numeric 
    health_df['Health_Z_Score'] = pd.to_numeric(health_df['Health_Z_Score'], errors='coerce')
    health_df['Community_Z_Score'] = pd.to_numeric(health_df['Community_Z_Score'], errors='coerce')

    # Multiply z-scores by -1 so positive scores are healthier
    health_df['Health_Z_Score'] = health_df['Health_Z_Score'] * -1
    health_df['Community_Z_Score'] = health_df['Community_Z_Score'] * -1

    # Convert to string, remove decimals if any, and pad with zeros to length 5
    health_df['FIPS'] = health_df['FIPS'].astype(int).astype(str).str.zfill(5)

    return health_df



def merge_migration_health_ranking_data():
    '''
    Merge county-to-county migration dataframe and county health rankings dataframe
    '''
    health_df = pd.read_csv('data/cleaned_health_rankings_2025.csv', index_col=0, dtype = {'FIPS': str})
    m_df = pd.read_csv('data/county_to_county_US_2020.csv', index_col=0, dtype={
        'GEOID1': str,
        'GEOID2':str,
        'state':str,
        'county':str})

    migration_agg = m_df.groupby('GEOID1').agg({
        'MOVEDIN': 'sum',
        'MOVEDOUT': 'sum', 
        'MOVEDNET': 'sum',      # Total people gained/lost
        'POP1YR': 'mean',       # Population (should be constant for GEOID1, mean works)
        'POP1YRAGO': 'mean',    # Different than just pop1yr - movednet because people are born and later die
        'STATE1_NAME': 'first', # Keep state name
        'FULL1_NAME': 'first'   # Keep county name
    }).reset_index()

    # Normalize to net migration per 1,000 residents 
    migration_agg['Net_Migration_Rate'] = (migration_agg['MOVEDNET'] / migration_agg['POP1YR']) * 1000
    migration_agg['In_Migration_Rate'] = (migration_agg['MOVEDIN'] / migration_agg['POP1YR']) * 1000
    migration_agg['Out_Migration_Rate'] = (migration_agg['MOVEDOUT'] / migration_agg['POP1YR']) * 1000

    # Ensure GEOID1 is a 5-digit string with leading zeros (Shay did this in her notebook too)
    migration_agg['FIPS'] = migration_agg['GEOID1'].astype(str).str.zfill(5)

    # Merge
    df_master = pd.merge(migration_agg, health_df, on='FIPS', how='inner')

    return df_master



def merge_migration_rankings_metrics_data():
    '''
    Merge all three dataframes: county migration, health rankings, and health metrics.
    '''

    migration_ranking_df = merge_migration_health_ranking_data()

    chd_metrics = pd.read_csv('data/cleaned_chd_metrics_2022.csv', index_col=0, dtype ={
        'statecode': str, 
        'countycode': str,
        'FIPS': str})

    df_master = pd.merge(migration_ranking_df, chd_metrics, on='FIPS', how='inner')

    # Now we have some duplicative columns to drop. 
    drop_cols = ['STATE1_NAME', 'FULL1_NAME', 'Number of Counties Included in Health Groups', 'FIPS', 'statecode','countycode','fipscode', 'state','county']
    df_master = df_master.drop(columns = drop_cols)

    # rename some columns 
    rename_col_key = {'Health Group.1' : 'Community Score Group', 'Health Group Range.1' : 'Community Score Range'}
    df_master = df_master.rename(columns=rename_col_key)

    return df_master



def create_county_summaries():
    '''
    Standardizes the groupby().agg() that summarizes migration data by county.
    '''

    m_df = pd.read_csv('data/county_to_county_US_2020.csv', index_col=0, dtype={
        'GEOID1': str,
        'GEOID2':str,
        'state':str,
        'county':str})

    migration_agg = m_df.groupby('GEOID1').agg({
        'MOVEDIN': 'sum',
        'MOVEDOUT': 'sum', 
        'MOVEDNET': 'sum',      # Total people gained/lost
        'POP1YR': 'mean',       # Population (should be constant for GEOID1, mean works)
        'POP1YRAGO': 'mean',    # Different than just pop1yr - movednet because people are born and later die
        'STATE1_NAME': 'first', # Keep state name
        'FULL1_NAME': 'first'   # Keep county name
    }).reset_index()

    # Normalize to net migration per 1,000 residents 
    migration_agg['Net_Migration_Rate'] = (migration_agg['MOVEDNET'] / migration_agg['POP1YR']) * 1000
    migration_agg['In_Migration_Rate'] = (migration_agg['MOVEDIN'] / migration_agg['POP1YR']) * 1000
    migration_agg['Out_Migration_Rate'] = (migration_agg['MOVEDOUT'] / migration_agg['POP1YR']) * 1000

    # Ensure GEOID1 is a 5-digit string with leading zeros (Shay did this in her notebook too)
    migration_agg['GEOID1'] = migration_agg['GEOID1'].astype(str).str.zfill(5)
    
    return migration_agg