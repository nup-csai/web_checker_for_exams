import {DynamicFields} from "./dynamic_fields.js";


function add_table(data){

    document.getElementById('tableContainer').innerHTML = '';

    for (let i = 0;i < data.length;i ++) {
        const h3 = document.createElement('h3');
        h3.textContent = `Repository ${i+1}`
        tableContainer.appendChild(h3);
        const repo_data = data[i];
        console.log(`repo_data: ${repo_data}`);
        if (!repo_data.routes_checking){
            const p = document.createElement('p');
            p.textContent = 'Has not been checked yet.';
            tableContainer.appendChild(p);
            break;
        }
        const table = document.createElement('table');
        const headerRow = document.createElement('tr');
        const headers = ['Test №', 'Status'];
        headers.forEach(headerText => {
            const th = document.createElement('th');
            th.textContent = headerText;
            headerRow.appendChild(th);
        });
        table.appendChild(headerRow);

        for (let i = 0; i < repo_data.routes_checking.length; i++) {
            const row = document.createElement('tr');
            if (repo_data.routes_checking[i][1] === 'OK') {
                row.classList.add('light-green');
            } else {
                row.classList.add('light-red');
            }

            for (let j = 0; j < 2; j++) {
                const td = document.createElement('td');
                td.textContent = `${repo_data.routes_checking[i][j]}`;
                row.appendChild(td);
            }

            table.appendChild(row);
        }

        const routes_header = document.createElement("h4");
        routes_header.textContent = "Routes";

        const files_header = document.createElement("h4");
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

        for (let i = 0; i < repo_data.files_checking.length; i++) {
            const row = document.createElement('tr');
            if (repo_data.files_checking[i][1] === 'OK') {
                row.classList.add('light-green');
            } else {
                row.classList.add('light-red');
            }

            for (let j = 0; j < 2; j++) {
                const td = document.createElement('td');
                td.textContent = `${repo_data.files_checking[i][j]}`;
                row.appendChild(td);
            }

            table2.appendChild(row);
        }

        tableContainer.appendChild(table2);
    }
}


document.getElementById('check_solutions').onclick = function () {
    const eventSource = new EventSource("/check_solution_from_github");

    eventSource.onmessage = function(event) {
        try {
            const data = JSON.parse(event.data);
            add_table(data.data);
        } catch (error) {
            console.log('error');
            console.log(event.data);
        }
    };

    eventSource.onerror = function() {
        console.error("Connection error");
        eventSource.close();
    };
};


const fields1 = new DynamicFields('repositories', 'repositoryContainer',
    'addRepositoryBtn', 'applyRepositoriesBtn');
const fields2 = new DynamicFields('files', 'filesContainer1',
    'addFileBtn', 'applyFilesBtn');
