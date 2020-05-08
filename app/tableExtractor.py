import camelot

def extractTable(filePath):
    print('extracting data from table')
    print(filePath)
    tables = camelot.read_pdf(filePath)
    tableFound = False
    for table in tables:
        table.to_excel("C:/Work/git/pdfExtractionService/app/output/response.xls")
        table.to_json("C:/Work/git/pdfExtractionService/app/output/response.json")
        print(table.df)
        tableFound = True
    if not tableFound:
        print('No tables foudnd need to try differenct approach')