# Apply SNP Mutations to FASTA (`apply-snp-mutations-fasta`)

A lightweight Python script for introducing specific amino acid substitutions (SNPs) into wild-type protein sequences from a multi-FASTA file. It reads target mutation strings directly from sequence headers (such as `mutation=F382C`) and generates mutant FASTA sequences ready for downstream 3D structure modeling tools like I-TASSER or AlphaFold.

## Features
- Parses multi-FASTA files containing one or more wild-type protein sequences.
- Extracts mutation notation (`<WildTypeAA><Position><MutantAA>`, e.g., `F382C`) from header metadata.
- Uses 1-based residue numbering to match standard biological sequence coordinates.
- Logs a note if the residue found at the target position differs from the expected wild-type amino acid, while still applying the requested substitution.
- Automatically resolves file paths relative to the script's folder (`os.path.dirname(os.path.abspath(__file__))`).

## What to Change to Reuse with Your Own Data

1. **Format your FASTA headers:** Make sure every header includes a space-separated `mutation=` tag in the format `<WildTypeAA><1-based Position><MutantAA>`:
   ```text
   >ProteinID_1 mutation=F382C length=507
   MKAKTPANPK...

   2. **Update the input and output file names:** Open `apply_snp_mutations.py` and edit lines 54–55 inside `main()` to point to your own FASTA file and desired output name:
   ```python
   input_file = os.path.join(script_dir, "destabilizing_selected_proteins.fasta")
   output_file = os.path.join(script_dir, "mutated_proteins_output.fasta")
   ```
   *(Replace `"destabilizing_selected_proteins.fasta"` and `"mutated_proteins_output.fasta"` with your own filenames.)*

3. **Keep files in the same folder and run:** Place your input FASTA file in the same directory as `apply_snp_mutations.py` and run:
   ```bash
   python apply_snp_mutations.py
   ```
