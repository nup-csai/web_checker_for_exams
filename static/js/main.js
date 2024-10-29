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

    console.log(data)

    for (let i = 0; i < data.length; i++) {
        const row = document.createElement('tr');
        if (data[i][1] === 'OK') {
            row.classList.add('light-green');
        } else {
            row.classList.add('light-red');
        }

        for (let j = 0; j < 2; j++) {
            const td = document.createElement('td');
            td.textContent = `${data[i][j]}`;
            row.appendChild(td);
        }

        table.appendChild(row);
    }

    tableContainer.appendChild(table);
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
        add_table(data.testing_data);
    });
};


document.getElementById('SubmitRepositoryNameButton').onclick = function() {
    const text = document.getElementById('repositoryNameInput').value;

    fetch('/check_solution_from_github', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: text }),
    })
    .then(response => response.json())
    .then(data => {
        add_table(data.testing_data);
    });
};