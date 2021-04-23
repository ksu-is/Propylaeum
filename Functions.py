from flask import Flask, render_template, request, Markup
rowIDs = []
rowStartIDs = []


app=Flask(__name__)
@app.route('/rows/', methods=['POST'])
def seats():
    #Create new section from form data
    current_section = request.form['sectionName']
    venueName = request.form['venueName']
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
        # define list to store html form fields
        table = []
        # define list to store input ids
        #rowIDs = []
        #rowStartIDs = []

        for count in range(0,len(rows)):
            # create new table row
            rowName = str(rows[count])
            inputName = "row"+str(count)
            rowStart = inputName+"startValue"

            table.append("<tr><td class='label'>"+rowName+"</td><td class='seatCount'><input type='text' name='"+inputName+"'></td><td class='seatCount'><input type='text' placeholder='101' name='"+rowStart+"'></td></tr>")
            
            # append IDs to lists for easier recall later
            rowIDs.append(inputName)
            rowStartIDs.append(rowStart)

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
    
    return render_template("rows.html",formArea=rowsTable(),sectionName=current_section,venueName=venueName)

@app.route('/seats/', methods=['POST'])
# create seat inputs as <td>
def seatForm():
    seatDataEntry = []


    
    rows = 3 # placeholder until I can figure out how to pass data between forms



    for count in range(0,int(rows)):
        current_row = rowIDs[count]
        rowStart = rowStartIDs[count]
        seats = request.form[current_row]

        # generate inputs for current row
        seatDataEntry.append("<tr><td class='label'>"+(count+1)+"</td>")
        # add seats to a row
        for seat in range(0,int(seats)):
            seatDataEntry.append("<td><svg class='seatSVG' data-name='Layer 1' xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16.75 16'><g><g><rect class='cls-1' x='1.63' y='0.13' width='13.5' height='15.75' rx='2.25'/></g><g><path class='cls-2' d='M15.13.88h0a.76.76,0,0,1-.75.75h-12A.75.75,0,0,1,1.63.88h0A.74.74,0,0,1,2.38.13h12A.75.75,0,0,1,15.13.88Z'/></g><g><rect class='cls-1' x='15.13' y='2.53' width='1.5' height='10.5'/></g><g><rect class='cls-1' x='0.13' y='2.53' width='1.5' height='10.5'/></g></g></svg><br><br><input type='text' placeholder='"+(int(rowStart) + seat)+"' class='seatNumber' id='"+current_row+"seat"+(seat + 1)+"'/></td>")
        seatDataEntry.append("</tr>")
    
    #return table as html markup
    return Markup(' '.join(seatDataEntry))

    return render_template("seats.html",formArea=seatForm())
            

        

@app.route('/')
def form():
    return render_template("form.html")

if __name__=="__main__":
    app.run(debug=True)