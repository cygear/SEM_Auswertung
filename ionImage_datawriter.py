import xlwt

def data_output(filename, col_names, col_values):
    book = xlwt.Workbook()
    sh = book.add_sheet(sheetname='Sheet1', cell_overwrite_ok= True)
    #sh = book.add_sheet(sheet)


    #You may need to group the variables together
    #for n, (v_desc, v) in enumerate(zip(desc, variables)):
    # for n, v_desc, v in enumerate(zip(col_names, col_values)):
    #     sh.write(0, n, col_names)
    #     sh.write(1, n, col_values)


    for i in range(len(col_names)):
        sh.write(0, i, col_names[i])

    for i in range(len(col_values)):
        sh.write(1, i, col_values[i])


    book.save(filename + '.xls')