import json
import os

def parse_openalex(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    parsed_records = []
    for record in data:
        # ONLY map raw -> structured schema. NO flattening.
        parsed = {
            'id': record.get('id', ''),
            'doi': record.get('doi', ''),
            'title': record.get('title', ''),
            'publication_year': record.get('publication_year'),
            'type': record.get('type', ''),
            'indexed_in': record.get('indexed_in', []),
            'primary_location': record.get('primary_location', {}),
            'open_access': record.get('open_access', {}),
            'authorships': record.get('authorships', []),
            
            # Provenance fields (FIX 5)
            'source_system': 'openalex',
            'metadata_format': 'json',
            'is_inferred': False
        }
        parsed_records.append(parsed)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        for rec in parsed_records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            
    print(f"Successfully parsed {len(parsed_records)} OpenAlex records to {output_file}.")

if __name__ == "__main__":
    parse_openalex(
        "data/raw/openalex_json/openalex_bby_works_full.json",
        "data/parsed/openalex/openalex_records.jsonl"
    )
