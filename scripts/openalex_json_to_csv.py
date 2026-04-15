import json
import pandas as pd
import os

def process_openalex_record(record):
    """
    Extracts the specified 15 columns from an OpenAlex record.
    Ensures a flat structure with no nested objects/lists.
    """
    # 1. Base fields
    processed = {
        'id': record.get('id', ''),
        'doi': record.get('doi', ''),
        'title': record.get('title', ''),
        'publication_year': record.get('publication_year'),
        'type': record.get('type', '')
    }

    # 2. indexed_in (stringified list)
    indexed_in = record.get('indexed_in', [])
    if isinstance(indexed_in, list):
        processed['indexed_in'] = "; ".join([str(x) for x in indexed_in if x])
    else:
        processed['indexed_in'] = str(indexed_in) if indexed_in else ""

    # 3. location_id (from primary_location)
    primary_loc = record.get('primary_location') or {}
    if isinstance(primary_loc, dict):
        processed['location_id'] = primary_loc.get('landing_page_url') or primary_loc.get('id', '')
        
        # New columns from primary_location -> source
        source = primary_loc.get('source', {})
        if isinstance(source, dict):
            processed['journal_name'] = source.get('display_name', '')
            
            issn = source.get('issn', [])
            if isinstance(issn, list):
                processed['issn'] = "; ".join([str(x) for x in issn if x])
            else:
                processed['issn'] = str(issn) if issn else ""

            processed['publisher'] = source.get('host_organization_name', '')
        else:
            processed.update({
                'journal_name': '',
                'issn': '',
                'publisher': ''
            })
    else:
        processed.update({
            'location_id': '',
            'journal_name': '',
            'issn': '',
            'publisher': ''
        })

    # 4. is_oa & oa_status (from open_access)
    oa_data = record.get('open_access') or {}
    if isinstance(oa_data, dict):
        processed['is_oa'] = oa_data.get('is_oa', False)
        processed['oa_status'] = oa_data.get('oa_status', '')
    else:
        processed['is_oa'] = False
        processed['oa_status'] = ''

    # 5. authorships based metrics
    authorships = record.get('authorships', [])
    if not isinstance(authorships, list):
        authorships = []
    
    processed['author_count'] = len(authorships)
    
    has_orcid = False
    has_ror = False
    
    for auth in authorships:
        if not isinstance(auth, dict):
            continue
            
        # Check ORCID
        author_info = auth.get('author') or {}
        if isinstance(author_info, dict) and author_info.get('orcid'):
            has_orcid = True
            
        # Check ROR
        institutions = auth.get('institutions', [])
        if isinstance(institutions, list):
            for inst in institutions:
                if isinstance(inst, dict) and inst.get('ror'):
                    has_ror = True
                    break
        
        if has_orcid and has_ror:
            break
            
    processed['has_orcid'] = has_orcid
    processed['has_ror'] = has_ror

    return processed

def create_completeness_matrix(input_file, output_file):
    """
    Main function to read OpenAlex JSON and save a clean 15-column CSV matrix.
    """
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found.")
        return

    print(f"Reading raw data from {input_file}...")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return

    print(f"Processing {len(data)} records (Whitelist Strategy - 15 Columns)...")
    matrix_data = [process_openalex_record(record) for record in data]
    
    df = pd.DataFrame(matrix_data)
    
    # Selection of specified 15 columns only (ensuring order)
    columns = [
        'id', 'doi', 'title', 'publication_year', 'type', 
        'indexed_in', 'location_id', 'journal_name', 'issn', 'publisher',
        'is_oa', 'oa_status', 
        'author_count', 'has_orcid', 'has_ror'
    ]
    df = df[columns]

    # Ensure target directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    print(f"Saving matrix to {output_file}...")
    try:
        # Use utf-8-sig for proper Turkish character support in Excel
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"Success! Matrix generated with {df.shape[0]} rows and {df.shape[1]} columns.")
    except Exception as e:
        print(f"Error saving CSV: {e}")

if __name__ == "__main__":
    INPUT_PATH = "data/raw/openalex_bby_works_full.json"
    OUTPUT_PATH = "data/processed/openalex_completeness_matrix.csv"
    create_completeness_matrix(INPUT_PATH, OUTPUT_PATH)
