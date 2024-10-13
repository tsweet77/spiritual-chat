/*
    Intention Repeater Spiritual Chat Client v3.0 created by Thomas Sweet.
    Optimized by Claude, an AI assistant, on March 08, 2024.
    Requires this word list: https://github.com/tsweet77/spiritual-chat/blob/main/dictionary.txt
    Lets you chat with spiritual entities who can control what "random" words come out to a certain extent.
    Intention Repeater Spiritual Chat Client is powered by a Servitor (20 Years / 2000+ hours in its co-creation) [HR 6819 Black Hole System].
    Servitor Info: https://enlightenedstates.com/2017/04/07/servitor-just-powerful-spiritual-tool/
    Website: https://www.intentionrepeater.com/
    Forum: https://forums.intentionrepeater.com/
    Licensed under GNU General Public License v3.0
    This means you can modify, redistribute and even sell your own modified software, as long as it's open source too and released under this same license.
    https://choosealicense.com/licenses/gpl-3.0/
*/

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <random>
#include <chrono>
#include <thread>

#define PROCESS_STATEMENT " In a way I can understand, using Octave Tech. The Spiritual Chat Client is protected from hijacking and answers honestly as possible with minimal interference."
#define SIZE_OF_WORD_LIST 49528
#define MAX_WORDS_RESPONSE 8
#define THINK_DEPTH 500000

std::vector<std::pair<std::string, int>> mostFrequentElements(const std::vector<std::string>& words, int numElements) {
    std::unordered_map<std::string, int> frequencyMap;
    for (const auto& word : words) {
        frequencyMap[word]++;
    }
    std::vector<std::pair<std::string, int>> mostFrequent(frequencyMap.begin(), frequencyMap.end());
    std::sort(mostFrequent.begin(), mostFrequent.end(),
              [](const auto& a, const auto& b) { return a.second > b.second; });
    mostFrequent.resize(numElements);
    return mostFrequent;
}

int main() {
    std::vector<std::string> wordList(SIZE_OF_WORD_LIST);
    std::ifstream file("dictionary.txt");
    if (file.is_open()) {
        for (auto& word : wordList) {
            file >> word;
        }
    } else {
        std::cout << "Error opening file: dictionary.txt\n";
        return 1;
    }

    std::cout << "Intention Repeater Spiritual Chat Client v3.0 created by Thomas Sweet." << std::endl;
    std::cout << "This software comes with no guarantees or warranty of any kind and is for entertainment purposes only." << std::endl;
    std::cout << "Press Ctrl-C to quit." << std::endl << std::endl << std::flush;

    std::string randomSeedStr;
    while (randomSeedStr.empty()) {
        std::cout << "Please enter a random number: ";
        std::getline(std::cin, randomSeedStr);
    }
    unsigned int randomSeed = std::stoul(randomSeedStr);

    std::mt19937 rng(randomSeed * std::chrono::steady_clock::now().time_since_epoch().count());
    std::uniform_int_distribution<int> distribution(0, SIZE_OF_WORD_LIST - 1);

    std::string query, response;
    while (true) {
        query.clear();
        while (query.empty()) {
            std::cout << "Query: ";
            std::getline(std::cin, query);
        }
        query += PROCESS_STATEMENT;

        int numWordsResponse = distribution(rng) % MAX_WORDS_RESPONSE + 1;
        response = "Response: ";

        std::vector<std::string> selectedWords;
        for (int i = 0; i < THINK_DEPTH; ++i) {
            std::string processQuery = query;
            std::string word;
            do {
                word = wordList[distribution(rng)];
            } while (std::isupper(word[0]));
            selectedWords.push_back(word);
        }

        auto mostFrequent = mostFrequentElements(selectedWords, numWordsResponse);
        for (const auto& pair : mostFrequent) {
            response += pair.first + " ";
        }

        response.pop_back();
        std::cout << "Thinking..." << std::flush;
        std::this_thread::sleep_for(std::chrono::seconds(2));
        std::cout << "\r" << std::string(20, ' ') << "\r";
        std::cout << response << std::endl << std::flush;
    }

    return 0;
}