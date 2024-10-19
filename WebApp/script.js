document.addEventListener('DOMContentLoaded', function () {
    const settingsButton = document.getElementById('settings-button');
    const settingsPanel = document.getElementById('settings-panel');
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatWindow = document.getElementById('chat-window');

    const email = 'healing' + '@' + 'intentionrepeater.com';

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

        // Determine the message based on the checkbox state
        const message = logging ? 'Logging Enabled' : 'Logging Disabled';
        showPopupMessage(message);

        // Send the state to process.php
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

    function setCookie(name, value, days) {
        const expires = new Date(Date.now() + days * 24 * 60 * 60 * 1000).toUTCString();
        document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/; SameSite=None; Secure`;
    }
    
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) {
            return decodeURIComponent(parts.pop().split(';').shift());
        }
        return null;
    }

    function saveSettings() {
        const model = document.getElementById('model').value; // Adjust based on your actual setting IDs
        const api_key = document.getElementById('api-key').value; // Adjust based on your actual setting IDs
        const mood = document.getElementById('mood').value; // Adjust based on your actual setting IDs
        const logging = document.getElementById('logging').checked; // Store as a boolean
        // Repeat for all relevant settings
        setCookie('spiritual_chat_model', model, 365);
        setCookie('spiritual_chat_api_key', api_key, 365);
        setCookie('spiritual_chat_mood', mood, 365);
        setCookie('spiritual_chat_logging', logging, 365);
        // Repeat for all relevant settings
    
        showPopupMessage('Settings Saved in Cookie!');
    }

    const saveSettingsButton = document.getElementById('save-settings-button');
    saveSettingsButton.addEventListener('click', function () {
        saveSettings();
    });

    function loadSettings() {
        const model = getCookie('spiritual_chat_model');
        const api_key = getCookie('spiritual_chat_api_key');
        const mood = getCookie('spiritual_chat_mood');
        const logging = getCookie('spiritual_chat_logging');

        // Repeat for all relevant settings
    
        if (model) document.getElementById('model').value = model;
        if (api_key) document.getElementById('api-key').value = api_key;
        if (mood) document.getElementById('mood').value = mood;
        // For the checkbox, convert the string to a boolean value
        if (logging) {
            document.getElementById('logging').checked = logging === 'true';
        }
        // Repeat for all relevant settings
    }

    document.addEventListener('DOMContentLoaded', loadSettings);

     // Obfuscate email to protect against scrapers
     document.getElementById('submitFeedbackButton').addEventListener('click', function() {
        const subject = encodeURIComponent('Spiritual Chat Feedback');
        const mailtoLink = `mailto:${email}?subject=${subject}`;
        window.location.href = mailtoLink;
    });
    
    window.onload = loadSettings; // Load settings when the page loads
    
});
