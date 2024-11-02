import {DynamicFields} from "./dynamic_fields.js";


function add_table(data){

    document.getElementById('tableContainer').innerHTML = '';

    const table = document.createElement('table');
    const headerRow = document.createElement('tr');
    const headers = ['Test №', 'Status'];
    headers.forEach(headerText => {
        const th = document.createElement('th');
        th.textContent = headerText;
        headerRow.appendChild(th);
    });
    table.appendChild(headerRow);

    for (let i = 0; i < data.routes_checking.length; i++) {
        const row = document.createElement('tr');
        if (data.routes_checking[i][1] === 'OK') {
            row.classList.add('light-green');
        } else {
            row.classList.add('light-red');
        }

        for (let j = 0; j < 2; j++) {
            const td = document.createElement('td');
            td.textContent = `${data.routes_checking[i][j]}`;
            row.appendChild(td);
        }

        table.appendChild(row);
    }

    const routes_header = document.createElement("h3");
    routes_header.textContent = "Routes";

    const files_header = document.createElement("h3");
    files_header.textContent = "Files";

    tableContainer.appendChild(routes_header);
    tableContainer.appendChild(table);
    tableContainer.appendChild(files_header);

    const table2 = document.createElement('table');
    const headerRow2 = document.createElement('tr');
    const headers2 = ['File', 'Status'];
    headers2.forEach(headerText2 => {
        const th = document.createElement('th');
        th.textContent = headerText2;
        headerRow2.appendChild(th);
    });
    table2.appendChild(headerRow2);

    for (let i = 0; i < data.files_checking.length; i++) {
        const row = document.createElement('tr');
        if (data.files_checking[i][1] === 'OK') {
            row.classList.add('light-green');
        } else {
            row.classList.add('light-red');
        }

        for (let j = 0; j < 2; j++) {
            const td = document.createElement('td');
            td.textContent = `${data.files_checking[i][j]}`;
            row.appendChild(td);
        }

        table2.appendChild(row);
    }

    tableContainer.appendChild(table2);
}


document.getElementById('submitButton').onclick = function() {
    const text = document.getElementById('textInput').value;

    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: text }),
    })
    .then(response => response.json())
    .then(data => {
        add_table(data);
    });
};


document.getElementById('check_solutions').onclick = function () {
    fetch('/check_solution_from_github', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        add_table(data);
    });
};


const fields1 = new DynamicFields('repositories', 'repositoryContainer',
    'addRepositoryBtn', 'applyRepositoriesBtn');
const fields2 = new DynamicFields('files', 'filesContainer1',
    'addFileBtn', 'applyFilesBtn');
