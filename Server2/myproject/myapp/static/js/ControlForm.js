document.addEventListener('DOMContentLoaded', function() {
    const confirmDialog = document.getElementById('confirmDialog');
    const confirmMessage = document.getElementById('confirmMessage');
    const confirmButton = document.getElementById('confirmButton');
    const cancelButton = document.getElementById('cancelButton');

    function showConfirmDialog(message, action) {
        confirmMessage.textContent = message;
        confirmDialog.style.display = 'block';

        confirmButton.onclick = function() {
            confirmDialog.style.display = 'none';
            action();
        };

        cancelButton.onclick = function() {
            confirmDialog.style.display = 'none';
        };
    }

    document.getElementById('calibrationButton').addEventListener('click', function() {
        const url = this.getAttribute('data-url');
        showConfirmDialog(translations.calibrationMessage, function() {
            // Send request to server to set calibration to True
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ calibration: true })
            });
        });
    });

    document.getElementById('panelButton').addEventListener('click', function() {
        const url = this.getAttribute('data-url');
        showConfirmDialog(translations.panelMessage, function() {
            // Send request to server to set panel to True
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ panel: true })
            });
        });
    });

    document.getElementById('motorButton').addEventListener('click', function() {
        const url = this.getAttribute('data-url');
        showConfirmDialog(translations.motorMessage, function() {
            // Send request to server to set motor to True
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ motor: true })
            });
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
