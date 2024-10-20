<?php

// Define the file path
$filename = 'counter.txt';

// Check if the file exists
if (!file_exists($filename)) {
    // If the file does not exist, create it and initialize the count to 1
    $count = 1;
    file_put_contents($filename, $count);
} else {
    // Open the file in read/write mode
    $file = fopen($filename, 'c+');
    if (flock($file, LOCK_EX)) {
        // Lock the file for writing
        $count = (int) fread($file, filesize($filename));
        $count++;
        // Move the file pointer back to the beginning before writing
        ftruncate($file, 0);
        rewind($file);
        fwrite($file, $count);
        fflush($file);
        flock($file, LOCK_UN); // Release the lock
    }
    fclose($file);
}

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
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&display=swap" rel="stylesheet">
</head>
<body>
    <div id="chat-container">
        <h1>Spiritual Chat Web App</h1>
        <div id="settings">
            <button id="settings-button">Settings</button>
            <div id="settings-panel" style="display: none;">
                <form id="api-key-form" style="display: flex; align-items: center; gap: 10px;">
                    <label for="api-key">
                        OpenRouter API Key (<a href="https://openrouter.ai/" target="_blank" class="bright-cyan">Get API Key</a>):
                    </label>
                    <input type="password" id="api-key" name="api-key" required style="flex: 1; padding: 5px;">
                    <button type="submit" id="save-api-key">Save</button>
                </form>

                <form id="model-form" style="display: flex; align-items: center; gap: 10px;">
                    <label for="model">Select Model:</label>
                    <select id="model" name="model" style="padding: 5px; flex: 1;">
                        <option value="openai/chatgpt-4o-latest">openai/chatgpt-4o-latest - (~$0.005/query)</option>
                        <option value="anthropic/claude-3.5-sonnet:beta">anthropic/claude-3.5-sonnet:beta - (~$0.003/query)</option>
                        <option value="mistralai/mistral-large">mistralai/mistral-large - (~$0.0042/query) (#1 Uncensored)</option>
                        <option value="x-ai/grok-2">x-ai/grok-2 - (~$0.0028/query) (#2 Uncensored)</option>
                        <option value="nvidia/llama-3.1-nemotron-70b-instruct">nvidia/llama-3.1-nemotron-70b-instruct - (~$0.00023/query) (#3 Uncensored)</option>
                        <option value="cognitivecomputations/dolphin-mixtral-8x22b">cognitivecomputations/dolphin-mixtral-8x22b - (~$0.00054/query) (#4 Uncensored)</option>
                        <option value="cognitivecomputations/dolphin-mixtral-8x7b">cognitivecomputations/dolphin-mixtral-8x7b - (~$0.00022/query) (#5 Uncensored)</option>
                        <option value="openai/o1-preview">openai/o1-preview - (~$0.11/query)</option>
                        <option value="openai/o1-mini">openai/o1-mini - (~$0.014/query)</option>
                        <option value="openai/gpt-4o-mini">openai/gpt-4o-mini - (~$0.0002/query)</option>
                        <option value="mistralai/mixtral-8x22b-instruct">mistralai/mixtral-8x22b-instruct - (~$0.00063/query)</option>
                        <option value="mistralai/mixtral-8x7b-instruct">mistralai/mixtral-8x7b-instruct - (~$0.00028/query)</option>
                        <option value="meta-llama/llama-3.1-405b-instruct">meta-llama/llama-3.1-405b-instruct - (~$0.0009/query)</option>
                        <option value="meta-llama/llama-3.1-70b-instruct">meta-llama/llama-3.1-70b-instruct - (~$0.00035/query)</option>
                        <option value="mistralai/mistral-medium">mistralai/mistral-medium - (~$0.00022/query)</option>
                    </select>
                    <button type="submit" id="save-model">Save</button>
                </form>

                <!-- Add Answer Mood Form -->
                <form id="mood-form" style="display: flex; align-items: center; gap: 10px;">
                    <label for="mood">Answer Mood:</label>
                    <select id="mood" name="mood" style="padding: 5px; flex: 1;">
                        <option value="neutral">Neutral</option>
                        <option value="fun">Fun (May use some emojis)</option>
                        <option value="casual">Casual</option>
                        <option value="funny">Funny</option>
                        <option value="thoughtful">Thoughtful</option>
                        <option value="introspective">Introspective</option>
                        <option value="empathic">Empathic</option>
                        <option value="encouraging">Encouraging</option>
                        <option value="inspirational">Inspirational</option>
                        <option value="serious">Serious</option>
                        <option value="formal">Formal</option>
                        <option value="mystical">Mystical</option>
                        <option value="calming">Calming</option>
                        <option value="direct">Direct</option>
                        <option value="playful">Playful (May use some emojis)</option>
                        <option value="whimsical">Whimsical (May use some emojis)</option>
                    </select>
                    <button type="submit" id="save-mood">Save</button>
                </form>

                <form id="logging-form" style="display: flex; align-items: center; gap: 10px;">
                    <label for="logging">Enable Logging:</label>
                    <input type="checkbox" id="logging" name="logging" style="margin: 0;">
                    <button type="submit">Save</button>
                    <button id="download-log">Download Log</button>
                    <button id="clear-log">Clear Log</button>
                    <button id="save-settings-button">Save Settings as Cookie</button>
                    <a href="#" id="submitFeedbackButton" class="bright-cyan">Submit Feedback</a>
                </form>

                <table padding="5">
                    <tr>
                        <td style="text-align: center; vertical-align: middle;">
                            <div style="display: flex; align-items: center; font-size: 0.9em; color: #666; text-align: center; margin-top: 10px;">
                                <img src="cookie_icon.png" alt="Cookie icon" style="width: 24px; height: 24px; margin-right: 8px;" />
                                <span>This website uses cookies to save your settings. Click "Save Settings as Cookie" if you agree to store your preferences as a cookie.</span>
                                <br><img src="lock_icon.png" alt="Lock icon" style="width: 24px; height: 24px; margin-right: 8px;" />
                                <span>Our chat logging system uses temporary variables and does not store chat data as files on our server. Your chat sessions are handled securely during processing, but they are not saved or retained afterward. Additionally, your API key is never recorded or stored on our server, ensuring that both your chats and API key remain private and are not monitored by us.</span>
                            </div>
                        </td>
                    </tr>
                </table>
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
