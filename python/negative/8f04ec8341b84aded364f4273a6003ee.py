impoimport pandas as pd  # for DataFrame operations

def merge_records_or_existing_dataframe_and_write_to_parquet_file_with_deduplication_via_pandas(records: list = None, df: pd.DataFrame = None, parquetPath: str = None) -> dict:
    """
    Merges new records or an existing DataFrame with old records, performs deduplication, 
    writes the final DataFrame to a Parquet file if specified, and returns process information.
    
    Args:
        records (list): List of new records (dictionaries or similar) to merge.  # new data records
        df (pd.DataFrame): Existing DataFrame to merge with new records; can be None.  # existing data
        parquetPath (str): Path to the Parquet file to write the merged DataFrame to; can be None.  # target parquet file path
    
    Returns:
        dict: Dictionary containing process information:
            - 'path': The Parquet file path  # file path
            - 'count_records_df': Number of new records added  # count of new records
            - 'count_old_df': Number of records in the old DataFrame  # count of old records
            - 'count_total_rows': Total number of rows in the final DataFrame after merging and deduplication  # total row count
            - 'df': The final processed DataFrame  # merged DataFrame
            - 'error': Error type if an exception occurred, otherwise None  # error info
    
    Example usage:
        >>> result = merge_records_or_existing_dataframe_and_write_to_parquet_file_with_deduplication_via_pandas(records=[{'file_path': 'example.py', 'function': 'foo'}], df=existing_df, parquetPath='python_files_summary.parquet')
    """
    result = {'path': parquetPath,'count_records_df': None,'count_old_df': None,'count_total_rows': 0,'df': pd.DataFrame(),'error': None}  # Initialize result dictionary
    final_df = pd.DataFrame()  # Initialize with an empty DataFrame

    try:
        if records:  # If new records are provided
            new_df = pd.DataFrame(records)  # Convert records list to DataFrame
            result['count_records_df'] = len(new_df)  # Store count of new records
            if df is not None and not df.empty:  # Merge with existing DataFrame if provided
                result['count_old_df'] = len(df)  # Store count of old records
                all_columns = list(set(df.columns) | set(new_df.columns))  # Union of all columns
                existing_df_reindexed = df.reindex(columns=all_columns)  # Reindex old df to include all columns
                new_df_reindexed = new_df.reindex(columns=all_columns)  # Reindex new df to include all columns
                final_df = pd.concat([existing_df_reindexed, new_df_reindexed], ignore_index=True)  # Merge DataFrames
            else:  # No existing df, just use new records
                final_df = new_df
        elif df is not None and not df.empty:  # No new records, but existing df exists
            final_df = df  # Use existing DataFrame
            result['count_old_df'] = len(df)  # Store count of old records
        else:  # Nothing to merge
            return result  # Exit early with initial result dictionary

        if not final_df.empty:  # If merged DataFrame is not empty
            if 'file_path' in final_df.columns:  # Deduplicate based on 'file_path'
                final_df.drop_duplicates(subset=['file_path'], keep='last', inplace=True)  # Keep last occurrence
            else:  # Deduplicate based on all columns
                initial_len = len(final_df)  # Store initial row count
                final_df.drop_duplicates(inplace=True)  # Remove duplicates
            result['count_total_rows'] = len(final_df)  # Store total row count after deduplication
            result['df'] = final_df  # Assign final DataFrame to result
            if parquetPath and not final_df.empty:  # Write to Parquet if path specified
                final_df.to_parquet(parquetPath, index=False)  # Save to file
        else:  # Final DataFrame is empty
            result['count_total_rows'] = 0  # No rows
            result['df'] = pd.DataFrame()  # Ensure empty DataFrame in result
    except Exception as e:  # Catch any exceptions
        result['error'] = e.__class__.__name__  # Store exception type
    return result  # Return result dictionary