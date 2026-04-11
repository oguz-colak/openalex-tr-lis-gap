import json
import pandas as pd
import os
import numpy as np

def normalize_list_field(value):
    """
    Converts a list of strings or a list of objects (with 'display_name') 
    into a semicolon-separated string.
    """
    if not isinstance(value, list) or not value:
        return ""
    
    items = []
    for item in value:
        if isinstance(item, str):
            items.append(item)
        elif isinstance(item, dict):
            # Extract display_name for concepts, topics, etc.
            display_name = item.get('display_name')
            if display_name:
                items.append(display_name)
            else:
                # Fallback to ID or string representation if display_name is missing
                items.append(item.get('id', str(item)))
    
    return "; ".join(items)

def process_openalex_record(record):
    """
    Processes a single OpenAlex record applying flattening rules.
    """
    processed = record.copy()
    
    # 1. List Normalization (Array to String)
    list_fields = ['indexed_in', 'topics', 'keywords', 'concepts']
    for field in list_fields:
        processed[field] = normalize_list_field(record.get(field))
    
    # 2. Open Access Flattening
    oa_data = record.get('open_access', {})
    if not isinstance(oa_data, dict):
        oa_data = {}
    processed['is_oa'] = oa_data.get('is_oa', False)
    processed['oa_status'] = oa_data.get('oa_status', "")
    
    # 3. Primary Location Flattening
    loc_data = record.get('primary_location', {})
    if not isinstance(loc_data, dict):
        loc_data = {}
    # Use landing_page_url, fallback to id
    processed['location_id'] = loc_data.get('landing_page_url') or loc_data.get('id', "")
    
    # 4. Authorships & FAIR Metrics
    authorships = record.get('authorships', [])
    if not isinstance(authorships, list):
        authorships = []
        
    processed['author_count'] = len(authorships)
    
    # Check for ORCID
    has_orcid = False
    for auth in authorships:
        if isinstance(auth, dict) and auth.get('author', {}).get('orcid'):
            has_orcid = True
            break
    processed['has_orcid'] = has_orcid
    
    # Check for ROR in institutions
    has_ror = False
    for auth in authorships:
        if isinstance(auth, dict):
            institutions = auth.get('institutions', [])
            if isinstance(institutions, list):
                for inst in institutions:
                    if isinstance(inst, dict) and inst.get('ror'):
                        has_ror = True
                        break
        if has_ror:
            break
    processed['has_ror'] = has_ror
    
    # 5. Cleanup: Drop original complex columns
    cols_to_drop = ['open_access', 'primary_location', 'authorships', 'institutions']
    for col in cols_to_drop:
        if col in processed:
            del processed[col]
            
    return processed

def flatten_openalex_data(input_file, output_file):
    """
    Main function to read JSON, transform it to a flat matrix, and save as CSV.
    """
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found.")
        return

    print(f"Loading data from {input_file}...")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return

    if not data:
        print("Error: JSON data is empty.")
        return

    print(f"Processing {len(data)} records...")
    flattened_data = [process_openalex_record(record) for record in data]
    
    df = pd.DataFrame(flattened_data)
    
    # Final cleanup: ensure no other objects/lists remain (strings only or simple types)
    for col in df.columns:
        if df[col].dtype == 'object':
            # Check if there are still lists or dicts in this column
            contains_complex = df[col].apply(lambda x: isinstance(x, (list, dict))).any()
            if contains_complex:
                print(f"Warning: Column '{col}' still contains complex structures. Stringifying...")
                df[col] = df[col].apply(lambda x: json.dumps(x, ensure_ascii=False) if isinstance(x, (list, dict)) else x)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    print(f"Saving to {output_file}...")
    try:
        # Use utf-8-sig for Excel compatibility
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"Successfully created CSV matrix with {df.shape[0]} rows and {df.shape[1]} columns.")
    except Exception as e:
        print(f"Error writing CSV file: {e}")

if __name__ == "__main__":
    INPUT_PATH = "data/raw/openalex_bby_works_full.json"
    OUTPUT_PATH = "data/processed/openalex_completeness_matrix.csv"
    flatten_openalex_data(INPUT_PATH, OUTPUT_PATH)
