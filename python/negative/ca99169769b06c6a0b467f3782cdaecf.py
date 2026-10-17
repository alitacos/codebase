def collect_html_pages_of_how_to_in_articles_wonderhowto_dot_com_sitemap_index_into_a_parquet_file_via_webdriver_and_print_for_debugging(driver:object=None, out_path= '/content/drive/MyDrive/datasets/html/wonderhowto_articles.parquet', xml_url:str='https://infosecwriteups.com/sitemap/sitemap.xml',BATCH_SIZE : int= 1,PRINT_INTERVAL :int = 100 )->int:
    """
	    Collects HTML pages from WonderHowTo sitemap index using a Selenium WebDriver,
    extracts article page content (URL, title, HTML, metadata), and writes results
    incrementally into a Parquet file while printing progress for debugging.

    Args:
        driver (object): Selenium WebDriver instance used to load and render web pages.
        out_path (Any): Output Parquet file path where scraped HTML data will be stored.
                        (Defaults to '/content/drive/MyDrive/datasets/html/wonderhowto_articles.parquet')
        xml_url (str): Sitemap index URL used to extract article links.
                       (Defaults to 'https://infosecwriteups.com/sitemap/sitemap.xml')
        BATCH_SIZE (int): Number of pages processed before writing to Parquet.
                         (Defaults to 1 for row-by-row streaming writes)
        PRINT_INTERVAL (int): Interval at which progress logs are printed during scraping.

    Returns:
        int: Total number of successfully processed article pages saved into the Parquet file.

    Example usage:
        >>> result = collect_html_pages_of_how_to_in_articles_wonderhowto_dot_com_sitemap_index_into_a_parquet_file_via_webdriver_and_print_for_debugging(driver='[MASKED]', out_path='/content/drive/MyDrive/datasets/html/wonderhowto_articles.parquet', xml_url='https://infosecwriteups.com/sitemap/sitemap.xml', BATCH_SIZE=1, PRINT_INTERVAL=100)
    	"""
    from selenium import webdriver
    import pandas as pd
    from bs4 import BeautifulSoup
    import os
    import pyarrow as pa
    import pyarrow.parquet as pq




    # Initialize an empty list to store the current batch of extracted data
    current_batch_data = []

    # Ensure the output directory exists
    output_dir = os.path.dirname(out_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

     
    writer = None # Initialize writer to None
    num_items_processed = 0

    def get_existing_urls_from_parquet(filepath:str=None, urls:list=[] ):
        """Reads existing URLs from a Parquet file for deduplication."""
        existing_urls_set = set()
        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            try:
                # Read only the 'url' column from the existing Parquet file
                existing_table = pq.read_table(filepath, columns=['url'])
                existing_urls_set = set(existing_table['url'].to_pylist())
                print(f"Found {len(existing_urls_set)} URLs in existing Parquet file. These will be skipped.")
            except Exception as e:
                print(f"Warning: Could not read existing URLs from {filepath} for deduplication: {e}. Proceeding without in-file deduplication for this run.")
        return sorted(set([u for u in [u for u in urls if u and '-' in u.strip('/').split('/')[-1]] if u not in existing_urls_set]))

    try:
        # --- Deduplication Logic ---


        # Iterate through all URLs, applying the initial filtering and then deduplicating

        filtered_urls = get_existing_urls_from_parquet(filepath=out_path, urls=urls )
        total_urls_to_process = len(filtered_urls)
        print(f"Starting to process {total_urls_to_process} new URLs after initial filtering and deduplication.")
        # --- End Deduplication Logic ---

        for i, url_item in enumerate(filtered_urls):
            try:
                driver.get(url_item)
                html_content = driver.page_source
                current_url = driver.current_url
                page_title = driver.title


                soup = BeautifulSoup(html_content, 'html.parser')
                title_tag = soup.find('title')
                if title_tag:
                    page_title = title_tag.text.strip()
                # If page_title from driver is sufficient, no else is needed, it defaults to driver.title

                item = { 'url': current_url, 'title': page_title, 'html': html_content, 'meteredContent': False }
                current_batch_data.append(item)
                num_items_processed += 1

                # If batch size is reached or it's the last item, write the batch
                # With BATCH_SIZE=1, this condition is met for every item, enabling row-by-row writing.
                if len(current_batch_data) >= BATCH_SIZE or (i == total_urls_to_process - 1 and current_batch_data):
                    batch_df = pd.DataFrame(current_batch_data)
                    batch_table = pa.Table.from_pandas(batch_df)

                    if writer is None:
                        # First write: check if file exists and schema matches, else create/overwrite
                        if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
                            try:
                                existing_schema = pq.read_schema(out_path)
                                if existing_schema.equals(batch_table.schema):
                                    writer = pq.ParquetWriter(out_path, existing_schema, compression='snappy')
                                    print(f"Appending to existing Parquet file: {out_path}")
                                else:
                                    # Schema mismatch, usually indicates a problem or new structure, so overwrite.
                                    print(f"Schema mismatch for {out_path}. Overwriting file to ensure consistency.")
                                    writer = pq.ParquetWriter(  out_path, batch_table.schema, compression='snappy')
                            except Exception as e:
                                print(f"Error handling existing Parquet file {out_path}: {e}. Creating new file to proceed.")
                                writer = pq.ParquetWriter(out_path, batch_table.schema, compression='snappy')
                        else:
                            writer = pq.ParquetWriter(out_path, batch_table.schema, compression='snappy')
                            print(f"Creating new Parquet file: {out_path}")

                        writer.write_table(batch_table) # Write the first batch (creating file or appending)

                    else: # Subsequent batches, use existing writer to append
                        writer.write_table(batch_table) # This appends new row groups

                    if num_items_processed % PRINT_INTERVAL == 0 or num_items_processed == total_urls_to_process:
                        remaining_to_process = total_urls_to_process - num_items_processed
                        print(f"Wrote batch of {len(current_batch_data)} items. Total processed: {num_items_processed}. Remaining to process: {remaining_to_process}")
                    current_batch_data = [] # Clear the batch for the next set of items

            except Exception as e:
                print(f"Error processing URL {url_item}: {e}. Skipping this URL.")
                # Continue to the next URL even if an error occurs

    finally:
        if writer:
            writer.close() # Close the writer to finalize the Parquet file
            print(f"Parquet writer closed. Final total items saved: {num_items_processed}")
        driver.quit() # Ensure the driver is quit after all processing
        print("Selenium driver closed.")
        return num_items_processed