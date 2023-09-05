import os
import re


def add_tilde(text):
    polish_letters = 'ąćęłńóśźżĄĆĘŁŃÓŚŹŻ'
    any_letter = '\w\d{'+polish_letters+'}\u0100-\uFFFF'

    # Define a regular expression pattern to match single letters or two-letter words
    pattern1 = r'(\s|\~|\()[{'+any_letter+'}]{1,2}\s'  # adding ~ behind 1 and 2 letter words, so they break correctly
    # Starts with ' ' <1-2 letters> ' '

    pattern2 = r'(['+any_letter+'][\s]['+any_letter+']{1})(?=\.|\))'  # adding ~ for ending letter "kat A." into kat~A."
    # TODO add units?

    def repl1(match):
        original = match.group(0)
        if '}' in original:
            return original

        return f'{original[:-1]}~'

    def repl2(match):
        original = match.group(0)
        return f'{original[0]}~{original[2:]}'

    text = re.sub(pattern1, repl1, text)
    text = re.sub(pattern2, repl2, text)
    return text


def process_tex_files_in_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".tex"):
            print(f'Working on file {filename}')
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()

            modified_content = add_tilde(content)
            # print(modified_content)

            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(modified_content)
        else:
            print(f'Skipping file {filename}')


if __name__ == '__main__':
    dir = os.path.abspath('./')
    print(f'Opening dir: {dir}')
    process_tex_files_in_directory(dir)
