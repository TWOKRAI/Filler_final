document.addEventListener('DOMContentLoaded', function() {
    const drink1Input = document.getElementById('drink1');
    const drink2Input = document.getElementById('drink2');
    const statusSwitch = document.getElementById('statusSwitch');
    const statusText = document.getElementById('statusText');
    const statusInfo = document.getElementById('status_info');
    const statusInput = document.createElement('input');

    statusInput.type = 'hidden';
    statusInput.name = 'status';

    document.getElementById('drinkForm').appendChild(statusInput);

    const translations = {
        on: document.getElementById('trans-on').textContent,
        off: document.getElementById('trans-off').textContent,
        info: {
            0: document.getElementById('trans-info-0').textContent,
            1: document.getElementById('trans-info-1').textContent,
            2: document.getElementById('trans-info-2').textContent,
        },

        info2: {
            0: document.getElementById('trans-info2-0').textContent,
            1: document.getElementById('trans-info2-1').textContent,
            2: document.getElementById('trans-info2-2').textContent,
            3: document.getElementById('trans-info2-3').textContent,
            4: document.getElementById('trans-info2-4').textContent,
            5: document.getElementById('trans-info2-5').textContent,
            6: document.getElementById('trans-info2-6').textContent,
        }
    };

    const color_green = '#30700b'
    const color_orange = '#f19101'

    function updateStatus(status) {
        statusText.textContent = status ? translations.on : translations.off;
        statusText.style.color = status ? color_green : 'red';
        statusSwitch.checked = status;
        statusInput.value = status;
    }

    function updateStatusInfo(info) {
        const statusInfo = document.getElementById('status_info');
        const statusCircle = document.getElementById('status_circle');

        statusInfo.textContent = translations.info[info];
    }

    function updateStatusInfoColor(info) {
        const statusInfo = document.getElementById('status_info');
        const statusCircle = document.getElementById('status_circle');

        switch (info) {
            case 0:
                statusInfo.style.color = color_green;
                statusCircle.style.backgroundColor = color_green;
                break;
            case 1:
                statusInfo.style.color = color_orange;
                statusCircle.style.backgroundColor = color_orange;
                break;
            case 2:
                statusInfo.style.color = 'red';
                statusCircle.style.backgroundColor = 'red';
                break;

            default:
                statusInfo.style.color = 'black';
                statusCircle.style.backgroundColor = 'black';
        }
    }

    function updateStatusInfoSize(info) {
        const statusInfo = document.getElementById('status_info');

        switch (info) {
            case 0:
                statusInfo.style.fontSize = '16px';
                break;
            case 1:
                statusInfo.style.fontSize = '15px';
                break;
            case 2:
                statusInfo.style.fontSize = '16px';
                break;
            default:
                statusInfo.style.fontSize = '16px';
        }
    }

    function updateStatusInfo2(info) {
        const statusInfo2 = document.getElementById('status_info2');

        statusInfo2.textContent = translations.info2[info]
    }

    function updateStatusInfo2Color(info) {
        const statusInfo2 = document.getElementById('status_info2');

        switch (info) {
            case 0:
                statusInfo2.style.color = color_green;
                break;
            case 1:
                statusInfo2.style.color = color_orange;
                break;
            case 2:
                statusInfo2.style.color = 'red';
                break;
            default:
                statusInfo2.style.color = 'black';
        }

    }

    function updateStatusInfo2Size(info) {
        const statusInfo2 = document.getElementById('status_info2');

        switch (info) {
            case 0:
            case 1:
            case 2:
            case 3:
            case 4:
            case 6:
                statusInfo2.style.fontSize = '15px';
                break;
            case 5:
                statusInfo2.style.fontSize = '14px';
                break;
            default:
                statusInfo2.style.fontSize = '16px';
        }
    }

    function validateInput(input) {
        let value = parseFloat(input.value);

        if (isNaN(value) || input.value.trim() === '') {
            value = 0;
        } else {
            value = Math.round(value);
            if (value < 0) {
                value = 0;
            } else if (value > 500) {
                value = 500;
            }
        }
        input.value = value;

        const event = new Event('change');
        input.dispatchEvent(event);
    }

    function sendData(formData) {
        fetch('', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log('Response data:', data);
            updateStatus(data.status);

            updateStatusInfo(data.info);
            updateStatusInfoColor(data.info);
            updateStatusInfoSize(data.info);

            updateStatusInfo2(data.info2);
            updateStatusInfo2Color(data.info);
            updateStatusInfo2Size(data.info2);
        })
        .catch(error => console.error('Error:', error));
    }

    function updateData() {
        $.ajax({
            url: '/get_data/',
            method: 'GET',
            success: function(data) {
                drink1Input.value = data.drink1;
                drink2Input.value = data.drink2;

                updateStatus(data.status);

                updateStatusInfo(data.info);
                updateStatusInfoColor(data.info);
                updateStatusInfoSize(data.info);

                updateStatusInfo2(data.info2);
                updateStatusInfo2Color(data.info);
                updateStatusInfo2Size(data.info2);
            },
            error: function(error) {
                console.error('Error fetching data:', error);
            }
        });
    }

    function showConfirmDialog(callback) {
        const confirmDialog = document.getElementById('confirmDialog-default');
        confirmDialog.style.display = 'block';

        document.getElementById('confirmButton-default').onclick = function() {
            callback(true);
            confirmDialog.style.display = 'none';
        };

        document.getElementById('cancelButton-default').onclick = function() {
            callback(false);
            confirmDialog.style.display = 'none';
        };
    }

    let updateInterval;
    let inactivityTimeout;

    function startUpdateInterval() {
        if (!updateInterval) {
            updateInterval = setInterval(updateData, 2100);
        }
    }

    function stopUpdateInterval() {
        clearInterval(updateInterval);
        updateInterval = null;
    }

    function resetInactivityTimeout() {
        clearTimeout(inactivityTimeout);
        inactivityTimeout = setTimeout(stopUpdateInterval, 60000);
    }

    function handleUserActivity() {
        resetInactivityTimeout();
        startUpdateInterval();
    }

    if (drink1Input && drink2Input && statusInput) {
        drink1Input.addEventListener('input', function() {
            validateInput(drink1Input);
            handleUserActivity();
        });

        drink2Input.addEventListener('input', function() {
            validateInput(drink2Input);
            handleUserActivity();
        });

        drink1Input.addEventListener('change', function() {
            console.log('Drink1 changed:', drink1Input.value);
            const formData = new FormData(document.getElementById('drinkForm'));
            sendData(formData);
            handleUserActivity();
        });

        drink2Input.addEventListener('change', function() {
            console.log('Drink2 changed:', drink2Input.value);
            const formData = new FormData(document.getElementById('drinkForm'));
            sendData(formData);
            handleUserActivity();
        });

        function handleStatusChange() {
            if (statusSwitch.checked) {
                showConfirmDialog(function(confirmed) {
                    const formData = new FormData(document.getElementById('drinkForm'));
                    formData.append('status', true);
                    if (confirmed) {
                        formData.append('pumping_ready', false);
                        formData.append('drink1', 30);
                        formData.append('drink2', 30);
                        formData.append('info', 1);
                        formData.append('info2', 1);
                    } else {
                        formData.append('pumping_ready', true);
                        formData.append('info', 0);
                        formData.append('info2', 1);
                    }
                    sendData(formData);
                    statusSwitch.checked = true; // Установить состояние свитча после подтверждения
                });
                statusSwitch.checked = false; // Временно отключить состояние свитча
            } else {
                const formData = new FormData(document.getElementById('drinkForm'));
                formData.append('status', false);
                sendData(formData);
            }
            handleUserActivity();
        }

        statusSwitch.addEventListener('change', handleStatusChange);

        updateData();
        startUpdateInterval();
        resetInactivityTimeout();

        document.addEventListener('visibilitychange', function() {
            if (!document.hidden) {
                handleUserActivity();
            }
        });

    } else {
        console.error('One or more elements are missing in the DOM.');
    }
});
