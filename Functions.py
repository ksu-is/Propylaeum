from flask import Flask, render_template, request, Markup

app=Flask(__name__)
@app.route('/seats/', methods=['POST'])
def seats():
    #Create new section from form data
    current_section = request.form['sectionName']
    section_rows = request.form['rowCount']
    row_count = int(section_rows)
    id_style = request.form['rowTaxonomy']
    row1 = request.form['firstRow']

    rows = []
    row_seat_count = []
    
    #determine layout of row data entry page
    if id_style == "numeric":
        current_row = int(row1)
        while row_count > 0:
            rows.append(str(current_row))
            current_row += 1
            row_count -= 1
            if row_count <= 0:
                break
    elif id_style == "alpha":
        current_row = ord(row1)
        while row_count > 0:
            rows.append(str(chr(current_row)))
            current_row += 1
            row_count -= 1
            if row_count <= 0:
                break

    # generate a form to add seats to rows
    def rowsTable():
        table = []
        for count in range(0,len(rows)):
            # create new table row
            rowName = str(rows[count])
            inputName = "seats-Row"+str(count)
            table.append("<tr><td class='label'>"+rowName+"</td><td class='seatCount'><input type='text' name='"+inputName+"'></td></tr>")
            
            # add seat name inputs as <td>
            #rowSeatCount = request.form[inputName] # <----- This returns an error - 400 Bad Request. It needs to go somewhere else
            
            #if type(rowSeatCount) == int:
            #    for number in range(0,rowSeatCount):
            #        table.append("<td class='seat'><input type='text' placeholder='"+str(number)+"' name='row"+str(count)+"seat"+str(number)+"'></#td>")
            #else:
            #    pass            
            
            #end row
            #table.append("</tr>")
        #return table as html markup
        return Markup(' '.join(table))
    
    return render_template("seating.html",formArea=rowsTable(),sectionName=current_section)

@app.route('/')
def form():
    return render_template("form.html")

if __name__=="__main__":
    app.run(debug=True)