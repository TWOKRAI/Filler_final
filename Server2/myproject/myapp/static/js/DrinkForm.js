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

        switch (info) {
            case 0:
                statusInfo.style.color = color_green;
                statusCircle.style.backgroundColor = color_green; 
                break;
            case 1:
            case 2:
            case 3:
                statusInfo.style.color = color_orange;
                statusCircle.style.backgroundColor = color_orange;
                break;
            case 4:
                statusInfo.style.color = 'red';
                statusCircle.style.backgroundColor = 'red';
                break;
            default:
                statusInfo.style.color = 'black';
                statusCircle.style.backgroundColor = 'black';
        }
    }


    function updateStatusInfo2(info) {
        const statusInfo2 = document.getElementById('status_info2');

        statusInfo2.textContent = translations.info[info]

        switch (info) {
            case 0:
                statusInfo2.style.color = color_green;
                break;
            case 1:
            case 2:
            case 3:
                statusInfo2.style.color = color_orange;
                break;
            case 4:
                statusInfo2.style.color = 'red';
                break;
            default:
                statusInfo2.style.color = 'black'; 
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
            updateStatusInfo2(data.info2);
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
                updateStatusInfo2(data.info2);
            },
            error: function(error) {
                console.error('Error fetching data:', error);
            }
        });
    }


    if (drink1Input && drink2Input && statusInput) {
        drink1Input.addEventListener('input', function() {
            validateInput(drink1Input);
        });

        drink2Input.addEventListener('input', function() {
            validateInput(drink2Input);
        });

        drink1Input.addEventListener('change', function() {
            console.log('Drink1 changed:', drink1Input.value);
            const formData = new FormData(document.getElementById('drinkForm'));
            sendData(formData);
        });

        drink2Input.addEventListener('change', function() {
            console.log('Drink2 changed:', drink2Input.value);
            const formData = new FormData(document.getElementById('drinkForm'));
            sendData(formData);
        });

        statusSwitch.addEventListener('change', function() {
            console.log('statusSwitch changed:', statusSwitch.checked);
            const formData = new FormData(document.getElementById('drinkForm'));
            formData.append('status', statusSwitch.checked);
            sendData(formData);
        });

        updateData();

    } else {
        console.error('One or more elements are missing in the DOM.');
    }

    setInterval(updateData, 2000);
});
