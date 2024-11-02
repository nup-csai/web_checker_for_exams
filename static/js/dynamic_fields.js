export class DynamicFields {
    constructor(name, containerId, addButtonId, submitButtonId) {
        this.name = name;
        this.container = document.getElementById(containerId);
        this.addButton = document.getElementById(addButtonId);
        this.submitButton = document.getElementById(submitButtonId);

        if (!this.container || !this.addButton || !this.submitButton) {
            console.error('One or more elements not found. Check IDs.');
            return;
        }

        this.addButton.addEventListener('click', () => this.addField());
        this.submitButton.addEventListener('click', () => this.submitFields());
    }

    addField() {
        const inputGroup = document.createElement('div');
        inputGroup.className = 'input-group';

        const div= document.createElement('div');

        const newInput = document.createElement('input');
        newInput.type = 'text';
        newInput.placeholder = 'Enter text';

        const removeBtn = document.createElement('button');
        removeBtn.innerHTML = '&times;';
        removeBtn.className = 'remove-btn';

        removeBtn.addEventListener('click', () => this.removeField(inputGroup));

        div.appendChild(newInput);
        div.appendChild(removeBtn);

        inputGroup.appendChild(div);

        this.container.appendChild(inputGroup);
    }

    removeField(inputGroup) {
        this.container.removeChild(inputGroup);
    }

    submitFields() {
        const inputs = this.container.getElementsByTagName('input');
        const values = [];

        for (const input of inputs) {
            values.push(input.value);
        }
        console.log(values);

        fetch(`/dynamic_fields/${this.name}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ data: values }),
        })
        .then(response => response.json())
        .then(data => console.log("Data submitted:", data))
        .catch(error => console.error("Error:", error));
    }
}
