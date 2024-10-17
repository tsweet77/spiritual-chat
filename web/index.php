<?php

// Define the file path
$file_path = 'counter.txt';

// Check if the file exists
if (file_exists($file_path)) {
    // Read the current counter value from the file
    $counter = (int) file_get_contents($file_path);
} else {
    // If the file does not exist, initialize the counter to 0
    $counter = 0;
}

// Increment the counter by one
$counter++;

// Write the updated counter value back to the file
file_put_contents($file_path, $counter);

session_start();

// Load wordlist
$wordlist = file('wordlist.txt', FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);

// Initialize session variables
if (!isset($_SESSION['log'])) {
    $_SESSION['log'] = [];
}

// Determine if the API key is set
$apiKeySet = isset($_SESSION['api_key']) && !empty($_SESSION['api_key']);
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Spiritual Chat Web App</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div id="chat-container">
        <h1>Spiritual Chat Web App</h1>
        <div id="settings">
            <button id="settings-button">Settings</button>
            <div id="settings-panel" style="display: none;">
                <form id="api-key-form">
                    <label for="api-key">OpenRouter API Key:</label>
                    <input type="password" id="api-key" name="api-key" required>
                    <button type="submit">Save</button>
                </form>
                <form id="model-form">
                    <label for="model">Select Model:</label>
                    <select id="model" name="model">
                        <option value="openai/chatgpt-4o-latest">openai/chatgpt-4o-latest</option>
                        <option value="openai/gpt-4o-mini">openai/gpt-4o-mini</option>
                        <option value="openai/o1-preview">openai/o1-preview</option>
                        <option value="openai/o1-mini">openai/o1-mini</option>
                        <option value="anthropic/claude-3.5-sonnet:beta">anthropic/claude-3.5-sonnet:beta</option>
                        <option value="x-ai/grok-2">x-ai/grok-2</option>
                        <option value="nvidia/llama-3.1-nemotron-70b-instruct">nvidia/llama-3.1-nemotron-70b-instruct</option>
                    </select>
                    <button type="submit">Save</button>
                </form>
                <!-- Add Answer Mood Form -->
                <form id="mood-form">
                    <label for="mood">Answer Mood:</label>
                    <select id="mood" name="mood">
                        <option value="fun">Fun (May use more emojis)</option>
                        <option value="serious">Serious</option>
                        <option value="thoughtful">Thoughtful</option>
                        <option value="encouraging">Encouraging</option>
                        <option value="mystical">Mystical</option>
                        <option value="humorous">Humorous</option>
                        <option value="inspirational">Inspirational</option>
                        <option value="casual">Casual</option>
                        <option value="formal">Formal</option>
                        <option value="empathic">Empathic</option>
                        <option value="introspective">Introspective</option>
                        <option value="funny">Funny</option>
                    </select>
                    <button type="submit">Save</button>
                </form>
                <form id="logging-form">
                    <label for="logging">Enable Logging:</label>
                    <input type="checkbox" id="logging" name="logging">
                    <button type="submit">Save</button>
                </form>
                <button id="download-log">Download Log</button>
                <button id="clear-log">Clear Log</button>
            </div>
        </div>
        <div id="chat-window">
            <!-- Chat messages will appear here -->
        </div>
        <form id="chat-form">
            <input type="text" id="user-input" placeholder="Type your message here..." autocomplete="off" required>
            <button type="submit">Send</button>
        </form>
    </div>
    <!-- Include the apiKeySet variable -->
    <script>
        var apiKeySet = <?php echo $apiKeySet ? 'true' : 'false'; ?>;
    </script>
    <script src="script.js"></script>
</body>
</html>
