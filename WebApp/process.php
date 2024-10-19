<?php
session_start();

// Constants
define('THINK_DEPTH', 88888);
define('MAX_WORDS', 8);

// Load wordlist
$wordlist = file('wordlist.txt', FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);

// Initialize log if not set
if (!isset($_SESSION['log'])) {
    $_SESSION['log'] = [];
}

// Check for action
$action = null;
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $action = $_POST['action'];
} elseif ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $action = $_GET['action'];
}

// Handle download_log action via GET request
if ($action === 'download_log') {
    // Provide log file for download
    header('Content-Type: text/plain');
    header('Content-Disposition: attachment; filename="chat_log.txt"');
    echo implode("\n", $_SESSION['log']);
    exit;
}

// Handle other actions
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Ensure action is set
    if (!$action) {
        echo json_encode(['status' => 'error', 'message' => 'No action specified.']);
        exit;
    }

    // Handle different actions
    if ($action === 'save_api_key') {
        // Save API key in session
        $api_key = trim($_POST['api_key']);
        if (!empty($api_key)) {
            $_SESSION['api_key'] = $api_key;
        } else {
            // If the API key is empty, remove it from the session
            unset($_SESSION['api_key']);
        }
        echo json_encode(['status' => 'success']);
    } elseif ($action === 'save_model') {
        // Save selected model in session
        $_SESSION['model'] = $_POST['model'];
        echo json_encode(['status' => 'success']);
    } elseif ($action === 'save_mood') {
        // Save selected mood in session
        $_SESSION['mood'] = $_POST['mood'];
        echo json_encode(['status' => 'success']);
    } elseif ($action === 'toggle_logging') {
        // Toggle logging
        $_SESSION['logging'] = isset($_POST['logging']) && $_POST['logging'] === 'true';
        echo json_encode(['status' => 'success']);
    } elseif ($action === 'clear_log') {
        // Clear log
        $_SESSION['log'] = [];
        echo json_encode(['status' => 'success']);
    } elseif ($action === 'send_message') {
        $query = trim($_POST['message']);

        if (empty($query)) {
            echo json_encode(['status' => 'error', 'message' => 'Empty query.']);
            exit;
        }

        if (!isset($_SESSION['api_key']) || empty($_SESSION['api_key'])) {
            echo json_encode(['status' => 'error', 'message' => 'API Key not set.']);
            exit;
        }

        // Add user message to log
        if (isset($_SESSION['logging']) && $_SESSION['logging']) {
            $_SESSION['log'][] = "User: $query";
        }

        // Generate bot response
        $response = generate_response($query, $wordlist);

        // Get meaning from OpenRouter API
        $model = $_SESSION['model'] ?? 'openai/chatgpt-4o-latest';
        $mood = $_SESSION['mood'] ?? 'fun'; // Default to 'fun' if mood not set
        $meaning = get_meaning($query, $response, $_SESSION['api_key'], $model, $mood);

        // Add bot response and meaning to log
        if (isset($_SESSION['logging']) && $_SESSION['logging']) {
            $_SESSION['log'][] = "Bot: $response";
            $_SESSION['log'][] = "Meaning: $meaning";
            $_SESSION['log'][] = ""; // Add empty line for readability
        }

        echo json_encode([
            'status' => 'success',
            'response' => $response,
            'meaning' => $meaning
        ]);
    } else {
        echo json_encode(['status' => 'error', 'message' => 'Invalid action.']);
    }
}

function generate_response($query, $wordlist) {
    // Define the file path
    $filename = 'numqueries.txt';

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

    $response = "";

    // Step 4: Compute initial hash_value
    $epoch_time = (string) time();
    $hash_input = $query . ":" . $epoch_time;
    $hash_value = hash('sha3-512', $hash_input);

    // Step 5: Convert hash_value to number from 1-8
    $hash_int = intval(hexdec(substr($hash_value, 0, 8)));
    $num_words = ($hash_int % MAX_WORDS) + 1;  // 1 to 8

    // Step 9: Repeat steps 4-8 num_words times
    for ($i = 0; $i < $num_words; $i++) {
        // Step 6: Repeat hash computation THINK_DEPTH times
        for ($j = 0; $j < THINK_DEPTH; $j++) {
            $epoch_time = (string) time();
            $hash_input = $query . ":" . $hash_value . ":" . $epoch_time;
            $hash_value = hash('sha3-512', $hash_input);
        }

        // Step 7: Convert hash_value to selected_word_index
        $hash_int = intval(hexdec(substr($hash_value, 0, 8)));
        $selected_word_index = $hash_int % count($wordlist);

        // Step 8: Append word to response
        $response .= $wordlist[$selected_word_index] . " ";
    }

    return trim($response);
}

function get_meaning($query, $response, $api_key, $model, $mood) {
    // Adjust system prompt based on mood
    $mood_prompts = [
        'neutral' => '',
        'fun' => 'Be fun.',
        'serious' => 'Be serious.',
        'thoughtful' => 'Be thoughtful.',
        'encouraging' => 'Be encouraging.',
        'mystical' => 'Be mystical.',
        'humorous' => 'Be humorous.',
        'inspirational' => 'Be inspirational.',
        'casual' => 'Be casual.',
        'formal' => 'Be formal.',
        'empathic' => 'Be empathic.',
        'introspective' => 'Be introspective.',
        'funny' => 'Be funny.',
        'whimsical' => 'Be whimsical'
    ];

    $mood_prompt = $mood_prompts[$mood] ?? ''; // Default to '' neutral if mood not found

    $system_prompt = "You're an expert at taking seemingly random word responses generated from a Spiritual Chat software, and a user query and forming a meaning. Do not mention the words are random. " . $mood_prompt;

    $user_prompt = "The user asked \'$query\' and got the response \'$response\'. Please give a very brief definition of each word and the meaning of each word and an overall meaning and how it relates to their query.";

    $post_fields = json_encode([
        "model" => $model,
        "messages" => [
            ["role" => "system", "content" => $system_prompt],
            ["role" => "user", "content" => $user_prompt]
        ]
    ]);

    $headers = [
        "Authorization: Bearer $api_key",
        "Content-Type: application/json",
        "HTTP-Referer: https://spiritualchat.intentionrepeater.com/",
        "X-Title: Spiritual Chat WebApp",
        "X-Description: Connect with spiritual entities, guides, and higher energies using AI interpretations."
    ];

    $ch = curl_init('https://openrouter.ai/api/v1/chat/completions');
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $post_fields);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    $result = curl_exec($ch);

    if ($result === false) {
        return "Error communicating with OpenRouter API: " . curl_error($ch);
    }

    curl_close($ch);

    $response_data = json_decode($result, true);

    if (isset($response_data['choices'][0]['message']['content'])) {
        return $response_data['choices'][0]['message']['content'];
    } else {
        return "Error in API response.";
    }
}
?>
