#!/usr/bin/env python3
import os
import sys

def parse_fasta(filepath):
    """Parses a multi-FASTA file and returns a list of dictionaries with header metadata and sequence."""
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.", file=sys.stderr)
        sys.exit(1)
        
    records = []
    current_header = ""
    current_seq = []
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if current_seq:
                    records.append({"header": current_header, "seq": "".join(current_seq)})
                    current_seq = []
                current_header = line[1:]
            else:
                current_seq.append(line)
        if current_seq:
            records.append({"header": current_header, "seq": "".join(current_seq)})
            
    return records

def apply_mutation(seq, mutation_str):
    """Applies a mutation string (e.g., G160C or G160A) to a sequence using 1-based indexing."""
    orig_aa = mutation_str[0]
    mut_pos = int(mutation_str[1:-1])
    mut_aa = mutation_str[-1]
    
    index = mut_pos - 1
    if index < 0 or index >= len(seq):
        raise ValueError(f"Position {mut_pos} is out of bounds for sequence length {len(seq)}.")
        
    if seq[index] != orig_aa:
        print(f"  [Note] Expected '{orig_aa}' at position {mut_pos}, found '{seq[index]}' in sequence.", file=sys.stderr)
        
    seq_list = list(seq)
    seq_list[index] = mut_aa
    return "".join(seq_list)

def main():
    # Automatically get the folder where this script is saved
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Point directly to the files inside that same folder
    input_file = os.path.join(script_dir, "destabilizing_selected_proteins.fasta")
    output_file = os.path.join(script_dir, "mutated_proteins_output.fasta")
    
    records = parse_fasta(input_file)
    print(f"Loaded {len(records)} sequences from {input_file}.\n")
    
    output_records = []
    
    for rec in records:
        header = rec['header']
        seq = rec['seq']
        
        # Extract the mutation from the header (e.g., 'mutation=F382C' -> 'F382C')
        mutation_str = None
        for part in header.split():
            if part.startswith("mutation="):
                mutation_str = part.split("=")[1]
                
        if not mutation_str:
            print(f"Warning: Could not parse mutation from header: {header}", file=sys.stderr)
            continue
            
        # 1. Generate the specific mutation listed in your file
        try:
            mut_seq = apply_mutation(seq, mutation_str)
            base_id = header.split()[0]
            new_header = f">{base_id}_mutated_{mutation_str} mutation={mutation_str} length={len(mut_seq)}"
            output_records.append((new_header, mut_seq))
            print(f"Successfully generated: {base_id} with mutation {mutation_str}")
        except Exception as e:
            print(f"Error processing {header}: {e}", file=sys.stderr)

    # Write all mutated sequences to an output FASTA file for I-TASSER
    with open(output_file, 'w') as out_f:
        for head, s in output_records:
            out_f.write(f"{head}\n{s}\n")
            
    print(f"\nAll mutated sequences saved to '{output_file}' ready for I-TASSER submission!")

if __name__ == "__main__":
    main()