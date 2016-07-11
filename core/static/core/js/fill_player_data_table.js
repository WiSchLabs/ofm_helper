// Fill data table with custom content

var tableBody = document.getElementById('player_data_table_body')

var data = new Array()
data[0] = new Array("MS", "Laurenz Lopes" , "12162" , "11138" , "11627" ,"16", "103", "11", "22", "26", "73", "28" ,"59" ,"0" ,"0", "9717255")

for (var i = 0; i < data.length; i++) {
    var tr = document.createElement('TR');
    for (var j = 0; j < data[i].length; j++) {
        var td = document.createElement('TD')
        td.appendChild(document.createTextNode(data[i][j]));
        tr.appendChild(td)
    }
    tableBody.appendChild(tr);
}