from flask import Flask, render_template, request, Markup
rowIDs = []
rowStartIDs = []


app=Flask(__name__)
@app.route('/rows/', methods=['POST'])
# create new form from user input

def seats():
    # declare variables
    sectionName = request.form['sectionName']
    venueName = request.form['venueName']
    section_rows = request.form['rowCount']
    row_count = int(section_rows)
    rowTaxonomy = request.form['rowTaxonomy']
    firstRow = request.form['firstRow']

    rows = []
    row_seat_count = []
    
    #determine layout of row data entry page
    if rowTaxonomy == "numeric":
        current_row = int(firstRow)
        while row_count > 0:
            rows.append(str(current_row))
            current_row += 1
            row_count -= 1
            if row_count <= 0:
                break
    elif rowTaxonomy == "alpha":
        current_row = ord(firstRow)
        while row_count > 0:
            rows.append(str(chr(current_row)))
            current_row += 1
            row_count -= 1
            if row_count <= 0:
                break

    # generate a form to add seats to rows
    def rowsTable():
        # define list to store html form fields
        formInputs = []
        rowNames = []

        for count in range(0,len(rows)):
            # create new table row
            row = str(rows[count])
            inputName = "row"+str(count)
            rowStart = inputName+"startValue"

            # store row label
            rowNames.append(row)

            formInputs.append("<tr><td class='label'>"+row+"</td><td class='seatCount'><input type='text' name='"+inputName+"'></td><td class='seatCount'><input type='text' placeholder='101' name='"+rowStart+"'></td></tr>")

        # prepare csv for data storage 
        import csv    

        from csv import DictWriter
        def append_dict_as_row(file_name, dict_of_elem, field_names):
            # Open file in append mode
            with open(file_name, 'a+', newline='') as write_obj:
                # Create a writer object from csv module
                dict_writer = DictWriter(write_obj, fieldnames=field_names)
                # Add dictionary as wor in the csv
                dict_writer.writerow(dict_of_elem)

        # If empty entries are missed then DictWriter will handle them automatically
        field_names = ['Venue', 'Section', 'Rows'] 
        row_dict = {'Venue': venueName, 'Section':sectionName, 'Rows':rowNames}
        # Append a dict missing entries as a row in csv file
        append_dict_as_row('venueData.csv', row_dict, field_names)

        seatNames = []
        

        #return table as html markup
        return Markup(' '.join(formInputs))
    
    return render_template("rows.html",formArea=rowsTable(),sectionName=sectionName,venueName=venueName,seatForm="")

@app.route('/seats/', methods=['POST'])
# create seat inputs as <td>
def seatForm():
    datasource = open('venuData.csv', 'r')
    rowData = datasource.readline()
    print(rowData)
    seatNames = []

    for count in range(0,len(rowNames)):
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