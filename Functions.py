from flask import Flask, render_template, request, Markup
import os
# import pandas
import pandas as pd

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

def get_last_n_lines(file_name, N):
    # Create an empty list to keep the track of last N lines
    list_of_lines = []
    # Open file for reading in binary mode
    with open(file_name, 'rb') as read_obj:
        # Move the cursor to the end of the file
        read_obj.seek(0, os.SEEK_END)
        # Create a buffer to keep the last read line
        buffer = bytearray()
        # Get the current position of pointer i.e eof
        pointer_location = read_obj.tell()
        # Loop till pointer reaches the top of the file
        while pointer_location >= 0:
            # Move the file pointer to the location pointed by pointer_location
            read_obj.seek(pointer_location)
            # Shift pointer location by -1
            pointer_location = pointer_location -1
            # read that byte / character
            new_byte = read_obj.read(1)
            # If the read byte is new line character then it means one line is read
            if new_byte == b'\n':
                # Save the line in list of lines
                list_of_lines.append(buffer.decode()[::-1])
                # If the size of list reaches N, then return the reversed list
                if len(list_of_lines) == N:
                    return list(reversed(list_of_lines))
                # Reinitialize the byte array to save next line
                buffer = bytearray()
            else:
                # If last read character is not eol then add it in buffer
                buffer.extend(new_byte)
        # As file is read completely, if there is still data in buffer, then its first line.
        if len(buffer) > 0:
            list_of_lines.append(buffer.decode()[::-1])
    # return the reversed list
    return list(reversed(list_of_lines))

svg = "<td><svg id='seatSVG' data-name='Layer 1' xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16.75 16'><title>Seat</title><g id='group422-619'><g id='shape418-620'><rect class='cls-1' x='1.63' y='0.13' width='13.5' height='15.75' rx='2.25'/></g><g id='shape419-622'><path class='cls-2' d='M15.13.88h0a.76.76,0,0,1-.75.75h-12A.75.75,0,0,1,1.63.88h0A.74.74,0,0,1,2.38.13h12A.75.75,0,0,1,15.13.88Z'/></g><g id='shape420-624'><rect class='cls-1' x='15.13' y='2.53' width='1.5' height='10.5'/></g><g id='shape421-626'><rect class='cls-1' x='0.13' y='2.53' width='1.5' height='10.5'/></g></g></svg>"

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

        # If empty entries are missed then DictWriter will handle them automatically
        field_names = ['Venue', 'Section', 'Rows'] 
        row_dict = {'Venue': venueName, 'Section':sectionName, 'Rows':rowNames}
        # Append a dict missing entries as a row in csv file
        append_dict_as_row('venueData.csv', row_dict, field_names)
        

        #return table as html markup
        return Markup(' '.join(formInputs))
    
    return render_template("rows.html",formArea=rowsTable(),sectionName=sectionName,venueName=venueName,seatForm="")

@app.route('/seats/', methods=['POST'])
# create seat inputs as <td>
def seatForm():

    def formFunctions():

        # read CSV file
        df = pd.read_csv('venueData.csv', error_bad_lines=False)
        venueNames = df['Venue'].tolist()
        sectionNames = df['Section'].tolist()
        venueData = df['Rows'].tolist()

        venueName = venueNames[-1]
        sectionName = sectionNames[-1]

        rowData = venueData[-1]

        remove = ['"',"'"]
        for value in remove:
            rowList = rowData.replace(value, '')

        rowListNoBrackets = str(rowList)[1:-1]
        
        rowNames = list(rowListNoBrackets.split(','))
        
        def listToStringWithoutBrackets(list1):
            return str(list1).replace('[','').replace(']','')

        seatDataEntry = []
        seatNames = []

        for count in range(0,(len(rowNames))):
            # declare variable names
            inputName = "row"+str(count)
            rowStart = inputName+"startValue"
            # get form variables
            seatCount = request.form[inputName]
            seatStart = int(request.form[rowStart])

            currentSeat = seatStart
            currentRowSeats = []

            seatDataEntry.append("<tr><td class='rowLabel'>"+rowNames[count]+"</td>")
            
            for seat in range(0,int(seatCount)):
                seatNo = currentSeat

                currentRowSeats.append(seatNo)

                # generate inputs for current row
                
                seatDataEntry.append("<td>"+svg+"<input class='seatInput' type='text' value='"+str(currentSeat)+"' class='seatNumber' id='row"+str(count+1)+"seat"+str(seat+1)+"'/></td>")
                currentSeat += 1
                
            seatDataEntry.append("</tr>")
            seatNames.append(currentRowSeats)

        # If empty entries are missed then DictWriter will handle them automatically
        field_names = ['Venue', 'Section', 'Rows', 'Seats'] 
        row_dict = {'Venue': venueName, 'Section':sectionName, 'Rows':rowNames, 'Seats':seatNames}
        # Append a dict missing entries as a row in csv file
        append_dict_as_row('venues.csv', row_dict, field_names)
        
        #return table as html markup
        return Markup(' '.join(seatDataEntry))

    return render_template("seats.html",formArea=formFunctions())
            

        

@app.route('/')
def form():
    return render_template("form.html")

if __name__=="__main__":
    app.run(debug=True)