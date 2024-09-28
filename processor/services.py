import pandas as pd


def reconcile_files(source_file, target_file):
    # Load CSV files into dataframes
    source_df = pd.read_csv(source_file)
    target_df = pd.read_csv(target_file)

    source_df = source_df.map(lambda x: x.strip().lower() if isinstance(x, str) else x)
    target_df = target_df.map(lambda x: x.strip().lower() if isinstance(x, str) else x)

    if 'Date' in source_df.columns and 'Date' in target_df.columns:
        source_df['Date'] = pd.to_datetime(source_df['Date'], errors='coerce').dt.date
        target_df['Date'] = pd.to_datetime(target_df['Date'], errors='coerce').dt.date

    source_df.set_index('ID', inplace=True)
    target_df.set_index('ID', inplace=True)

    missing_in_target = source_df[~source_df.index.isin(target_df.index)]
    missing_in_source = target_df[~target_df.index.isin(source_df.index)]

    discrepancies = {}
    common_ids = source_df.index.intersection(target_df.index)

    for column in source_df.columns:
        if column in target_df.columns:  # Ensure the column exists in both DataFrames
            source_series = source_df.loc[common_ids, column]
            target_series = target_df.loc[common_ids, column]
            discrepancy_mask = source_series != target_series
            if discrepancy_mask.any():
                discrepancies[column] = source_df.loc[common_ids[discrepancy_mask]].reset_index().to_dict(
                    orient='records')

    return {
        'missing_in_target': missing_in_target.reset_index().to_dict(orient='records'),
        'missing_in_source': missing_in_source.reset_index().to_dict(orient='records'),
        'discrepancies': discrepancies
    }
