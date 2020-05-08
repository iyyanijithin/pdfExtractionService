import camelot

file = 'C:/Work/git/pdfExtractionService/app/uploads/foo.pdf'
tables = camelot.read_pdf(file)
for table in tables:
    print(table.df)
