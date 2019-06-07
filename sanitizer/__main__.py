from sanitizer.SanitizerTokenizer import SanitizerTokenizer
import click

"""
    Name: Sanitizer module
    Description: This module offer 3 options to sanitize a text and save the result into a file.
    Author: Matthias Christe
    Date: 07.06.2019

"""


@click.command()
@click.option('--verbose', is_flag=True, default=False, help="Only useful if you choose sanitize_numbers_limit_commonwords, it shows information about the reduction of the word dictionary")
@click.option('--n_most_common', default=10000, help='Number of most common words to keep')
@click.option('--sanitizemethod', default="sanitize_hard", help='Sanitize method: sanitize_hard, sanitize_numbers, sanitize_numbers_limit_commonwords')
@click.argument('input_file', nargs=1, type=click.File())
@click.argument('output_file', nargs=1)
def main(input_file, output_file, sanitizemethod, n_most_common, verbose):
    # sanitize the file
    sentences = [l.strip() for l in input_file]
    if sanitizemethod == "sanitize_hard":
        sentences_san = [SanitizerTokenizer.sanitize_hard(sen) for sen in sentences]
    elif sanitizemethod == "sanitize_numbers":
        sentences_san = [SanitizerTokenizer.sanitize_numbers(sen) for sen in sentences]
    elif sanitizemethod == "sanitize_numbers_limit_commonwords":
        sentences_san = SanitizerTokenizer.sanitize_numbers_limit_commonwords(sentences, n_mostcommon=n_most_common, verbose=verbose)

    # save sanitized sentences to file
    with open(output_file, 'w') as filehandle:
        for sentence in sentences_san:
            filehandle.write('%s\n' % sentence)

if __name__ == '__main__':
    main()
