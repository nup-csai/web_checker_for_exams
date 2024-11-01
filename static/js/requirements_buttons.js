const addFieldBtn = document.getElementById('addFieldBtn');
const submitBtn = document.getElementById('submitBtn');
const inputContainer = document.getElementById('inputContainer');


addFieldBtn.addEventListener('click', () => {
    const inputGroup = document.createElement('div');
    inputGroup.className = 'input-group';

    const n = document.getElementsByClassName("input-group").length;
    inputGroup.innerHTML = `<h3>Requirement ${n}<h3>`;

    const h4 = document.createElement("h4");
    h4.textContent = "Route";

    const newInput = document.createElement('input');
    newInput.type = 'text';
    newInput.placeholder = 'Enter text';

    const removeBtn = document.createElement('button');
    removeBtn.innerHTML = '&times;';
    removeBtn.className = 'remove-btn';

    removeBtn.addEventListener('click', () => {
        inputContainer.removeChild(inputGroup);
        const elements = document.getElementsByClassName("input-group");
        for (let i = 0; i < elements.length; i += 1) {
            const h3 = elements[i].querySelector("h3");
            if (h3) {
                h3.textContent = `Requirement ${i}`;
            }
        }
    });

    const h4_2 = document.createElement("h4");
    h4_2.textContent = "Content";

    const textarea = document.createElement("textarea");
    textarea.rows = 5;
    textarea.cols = 30;
    textarea.placeholder = "Enter the expected content of the page corresponding to this route...";

    inputGroup.appendChild(h4);
    inputGroup.appendChild(newInput);
    inputGroup.appendChild(removeBtn);
    inputGroup.appendChild(h4_2);
    inputGroup.appendChild(textarea);

    inputContainer.appendChild(inputGroup);
});


submitBtn.addEventListener('click', () => {
    const inputs = inputContainer.getElementsByTagName('input');
    const text_areas = inputContainer.getElementsByTagName("textarea");
    const values = [];
    for (let i = 0;i < inputs.length;i++) {
        values.push([inputs[i].value, text_areas[i].value]);
    }
    fetch('/apply_requirements', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({routes: values}),
    })
        .then(response => response.json())
});