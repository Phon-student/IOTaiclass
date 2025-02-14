from fpdf import FPDF

def convert_to_pdf_fpdf(input_file, output_pdf):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    with open(input_file, 'r') as python_file:
        content = python_file.read()
        pdf.multi_cell(0, 10, content)

    pdf.output(output_pdf)

# Example usage:
convert_to_pdf_fpdf('GP5.py', 'lab4.pdf')
print("PDF is Saved Successfully")