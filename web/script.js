document.addEventListener('DOMContentLoaded', function () {
    const settingsButton = document.getElementById('settings-button');
    const settingsPanel = document.getElementById('settings-panel');
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatWindow = document.getElementById('chat-window');

    // Ensure apiKeySet is a Boolean
    apiKeySet = !!apiKeySet;

    // Toggle settings panel
    settingsButton.addEventListener('click', function () {
        if (settingsPanel.style.display === 'none') {
            settingsPanel.style.display = 'block';
        } else {
            settingsPanel.style.display = 'none';
        }
    });

    // Save API Key
    const apiKeyForm = document.getElementById('api-key-form');
    apiKeyForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const apiKey = document.getElementById('api-key').value.trim();

        fetch('process.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'action=save_api_key&api_key=' + encodeURIComponent(apiKey)
        })
        .then(response => response.json())
        .then(data => {
            // Update apiKeySet based on whether the API key is empty
            if (apiKey !== '') {
                apiKeySet = true;
                showPopupMessage('API Key Set');
            } else {
                apiKeySet = false;
                showPopupMessage('API Key Cleared');
            }
        })
        .catch(error => {
            console.error('Error saving API Key:', error);
        });
    });

    // Save Model
    const modelForm = document.getElementById('model-form');
    modelForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const model = document.getElementById('model').value;

        showPopupMessage(model + ' Model Selected');

        fetch('process.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'action=save_model&model=' + encodeURIComponent(model)
        });
    });

    // Save Mood
    const moodForm = document.getElementById('mood-form');
    moodForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const mood = document.getElementById('mood').value;

        showPopupMessage(mood + ' Mood Selected');

        fetch('process.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'action=save_mood&mood=' + encodeURIComponent(mood)
        });
    });

    // Toggle Logging
    const loggingForm = document.getElementById('logging-form');
    loggingForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const logging = document.getElementById('logging').checked;

        showPopupMessage('Logging Enabled');

        fetch('process.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'action=toggle_logging&logging=' + logging
        });
    });

    // Download Log
    const downloadLogButton = document.getElementById('download-log');
    downloadLogButton.addEventListener('click', function () {
        window.location.href = 'process.php?action=download_log';
    });

    // Clear Log
    const clearLogButton = document.getElementById('clear-log');
    clearLogButton.addEventListener('click', function () {
        fetch('process.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'action=clear_log'
        }).then(() => {
            showPopupMessage('Log Cleared');
        });
    });

    // Send Chat Message
    chatForm.addEventListener('submit', function (e) {
        e.preventDefault();

        // Ensure apiKeySet is a Boolean
        apiKeySet = !!apiKeySet;

        // Check if API Key is set
        if (!apiKeySet) {
            alert('Please enter your OpenRouter API Key in the settings before sending messages.');
            return; // Do not proceed further
        }

        const message = userInput.value.trim();
        if (message === '') return;

        // Display user's message
        displayMessage('User: ' + message, 'user');
        userInput.value = '';

        // Generate a unique ID for the thinking message
        const thinkingMessageId = 'thinking-message-' + Date.now();

        // Display the animated "Thinking..." message
        displayThinkingMessage(thinkingMessageId);

        // Send message to server
        fetch('process.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'action=send_message&message=' + encodeURIComponent(message)
        })
            .then(response => response.json())
            .then(data => {
                // Stop the thinking animation
                const thinkingMessageElement = document.getElementById(thinkingMessageId);
                clearInterval(thinkingMessageElement.animationInterval);

                // Replace the "Thinking..." message with the actual response
                if (data.status === 'success') {
                    thinkingMessageElement.innerHTML = 'Bot: ' + data.response.replace(/\n/g, '<br>');

                    // Display the meaning as a new message
                    displayMessage('Meaning: ' + data.meaning, 'meaning');
                } else {
                    thinkingMessageElement.innerHTML = 'Error: ' + data.message;
                }
                chatWindow.scrollTop = chatWindow.scrollHeight;
            });
    });

    function displayMessage(message, type, messageId = null) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', type);

        // Assign a unique ID if provided
        if (messageId) {
            messageElement.id = messageId;
        }

        // Escape HTML special characters to prevent XSS attacks
        const escapedMessage = message
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;");

        // Replace newline characters with <br> tags for HTML rendering
        const htmlMessage = escapedMessage.replace(/\n/g, "<br>");

        // Set the innerHTML to display line breaks properly
        messageElement.innerHTML = htmlMessage;

        chatWindow.appendChild(messageElement);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    function displayThinkingMessage(messageId) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', 'bot');
        messageElement.id = messageId;

        // Create the animated dots
        messageElement.innerHTML = 'Bot: Thinking<span id="' + messageId + '-dots">.</span>';

        chatWindow.appendChild(messageElement);
        chatWindow.scrollTop = chatWindow.scrollHeight;

        // Animate the dots
        let dotCount = 1;
        const maxDots = 3;
        const dotsElement = document.getElementById(messageId + '-dots');

        messageElement.animationInterval = setInterval(() => {
            dotCount = (dotCount % maxDots) + 1;
            dotsElement.textContent = '.'.repeat(dotCount);
        }, 500);
    }

    function showPopupMessage(message) {
        const popup = document.createElement('div');
        popup.className = 'popup-message';
        popup.textContent = message;
        document.body.appendChild(popup);
    
        // Show popup with fade-in
        setTimeout(() => popup.style.opacity = '1', 10);
    
        // Remove popup after 4 seconds (1 second fade-in, 2 seconds display, 1 second fade-out)
        setTimeout(() => {
            popup.style.opacity = '0';
            setTimeout(() => popup.remove(), 1000);
        }, 3000);
    }
});
