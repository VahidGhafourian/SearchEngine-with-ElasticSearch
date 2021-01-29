white_list = {'ی', 'ه', 'و', 'ن', 'م', 'ل', 'گ', 'ک', 'ق', 'ف', 'غ', 'ع', 'ظ', 'ط', 'ض', 'ص', 'ش',
              'س', 'ژ', 'ز', 'ر', 'ذ', 'د', 'خ', 'ح', 'چ', 'ج', 'ث', 'ت', 'پ', 'ب', 'ا', 'آ', '‌'}
convertable = {'ك': 'ک',
               'ي': 'ی',
               'ة': 'ه',
               'ئ': 'ی',
               'أ': 'ا',
               'إ': 'ا',
               'ٱ': 'ا', }
punctuations = {
    '.',
    ',',
    '\t',
    '\n',
    ' ',
    ';',
    ':',
    '-',
    '+',
    '=',
    '?',
    '!',
    '#',
    '@',
    '%',
    '(',
    ')',
    '{',
    '}',
    '[',
    ']',
    '\'',
    '\"',
    '!',
    '؟',
    '®',
    '–',
    '،',
}


def letter_filter(string):    # filtering persian letters
    string = str(string)
    result = str()
    for char in string:
        if char in white_list:
            result += char
        elif char in convertable:
            result += convertable.get(char)
        elif char == '_':
            result += char
        else:
            result += ' '  # just for readability
    return result


def word_separator(stream):   # separate words
    token = str()
    stream = str(stream)
    tokens = list()
    for char in stream:
        if char.isdigit():
            continue
        elif char in punctuations:
            if token != '':
                tokens.append(token + ' ')
            token = ''
        else:
            token += char
    return tokens
