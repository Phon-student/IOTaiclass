import matplotlib.pyplot as plt

def convert_to_pdf_matplotlib(input_file, output_pdf):
    with open(input_file, 'r') as python_file:
        content = python_file.read()
        fig, ax = plt.subplots()
        ax.text(0.1, 0.5, content, wrap=True, fontsize=12)
        ax.axis('off')

        plt.savefig(output_pdf, format='pdf')

if __name__ == "__main__":
    input_file = input("Enter the input Python file name: ")
    output_pdf = input("Enter the output PDF file name: ")
    convert_to_pdf_matplotlib(input_file, output_pdf)
    print("PDF is Saved Successfully")