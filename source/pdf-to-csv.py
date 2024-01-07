import tabula
import pandas as pd

rblPdf = tabula.read_pdf("../../Documents/AccountStatement01-10-2023-to-04-01-2024.pdf", pages='2')

print(rblPdf)