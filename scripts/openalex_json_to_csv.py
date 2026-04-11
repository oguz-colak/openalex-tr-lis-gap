import json
import csv
import os

def flatten_openalex_data(input_file, output_file):
    """
    Reads OpenAlex JSON data and converts it to a flattened CSV format.
    """
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found.")
        return

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return

    # Define CSV fieldnames in order
    fieldnames = [
        'id', 'doi', 'title', 'publication_year', 'journal_name', 'issn',
        'type', 'language', 'authors_count', 'authors_names', 'affiliations',
        'oa_status', 'has_references'
    ]

    try:
        # Use utf-8-sig for Excel compatibility
        with open(output_file, 'w', encoding='utf-8-sig', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for work in data:
                # 1. basic fields
                row = {
                    'id': work.get('id'),
                    'doi': work.get('doi'),
                    'title': work.get('title'),
                    'publication_year': work.get('publication_year'),
                    'type': work.get('type'),
                    'language': work.get('language'),
                }

                # 2. journal_name and issn
                primary_location = work.get('primary_location') or {}
                source = primary_location.get('source') or {}
                row['journal_name'] = source.get('display_name')
                
                # issn handling: issn_l or joined issn list
                issn_l = source.get('issn_l')
                issns = source.get('issn')
                if issn_l:
                    row['issn'] = issn_l
                elif issns and isinstance(issns, list):
                    row['issn'] = ", ".join(issns)
                else:
                    row['issn'] = None

                # 3. authors and affiliations
                authorships = work.get('authorships', [])
                row['authors_count'] = len(authorships)
                
                author_names = []
                institution_names = set() # Use set to avoid duplicate affiliations across authors
                
                for auth in authorships:
                    # author name
                    author_info = auth.get('author') or {}
                    name = author_info.get('display_name')
                    if name:
                        author_names.append(name)
                    
                    # institutions
                    institutions = auth.get('institutions', [])
                    for inst in institutions:
                        inst_name = inst.get('display_name')
                        if inst_name:
                            institution_names.add(inst_name)
                
                row['authors_names'] = "; ".join(author_names)
                row['affiliations'] = "; ".join(sorted(list(institution_names)))

                # 4. oa_status
                open_access = work.get('open_access', {})
                row['oa_status'] = open_access.get('oa_status')

                # 5. has_references (boolean or count indicating if referenced_works has items)
                referenced_works = work.get('referenced_works', [])
                row['has_references'] = len(referenced_works) > 0

                writer.writerow(row)

        print(f"Successfully converted {len(data)} records to {output_file}")

    except Exception as e:
        print(f"Error writing CSV file: {e}")

if __name__ == "__main__":
    INPUT_PATH = "data/raw/openalex_bby_works_full.json"
    OUTPUT_PATH = "data/processed/openalex_bby_works_full.csv"
    flatten_openalex_data(INPUT_PATH, OUTPUT_PATH)
