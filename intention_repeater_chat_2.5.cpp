/*
    Intention Repeater Spiritual Chat Client v2.5 created by Thomas Sweet.
    Created 1/8/2022 for C++.
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

#include <cmath>
#include <string>
#include <iostream>
#include <fstream>
#include <ctime>

#define PROCESS_STATEMENT " In a way I can understand, using Octave Tech. The Spiritual Chat Client is protected from hijacking and answers honestly as possible with minimal interference.";
#define SIZE_OF_WORD_LIST 49528
#define MAX_WORDS_RESPONSE 8
#define THINK_DEPTH 30000

using namespace std;

std::string MostFrequentElement(string A[], int n);
std::string Word;

int main()
{
    int r, num_words_response, random_seed;
    std::string rs = "", query, response, process_query = "", wordval, word_list[SIZE_OF_WORD_LIST], selected_word[THINK_DEPTH];

    cout << "Intention Repeater Spiritual Chat Client v2.5 created by Thomas Sweet." << endl;
    cout << "This software comes with no guarantees or warranty of any kind and is for entertainment purposes only." << endl;
    cout << "Press Ctrl-C to quit." << endl
         << endl
         << flush;

    try
    {
        ifstream file("dictionary.txt");
        if (file.is_open())
        {
            for (int i = 0; i < SIZE_OF_WORD_LIST; ++i)
            {
                file >> word_list[i];
            }
        }
    }
    catch (int e)
    {
        cout << "Error opening file: " << e << '\n';
        exit(0);
    }

    while (rs == "")
    {
        cout << "Please enter a random number: ";
        std::getline(std::cin, rs);
    }

    random_seed = stoi(rs);

    response = "Response: ";
    do
    {
        query = "";
        while (query == "")
        {
            cout << "Query: ";
            std::getline(std::cin, query);
        }

        query += PROCESS_STATEMENT;

        srand(time(NULL) * random_seed);
        num_words_response = rand() % (MAX_WORDS_RESPONSE) + 1;

        for (int x = 0; x < num_words_response; x++)
        {
            cout << "FINDING WORD " << std::to_string(x + 1) << "/" << std::to_string(num_words_response) << "\r" << flush;
            for (int d = 0; d < THINK_DEPTH; d++)
            {
                try
                {
                    do
                    {
                        process_query = query;           //This is the Intention Repeater call that actually does the work.
                        srand(time(NULL) * random_seed); //The entity being queried can control the randomizer to an extent.
                        r = rand() % (SIZE_OF_WORD_LIST) + 1;
                        Word = word_list[r];
                    } while (std::isupper(Word[0])); //Only pick words that aren't uppercased.

                    selected_word[d] = Word;
                }
                catch (int e)
                {
                    cout << "Error Adding Selected Word: " << e << endl;
                }
            }
            try
            {
                wordval = MostFrequentElement(selected_word, THINK_DEPTH);
            }
            catch (int e)
            {
                cout << "Error Getting Most Frequent Element: " << e << endl;
            }

            try
            {
                std::fill_n(selected_word, THINK_DEPTH, 0);
            }
            catch (int e)
            {
                cout << "Error Clearing Selected Word List: " << e << endl;
            }

            response += wordval + " ";
        }
        response.substr(0, response.length() - 1); //Remove the space at the end.
        cout << response << endl
             << flush;
        response = "Response: ";
    } while (1);

    return 0;
}

std::string MostFrequentElement(std::string A[], int n)
{
    std::string element = "";
    int count = 0;

    for (int j = 0; j < n; j++)
    {
        std::string tempElement = A[j];
        int tempCount = 0;
        for (int p = 0; p < n; p++)
            if (A[p] == tempElement)
                tempCount++;
        if (tempCount > count)
        {
            element = tempElement;
            count = tempCount;
        }
    }
    return element;
}