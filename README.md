# Sanitizer

This module **sanitizer** allow to parse a file of text and to sanitize with fixed rules. The goal is to process a text in different ways before using it in a data science project. Machine learning is one field that often need to sanitize the text.

## Set-up

Download the entire repository. And then install the module:
```bash
python setup.py install
```

After that, you will be available to use the module in command line:

```bash
sanitizer <path to your input file> <path to your output file>
```

Some options are avalaible:

Options:

*   **--sanitizemethod**: Which sanitization method to apply to the dataset. For the moment, 3 methods are available:
  * *sanitize_hard* (remove numbers and punctuation except dashes, unify whitespaces, lowercase)
  * *sanitize_numbers* (remove punctuation except dashes, replace numbers with **N**)
  * *sanitize_numbers_limit_commonwords* ( unify whitespaces, replace numbers with **N**, keep n most common words and replace other with **\<unk\>**)  
* **--n_most_common** INTEGER:  Only useful if you choose sanitize_numbers_limit_commonwords, specifiy the number of most common words to keep
* **--verbose**: Only useful if you choose sanitize_numbers_limit_commonwords, it shows information about the reduction of the word dictionary
*  **--help**: Help message

## Commands

Sample command with options:

```bash
sanitizer file.txt file-san.txt --sanitizemethod "sanitize_numbers_limit_commonwords" --verbose --n_most_common 20000
```

**Possible output**:

```
Coverage from most common words 2629558/2996546 (87.75%)
Dictionary size reduced from 236587 => 20000 (8.45%)
```
