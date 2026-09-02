#include <iostream>
#include <fstream>
#include <string>

using namespace std;


// ============================================================
// FREQUENCY ANALYSIS
// ============================================================
void frequency_analysis(string ciphertext)
{
    int frequency[26] = {0};
    int totalLetters = 0;

    // Count each letter
    for (char ch : ciphertext)
    {
        if (ch >= 'A' && ch <= 'Z')
        {
            frequency[ch - 'A']++;
            totalLetters++;
        }
    }

    cout << "\n========== FREQUENCY ANALYSIS ==========\n";

    cout << "Letter\tFrequency\tPercentage\n";

    // Display frequency and percentage
    for (int i = 0; i < 26; i++)
    {
        double percentage = 0;

        if (totalLetters > 0)
        {
            percentage =
                (double)frequency[i] / totalLetters * 100;
        }

        cout << char('A' + i)
             << "\t"
             << frequency[i]
             << "\t\t"
             << percentage
             << "%\n";
    }


    // ========================================================
    // Sort letters according to frequency
    // ========================================================

    int sortedFrequency[26];
    char sortedLetters[26];

    for (int i = 0; i < 26; i++)
    {
        sortedFrequency[i] = frequency[i];
        sortedLetters[i] = char('A' + i);
    }

    // Simple selection sort
    for (int i = 0; i < 26; i++)
    {
        int maxIndex = i;

        for (int j = i + 1; j < 26; j++)
        {
            if (sortedFrequency[j] >
                sortedFrequency[maxIndex])
            {
                maxIndex = j;
            }
        }

        // Swap frequency
        int tempFrequency = sortedFrequency[i];
        sortedFrequency[i] = sortedFrequency[maxIndex];
        sortedFrequency[maxIndex] = tempFrequency;

        // Swap letters
        char tempLetter = sortedLetters[i];
        sortedLetters[i] = sortedLetters[maxIndex];
        sortedLetters[maxIndex] = tempLetter;
    }


    // ========================================================
    // Display descending frequency
    // ========================================================

    cout << "\n========== DESCENDING FREQUENCY ==========\n";

    cout << "Rank\tLetter\tFrequency\tPercentage\n";

    for (int i = 0; i < 26; i++)
    {
        double percentage = 0;

        if (totalLetters > 0)
        {
            percentage =
                (double)sortedFrequency[i] /
                totalLetters * 100;
        }

        cout << i + 1
             << "\t"
             << sortedLetters[i]
             << "\t"
             << sortedFrequency[i]
             << "\t\t"
             << percentage
             << "%\n";
    }


    // ========================================================
    // Most frequent letter
    // ========================================================

    cout << "\n========== MOST FREQUENT LETTER ==========\n";

    cout << sortedLetters[0]
         << " occurs "
         << sortedFrequency[0]
         << " times.\n";
}


// ============================================================
// WORD FREQUENCY ANALYSIS
// ============================================================
void word_frequency_analysis(string ciphertext)
{
    string words[1000];
    int wordCount[1000] = {0};
    int totalWords = 0;

    string currentWord = "";

    // Extract words from ciphertext
    for (int i = 0; i <= ciphertext.length(); i++)
    {
        char ch;

        if (i < ciphertext.length())
            ch = ciphertext[i];
        else
            ch = ' ';

        // If character is a letter
        if (ch >= 'A' && ch <= 'Z')
        {
            currentWord += ch;
        }
        else
        {
            // Word has ended
            if (currentWord != "")
            {
                bool found = false;

                // Check whether word already exists
                for (int j = 0; j < totalWords; j++)
                {
                    if (words[j] == currentWord)
                    {
                        wordCount[j]++;
                        found = true;
                        break;
                    }
                }

                // If it is a new word
                if (!found)
                {
                    words[totalWords] = currentWord;
                    wordCount[totalWords] = 1;
                    totalWords++;
                }

                // Clear current word
                currentWord = "";
            }
        }
    }


    // ========================================================
    // Display one-letter words
    // ========================================================

    cout << "\n========== ONE-LETTER WORDS ==========\n";

    for (int i = 0; i < totalWords; i++)
    {
        if (words[i].length() == 1)
        {
            cout << words[i]
                 << " : "
                 << wordCount[i]
                 << " times\n";
        }
    }


    // ========================================================
    // Display two-letter words
    // ========================================================

    cout << "\n========== TWO-LETTER WORDS ==========\n";

    for (int i = 0; i < totalWords; i++)
    {
        if (words[i].length() == 2)
        {
            cout << words[i]
                 << " : "
                 << wordCount[i]
                 << " times\n";
        }
    }


    // ========================================================
    // Display three-letter words
    // ========================================================

    cout << "\n========== THREE-LETTER WORDS ==========\n";

    for (int i = 0; i < totalWords; i++)
    {
        if (words[i].length() == 3)
        {
            cout << words[i]
                 << " : "
                 << wordCount[i]
                 << " times\n";
        }
    }


    // ========================================================
    // Display repeated words
    // ========================================================

    cout << "\n========== REPEATED WORDS ==========\n";

    for (int i = 0; i < totalWords; i++)
    {
        if (wordCount[i] > 1)
        {
            cout << words[i]
                 << " : "
                 << wordCount[i]
                 << " times\n";
        }
    }
}

// ============================================================
// PATTERN ANALYSIS
// ============================================================
void pattern_analysis(string ciphertext)
{
    string words[1000];
    int totalWords = 0;

    string currentWord = "";

    // --------------------------------------------------------
    // Extract all words from ciphertext
    // --------------------------------------------------------
    for (int i = 0; i <= ciphertext.length(); i++)
    {
        char ch;

        if (i < ciphertext.length())
            ch = ciphertext[i];
        else
            ch = ' ';

        if (ch >= 'A' && ch <= 'Z')
        {
            currentWord += ch;
        }
        else
        {
            if (currentWord != "")
            {
                words[totalWords] = currentWord;
                totalWords++;

                currentWord = "";
            }
        }
    }


    // --------------------------------------------------------
    // Display pattern of each word
    // --------------------------------------------------------
    cout << "\n========== PATTERN ANALYSIS ==========\n";

    cout << "Word\t\tPattern\n";


    for (int i = 0; i < totalWords; i++)
    {
        string word = words[i];

        // Array to store pattern number for each letter
        int pattern[100];

        int nextNumber = 1;


        // Initially mark all positions as 0
        for (int j = 0; j < word.length(); j++)
        {
            pattern[j] = 0;
        }


        // ----------------------------------------------------
        // Generate pattern
        // ----------------------------------------------------
        for (int j = 0; j < word.length(); j++)
        {
            // If this letter already appeared
            bool found = false;

            for (int k = 0; k < j; k++)
            {
                if (word[k] == word[j])
                {
                    pattern[j] = pattern[k];
                    found = true;
                    break;
                }
            }

            // If this is a new letter
            if (!found)
            {
                pattern[j] = nextNumber;
                nextNumber++;
            }
        }


        // ----------------------------------------------------
        // Display word and pattern
        // ----------------------------------------------------
        cout << word << "\t\t";

        for (int j = 0; j < word.length(); j++)
        {
            cout << pattern[j];

            if (j < word.length() - 1)
                cout << "-";
        }

        cout << endl;
    }
}


// ============================================================
// APPLY SUBSTITUTION
// ============================================================
string apply_substitution(string ciphertext, string key)
{
    string plaintext = "";

    for (char ch : ciphertext)
    {
        if (ch >= 'A' && ch <= 'Z')
        {
            int position = ch - 'A';

            if (key[position] != '?')
            {
                plaintext += key[position];
            }
            else
            {
                plaintext += '_';
            }
        }
        else
        {
            // Keep spaces and punctuation unchanged
            plaintext += ch;
        }
    }

    return plaintext;
}


// ============================================================
// DISPLAY PARTIAL PLAINTEXT
// ============================================================
void display_partial_plaintext(string plaintext)
{
    cout << "\n========== PARTIAL PLAINTEXT ==========\n";
    cout << plaintext << endl;
}






// ============================================================
// MAIN FUNCTION
// ============================================================
int main()
{
    // ========================================================
    // Open the plaintext file
    // ========================================================

    ifstream file("monoalphabetic/data/plaintext.txt");

    if (!file)
    {
        cout << "Error: Could not open plaintext.txt"
             << endl;

        return 1;
    }


    // ========================================================
    // Read the complete plaintext
    // ========================================================

    string plaintext;
    string line;

    while (getline(file, line))
    {
        plaintext += line;
        plaintext += "\n";
    }

    file.close();


    // ========================================================
    // Monoalphabetic substitution key
    // ========================================================

    string normalAlphabet =
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    string cipherAlphabet =
        "QWERTYUIOPASDFGHJKLZXCVBNM";


    // ========================================================
    // Generate ciphertext
    // ========================================================

    string ciphertext = "";

    for (char ch : plaintext)
    {
        // Convert lowercase to uppercase
        if (ch >= 'a' && ch <= 'z')
        {
            ch = ch - 'a' + 'A';
        }

        // Substitute alphabetic characters
        if (ch >= 'A' && ch <= 'Z')
        {
            int position = ch - 'A';

            ciphertext +=
                cipherAlphabet[position];
        }
        else
        {
            // Keep spaces and punctuation unchanged
            ciphertext += ch;
        }
    }


    // ========================================================
    // Display plaintext
    // ========================================================

    cout << "========== PLAINTEXT =========="
         << endl;

    cout << plaintext << endl;


    // ========================================================
    // Display substitution key
    // ========================================================

    cout << "========== SUBSTITUTION KEY =========="
         << endl;

    cout << "Normal :  "
         << normalAlphabet
         << endl;

    cout << "Cipher :  "
         << cipherAlphabet
         << endl;


    // ========================================================
    // Display ciphertext
    // ========================================================

    cout << "========== CIPHERTEXT =========="
         << endl;

    cout << ciphertext << endl;


    // ========================================================
    // STEP 1: FREQUENCY ANALYSIS
    // ========================================================

    frequency_analysis(ciphertext);


    // ========================================================
    // STEP 2: WORD FREQUENCY ANALYSIS
    // ========================================================

    word_frequency_analysis(ciphertext);

pattern_analysis(ciphertext);
// Create an unknown substitution key
string key(26, '?');

// Test a possible substitution
// ZIT appears many times and has pattern 1-2-3
// Try: ZIT -> THE

key['Z' - 'A'] = 'T';
key['I' - 'A'] = 'H';
key['T' - 'A'] = 'E';

// Apply the guessed substitutions
string partialPlaintext = apply_substitution(ciphertext, key);

// Display the result
display_partial_plaintext(partialPlaintext);
    return 0;
}
