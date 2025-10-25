# Context-Aware Spell Checker using N-gram Language Model

A sophisticated spell checker application that uses N-gram language models to detect and correct both non-word errors and context-aware real-word errors. Built with Python and PyQt5, it provides an interactive GUI with real-time spell checking and context-sensitive suggestions.

## Features

### Dual Error Detection
- **Non-word Error Detection**: Identifies misspelled words not present in the vocabulary (e.g., "teh" instead of "the")
- **Real-word Error Detection**: Detects contextually incorrect words using bigram language models (e.g., "I have to go their" should be "there")

### Visual Feedback
- Red underline for non-word errors
- Blue underline for context-based errors
- Right-click context menu for correction suggestions

### Advanced Algorithms
- **Minimum Edit Distance (MED)**: Generates spelling suggestions up to edit distance of 2
- **N-gram Language Models**: Uses unigram and bigram models for context-aware checking
- **Laplace Smoothing**: Handles zero-probability issues in language model calculations

## Installation

### Prerequisites
- Python 3.x
- PyQt5
- NumPy

### Setup
1. Clone the repository:
```bash
git clone <repository-url>
cd context-aware-spellchecker-using-N-gram-language-model
```

2. Install required dependencies:
```bash
pip install PyQt5 numpy
```

3. Prepare the corpus data:
   - Create a `data` directory in the project root
   - Move `corpus.txt` to the `data` directory, or add your own text files
```bash
mkdir data
mv corpus.txt data/
```

## Usage

Run the application:
```bash
python main.py
```

The application will open a text editor window where you can:
1. Type or paste text
2. Misspelled words will be underlined in red
3. Contextually incorrect words will be underlined in blue
4. Right-click on underlined words to see correction suggestions
5. Click a suggestion to replace the word

## Project Structure

```
.
├── main.py                  # Application entry point with PyQt5 GUI
├── spellcheckwrapper.py     # Wrapper class integrating all spell checking functionality
├── non_word_checking.py     # Non-word error detection and correction
├── real_word_checking.py    # Context-aware real-word error detection
├── spelltextedit.py         # Custom QTextEdit with spell checking support
├── highlighter.py           # Syntax highlighter for marking spelling errors
├── correction_action.py     # Custom QAction for correction menu items
└── corpus.txt               # Training corpus for language models
```

## How It Works

### 1. Tokenization
The system preprocesses text by:
- Converting to lowercase
- Removing punctuation and special characters
- Splitting into sentences with `<SOS>` (Start of Sentence) and `<EOS>` (End of Sentence) markers
- Creating token lists for model training

### 2. Language Model Training
- **Unigram Model**: Tracks individual word frequencies
- **Bigram Model**: Tracks word pair frequencies for context analysis
- Models are trained on the corpus during initialization

### 3. Non-word Error Detection
- Checks if a word exists in the vocabulary
- Generates suggestions using edit operations (insert, delete, replace, transpose)
- Ranks suggestions by Minimum Edit Distance

### 4. Real-word Error Detection
- Calculates bigram probability for word sequences
- Compares original word probability with similar word alternatives
- Suggests replacements if alternatives have higher probability in context

### 5. Laplace Smoothing
Applies add-one smoothing to handle unseen word pairs:
```
P(word2 | word1) = (count(word1, word2) + 1) / (count(word1) + V + 1)
```
where V is the vocabulary size.

## Algorithm Details

### Minimum Edit Distance (MED)
Supports four edit operations:
- **Deletion**: Remove a character
- **Insertion**: Add a character
- **Replacement**: Change a character
- **Transposition**: Swap adjacent characters

### Bigram Sentence Probability
Calculates sentence likelihood as:
```
P(sentence) = Σ log P(word_i | word_{i-1})
```

Higher probability indicates better grammatical context.

## Example

**Input**: "I have too books"

**Detection**:
- "too" is correctly spelled but contextually wrong
- Bigram model suggests "two" has higher probability after "have"
- Word is underlined in blue
- Right-click shows: "two (Real-word Error)"

## References

This project builds upon concepts from:
- [GrammaticalErrorDetection-Correction](https://github.com/AshwiniRangnekar/GrammaticalErrorDetection-Correction)
- [spelling-correction](https://github.com/troublemeeter/spelling-correction)
- [pyqt-spellcheck](https://github.com/NethumL/pyqt-spellcheck)
