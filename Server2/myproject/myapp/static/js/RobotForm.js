document.addEventListener('DOMContentLoaded', function() {
    const inputSpeed = document.getElementById('speed');
    const inputWaiting = document.getElementById('waiting');

    const container = document.querySelector('.container2');
    const body = document.body;
    const toggleButton = document.getElementById('toggleButton');
    const backButton = document.getElementById('backButton');
    const applyButton = document.getElementById('applyButton');
    const confirmDialog = document.getElementById('confirmDialog');
    const confirmButton = document.getElementById('confirmButton');
    const cancelButton = document.getElementById('cancelButton');
    const robotForm = document.getElementById('robotForm');
    const defaultButton = document.getElementById('defaultButton');
    const confirmDialogDefault = document.getElementById('confirmDialog-default');
    const confirmButtonDefault = document.getElementById('confirmButton-default');
    const cancelButtonDefault = document.getElementById('cancelButton-default');

    // Получаем URL из атрибута data-index-url
    const indexUrl = robotForm.getAttribute('data-index-url');

    function validateInput(input, min = 0, max = 500) {
        let value = parseFloat(input.value);

        if (isNaN(value) || input.value.trim() === '') {
            value = min;
        } else {
            value = Math.round(value);
            if (value < min) {
                value = min;
            } else if (value > max) {
                value = max;
            }
        }
        input.value = value;

        const event = new Event('change');
        input.dispatchEvent(event);
    }

    if (container && toggleButton) {
        toggleButton.addEventListener('click', function() {
            container.classList.toggle('expanded');
            body.classList.toggle('expanded');

            if (container.classList.contains('expanded')) {
                toggleButton.textContent = '{% trans "Show Less" %}';
                console.log('Container expanded');
            } else {
                toggleButton.textContent = '{% trans "Show More" %}';
                console.log('Container collapsed');
            }
        });
    } else {
        console.error('Container or toggleButton not found');
    }

    if (inputSpeed && inputWaiting) {
        inputSpeed.addEventListener('input', function() {
            validateInput(inputSpeed, 0, 100);
        });

        inputWaiting.addEventListener('input', function() {
            validateInput(inputWaiting, 0, 10);
        });
    }

    applyButton.addEventListener('click', function() {
        confirmDialog.style.display = 'block';
    });

    confirmButton.addEventListener('click', function() {
        confirmDialog.style.display = 'none';

        // Отправка формы на сервер с использованием fetch
        const formData = new FormData(robotForm);

        fetch(robotForm.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        }).then(response => {
            if (response.ok) {
                // Перенаправление на текущую страницу после успешной отправки формы
                window.location.href = indexUrl;
            } else {
                console.error('Form submission failed');
            }
        }).catch(error => {
            console.error('Error:', error);
        });
    });

    cancelButton.addEventListener('click', function() {
        confirmDialog.style.display = 'none';
    });

    defaultButton.addEventListener('click', function() {
        confirmDialogDefault.style.display = 'block';
    });

    confirmButtonDefault.addEventListener('click', function() {
        confirmDialogDefault.style.display = 'none';

        // Отправка запроса на сервер для сброса до дефолтных значений
        fetch(resetUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        }).then(response => {
            if (response.ok) {
                // Перезагрузка страницы для обновления данных
                window.location.reload();
            } else {
                console.error('Reset to default failed');
            }
        }).catch(error => {
            console.error('Error:', error);
        });
    });

    cancelButtonDefault.addEventListener('click', function() {
        confirmDialogDefault.style.display = 'none';
    });
});
