import tabula
import PyPDF2
import re
import csv

def clean_up_rbl_data(account_data):
    # Extracting relevant account information using regular expressions
    opening_balance_match = re.search(r'Opening\s+Balance₹\s+([\d,]+\.\d+)', account_data)
    closing_balance_match = re.search(r'Closing\s+Balance₹\s+([\d,]+\.\d+)', account_data)
    eff_avail_bal_match = re.search(r'Eff\s+Avail\s+Bal₹\s+([\d,]+\.\d+)', account_data)
    count_of_debit_match = re.search(r'Count\s+Of\s+Debit(\d+)', account_data)
    count_of_credit_match = re.search(r'Count\s+Of\s+Credit(\d+)', account_data)
    lien_amt_match = re.search(r'Lien\s+Amt₹\s+([\d,]+\.\d+)', account_data)

    # Creating a dictionary with the extracted information
    cleaned_data = {
        'Bank Account': "RBL Bank",
        'Opening Balance': '₹ ' + opening_balance_match.group(1) if opening_balance_match else None,
        'Closing Balance': '₹ ' + closing_balance_match.group(1) if closing_balance_match else None,
        'Eff Avail Bal': '₹ ' + eff_avail_bal_match.group(1) if eff_avail_bal_match else None,
        'Count Of Debit': int(count_of_debit_match.group(1)) if count_of_debit_match else None,
        'Count Of Credit': int(count_of_credit_match.group(1)) if count_of_credit_match else None,
        'Lien Amt': '₹ ' + lien_amt_match.group(1) if lien_amt_match else None,
    }

    return cleaned_data

def extract_table_from_pdf(pdf_path, page_number=1):
    # Specify the area containing the table using the 'area' parameter
    table_area = [514.08, 33.84, 685.44, 560.88]  # Adjust these values based on your PDF layout

    # Read the PDF and extract the table
    table_df = tabula.read_pdf(pdf_path, pages=page_number, multiple_tables=True, area=table_area)

    return table_df

def extract_rbl_data_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)

        # Assuming you want to extract text data from the first page
        account_details_page = pdf_reader.pages[4]
        account_details_data = account_details_page.extractText()

        # Table out of RBL PDF
        records_data = extract_table_from_pdf(pdf_path)

        # Save the table data to a CSV file
        if records_data:
            print(records_data[0])
            records_data[0].to_csv("../rbl_table_data.csv", index=False)

        clean_data = clean_up_rbl_data(account_details_data)

        return clean_data

pdf_path = "../../Documents/AccountStatement01-10-2023-to-04-01-2024.pdf"
data_from_pdf = extract_rbl_data_from_pdf(pdf_path)

def write_to_csv(data, csv_filename):
    # Extracting the keys from the dictionary to use as column headers
    headers = list(data.keys())

    # Extracting the values from the dictionary
    values = list(data.values())

    # Writing to the CSV file
    with open(csv_filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Writing the headers
        csv_writer.writerow(headers)

        # Writing the values
        csv_writer.writerow(values)

write_to_csv(data_from_pdf, "../rbl_data.csv")
