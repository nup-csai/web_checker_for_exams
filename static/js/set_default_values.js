function add_routes(routes, answers) {
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

    const applySettingsBtn = document.getElementById('submitBtn');
    applySettingsBtn.click();
}

function add_fields(values, addFieldBtnId, applyBtnId, containerId) {
    const addFieldBtn = document.getElementById(addFieldBtnId);
    const container = document.getElementById(containerId);

    for (let value of values) {
        addFieldBtn.click();
        const elements = container.querySelectorAll('.input-group');
        const lastElement = elements[elements.length - 1];
        const inputField = lastElement.querySelector('input');
        inputField.value = value;
    }

    const applyBtn = document.getElementById(applyBtnId);
    applyBtn.click();
}

add_routes(['/hello Miku!', '/hello World!', '/about'],
['Hello, Miku', 'Hello, World', 'This is about page']);

setTimeout(() => {
    add_fields(['https://github.com/KonstBeliakov/test_repository.git'], 'addRepositoryBtn',
    'applyRepositoriesBtn', 'repositoryContainer');

    add_fields(['Dockerfile', 'main.py', 'utils.py'], 'addFileBtn',
    'applyFilesBtn', 'filesContainer1')
}, 100);
