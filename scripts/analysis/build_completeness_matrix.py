import json
import pandas as pd
import os

def flatten_openalex(record):
    processed = {
        'id': record.get('id', ''),
        'doi': record.get('doi', ''),
        'title': record.get('title', ''),
        'publication_year': record.get('publication_year'),
        'type': record.get('type', ''),
        'source_system': record.get('source_system'),
        'metadata_format': record.get('metadata_format'),
        'is_inferred': record.get('is_inferred')
    }

    indexed_in = record.get('indexed_in', [])
    processed['indexed_in'] = "; ".join([str(x) for x in indexed_in if x]) if isinstance(indexed_in, list) else str(indexed_in)

    primary_loc = record.get('primary_location') or {}
    processed['location_id'] = primary_loc.get('landing_page_url') or primary_loc.get('id', '')
    
    source = primary_loc.get('source') or {}
    processed['journal_name'] = source.get('display_name', '')
    issn = source.get('issn', [])
    processed['issn'] = "; ".join([str(x) for x in issn if x]) if isinstance(issn, list) else str(issn)
    processed['publisher'] = source.get('host_organization_name', '')

    oa_data = record.get('open_access') or {}
    processed['is_oa'] = oa_data.get('is_oa', False)
    processed['oa_status'] = oa_data.get('oa_status', '')

    authorships = record.get('authorships', [])
    processed['author_count'] = len(authorships)
    
    has_orcid = False
    has_ror = False
    for auth in authorships:
        author_info = auth.get('author') or {}
        if author_info.get('orcid'):
            has_orcid = True
            
        institutions = auth.get('institutions', [])
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
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found.")
        return

    print(f"Reading parsed data from {input_file}...")
    
    data = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))

    print(f"Processing {len(data)} records for analysis matrix...")
    matrix_data = [flatten_openalex(record) for record in data]
    
    df = pd.DataFrame(matrix_data)
    
    columns = [
        'id', 'doi', 'title', 'publication_year', 'type', 
        'indexed_in', 'location_id', 'journal_name', 'issn', 'publisher',
        'is_oa', 'oa_status', 
        'author_count', 'has_orcid', 'has_ror',
        'source_system', 'metadata_format', 'is_inferred'
    ]
    df = df[[c for c in columns if c in df.columns]]

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    print(f"Saving matrix to {output_file}...")
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"Success! Matrix generated with {df.shape[0]} rows and {df.shape[1]} columns.")

if __name__ == "__main__":
    INPUT_PATH = "data/parsed/openalex/openalex_records.jsonl"
    OUTPUT_PATH = "data/analysis/completeness_matrix/openalex_completeness_matrix.csv"
    create_completeness_matrix(INPUT_PATH, OUTPUT_PATH)
