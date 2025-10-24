import fitz  # PyMuPDF
import pandas as pd
import os

# --- Configuration ---
NAME_FONT_SIZE = 12  # Reduced for smaller page
# Adjusted coordinates for your A5 landscape page (419.25 x 297.75)
# Format: (Left_X, Top_Y, Right_X, Bottom_Y)
NAME_RECT = fitz.Rect(50, 150, 370, 210)
NAME_FONT_NAME = "Helvetica-Bold"  # Bold looks better for certificates
NAME_COLOR = (0, 0, 0)  # Black

# Create the output directory if it doesn't exist
output_dir = "certificates_org"
os.makedirs(output_dir, exist_ok=True)

# Read the CSV file
try:
    df = pd.read_csv("lista.csv")
    names = df["NOME"]
    print(f"Found {len(names)} names to process")
except FileNotFoundError:
    print("Error: 'lista.csv' not found. Cannot proceed.")
    names = []

# Iterate over the names and create a certificate for each one
for name in names:
    try:
        doc = fitz.open("certificado.pdf")
        page = doc[0]
        
        print(f"Processing: {name}")
        
        # Insert the name
        rc = page.insert_textbox(
            NAME_RECT,
            name,
            fontsize=NAME_FONT_SIZE,
            fontname=NAME_FONT_NAME,
            align=fitz.TEXT_ALIGN_CENTER,
            color=NAME_COLOR
        )
        
        if rc < 0:
            print(f"  Warning: Text might not fit - try reducing font size")
        
        # Save the new PDF
        safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '_')).rstrip()
        output_filename = os.path.join(output_dir, f"certificate_{safe_name}.pdf")
        doc.save(output_filename)
        doc.close()
        
        print(f"  ✓ Created {output_filename}")
        
    except Exception as e:
        print(f"  Error processing {name}: {e}")

print("\nDone!")
