import re
import random
# Import warnings and enable DeprecationWarning's for parse function
import warnings
warnings.simplefilter('always', DeprecationWarning)


def _replace_string(string):
    """
    Function that generates all the strings for the options in the first {}
    :param match object:
    :return string:
    """
    global spintax_seperator, spintax_bracket, random_string
   
    match = re.findall(spintax_bracket, string)
    if not len(match):
        return [string]
    match = match[0]
            
    test_string = re.sub(spintax_seperator, lambda x: x[1]+random_string, match[1])
    pattern = '{' + match[1].replace('\\','\\\\').replace('|','\|') + '}'
    options = re.split(random_string, test_string)
    res = [re.sub(pattern, option, string) for option in options]
    #res = [match[0] + option + match[2] for option in options]
    return res

def prep_custom_spintax(string, spintax_chars):
    characters = [chr(x) for x in range(1234, 1368)]    
    
    temp = ''.join(random.sample(characters, 30))
    if spintax_chars[0] != '{':
        string = string.replace('{', temp).replace(spintax_chars[0], '{').replace(temp, spintax_chars[0])
    if spintax_chars[1] != '|':
        string = string.replace('|', temp).replace(spintax_chars[1], '|').replace(temp, spintax_chars[1])
    if spintax_chars[2] != '}':
        string = string.replace('}', temp).replace(spintax_chars[2], '}').replace(temp, spintax_chars[2])
    return string

def undo_custom_spintax(string, spintax_chars):
    characters = [chr(x) for x in range(1234, 1368)]    
    temp = ''.join(random.sample(characters, 30))
    
    if spintax_chars[0] != '{':
        string = string.replace(spintax_chars[0], temp).replace('{', spintax_chars[0]).replace(temp, '{')
    if spintax_chars[1] != '|':
        string = string.replace(spintax_chars[1], temp).replace('|', spintax_chars[1]).replace(temp, '|')
    if spintax_chars[2] != '}':
        string = string.replace(spintax_chars[2], temp).replace('}', spintax_chars[2]).replace(temp, '}')
    return string

def spin(string, seed=None, generate_all:bool = False, spintax_chars:tuple = ('{','|','}')):
    """
    Function used to spin the spintax string
    :param string:
    :param seed:
    :return string:
    """
    string = prep_custom_spintax(string, spintax_chars)

    # As look behinds have to be a fixed width I need to do a "hack" where
    # a temporary string is used. This string is randomly chosen. There are
    # 1.9e62 possibilities for the random string and it uses uncommon Unicode
    # characters, that is more possibilerties than number of Planck times that
    # have passed in the universe so it is safe to do.
    characters = [chr(x) for x in range(1234, 1368)]    
    global random_string
    random_string = ''.join(random.sample(characters, 30))
    
    # If the user has chosen a seed for the random numbers use it
    if seed is not None:
        random.seed(seed)

    # Regex to find spintax seperator, defined here so it is not re-defined
    # on every call to _replace_string function
    global spintax_seperator
    spintax_seperator = r'((?:(?<!\\)(?:\\\\)*))(\|)'
    spintax_seperator = re.compile(spintax_seperator)

    global spintax_bracket
    # Regex to find all non escaped spintax brackets
    spintax_bracket = r'(?<!\\)((?:\\{2})*)\{([^}{}]+)(?<!\\)((?:\\{2})*)\}'
    spintax_bracket = re.compile(spintax_bracket)

    # Need to iteratively apply the spinning because of nested spintax
    if generate_all:
        strings = [string]
        
        while True:
            new_strings = [s for s in _replace_string(string) for string in strings]
            
            if not set(strings).symmetric_difference(set(new_strings)):
                break
            strings = new_strings
        return [undo_custom_spintax(s, spintax_chars) for s in strings]
    else:
        while True:
            res = _replace_string(string)         
            new_string = random.choice(res)
            if new_string == string:
                break
            string = new_string

        # Replaces the literal |, {,and }.
        string = re.sub(r'\\([{}|])', r'\1', string)
        # Removes double \'s
        string = re.sub(r'\\{2}', r'\\', string)

        return undo_custom_spintax(string, spintax_chars)


def parse(string, seed=None):
    """
    Old function used will be removed use spin() instead
    :param string:
    :param seed:
    :return list:
    """
    warnings.warn(
        "This function (parse) is being depreciated, please use spin(string)",
        DeprecationWarning
    )
    return [spin(string, seed)]
