async function CreateFunction(event) {
    event.preventDefault();  // Предотвращаем стандартное действие формы

    const form = document.getElementById('create-form');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    console.log(data);

    try {
        const response = await fetch('/incidents/client/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const errorData = await response.json();
            displayErrors(errorData);
            return;
        }

        const result = await response.json();
        alert('Успешно!')

    } catch (error) {

        alert('Произошла ошибка при входе. Пожалуйста, попробуйте снова.');
    }
}