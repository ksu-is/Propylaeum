# Propylaeum: Seating Diagrams for the 21st Century

Propylaeum is an application for generating interactive seating diagrams. Managers of event venues can use Propylaeum to model their seating options and track availability as tickets are sold.

### Background
Working in the audiovisual industry, I realized that smaller venues are generally too understaffed to `1` create visual diagrams for their renters that intuitively present the seating options of the venue, `2` track tickets issued by their renters, and `3` validate ticket quantities against the capacity of the facility.

Propylaeum aims to make it easier for venues to address these deficiencies.

**Primary Development Goals**
---

1. Create an application that dynamically generates seating diagrams from user input:
 * Number of distinct seating sections and their names
 * Number of rows in each section
 * Number of seats in each row

2. Create a python function to identify and interpret patterns in the naming taxonomy of seats and rows, based on analysis of user input
 * Often, seats are incremented as “odd” or “even” based on their location in the venue. Some rows may differ from others, but the patterns are usually generic.
 * Venues often increment rows either with letters `[AA, BB, CC]` or large numbers `[100, 200, 300]`.
 * By finding patterns, we can simplify the process of labeling elements in diagrams.

3. Develop an application framework with flask to pass data between the front and back end
 * A page with dynamically generated form fields, used to gather input to create new diagrams
 * A page to view , in which a user can select seats from a visual diagram and set their status to either `unavailable`, `available`, or `occupied`
    * This interface will display a live summary of seating counts for each class.
    * SVG seats change colors based on their class.
***
## Images
[![Sample Form](https://i.imgur.com/6oLxl58.jpg)]()
> *This screenshot shows a previous attempt at creating this application before I knew Python (July of 2019). Using HTML and a bit of JavaScript, this diagram was generated with minimal user input.*
---

## Sample Form Generation
>Since form inputs are variable based on the quantities of seats, rows, and sections of a venue, some aspects must be generated dynamically. This function generates HTML code for a tabular form, used to specify seat counts for each row. 

```python
def rowsTable(rows):
    table = []

    for count in range(0,len(rows)):
        # create new table row
        rowName = str(rows[count])
        inputName = "seats-Row"+str(count)
        table.append("<tr><td class='label'>"+rowName+"</td><td class='seatCount'><input type='text' name='"+inputName+"'></td></tr>")
        
    #return table as html markup
    return Markup(' '.join(table))
```
---

## Contributors
| <a href="https://www.linkedin.com/in/bperky/" target="_blank">**Ben Perkins**</a>  |
|:-----:|
|[![Ben Perkins](https://avatars.githubusercontent.com/u/36800016?v=4&s=200)](https://www.linkedin.com/in/bperky/) |
| <a href="http://github.com/bperky" target="_blank">`github.com/bperky`</a> |

---

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2021 © Ben Perkins.
