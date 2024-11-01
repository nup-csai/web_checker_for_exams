export function add_routes(routes, answers) {
    const addFieldBtn = document.getElementById('addFieldBtn');

    for (let i = 0; i < routes.length; i++) {
        addFieldBtn.click();

        const inputGroups = document.getElementsByClassName('input-group');
        const lastInputGroup = inputGroups[inputGroups.length - 1];

        const inputField = lastInputGroup.querySelector('input');
        inputField.value = routes[i];

        const textareaField = lastInputGroup.querySelector('textarea');
        textareaField.value = answers[i];
    }
}