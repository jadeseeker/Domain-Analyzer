#!/usr/bin/env python
import sqlite3

# Function Name: lexical_analysis
# Input: url
# Output: A list containing 28 elements (in order):
#     01. URL
#     02. Brand name presence (1/0)
#     03. URL length
#     04. Domain token count
#     05. Domain total length
#     06. Domain token average length
#     07. Domain token max length
#     08. Path token count
#     09. Path total length
#     10. Path token average length
#     11. Path token max length
#     12. Percentage of special characters in url
#     13. Percentage of digits in url
#     14. Percentage of all alphabets in url (26 elements)


def lexical_analysis(url):
    return_values = []
    return_values.append(url)
    temp = url.find('//')
    if temp != -1:
        url = url[temp+2:]


    url_length = len(url)		# URL length

    # Getting the domain and path tokens
    domain_tokens = get_domain_tokens(url)
    path_tokens = get_path_tokens(url)

    # Get token count, total length, average length and max length for domain and path
    domain_characteristics = token_characteristics(domain_tokens)
    path_characteristics = token_characteristics(path_tokens)

    # Get percentage of special characters, digits and all alphabets
    char_freq = character_frequencies(url, url_length - domain_characteristics[0] - path_characteristics[0] + 2)

    # Check if a popular brand name is present in the path
    brand_presence = check_brand_name(url)

    return_values.append(brand_presence)
    return_values.append(url_length)
    return_values.extend(domain_characteristics)
    return_values.extend(path_characteristics)
    return_values.extend(char_freq)
    return return_values

# Function name: get_domain_tokens
# Input: URL
# Output: List of domain tokens

def get_domain_tokens(url):
    temp = url.find('/')
    domain_length = temp
    if temp == -1:
        domain_length = len(url)

    temp2 = url[0:domain_length]
    domains = temp2.split('.')
    return domains

# Function name: get_path_tokens
# Input: URL
# Output: List of path tokens

def get_path_tokens(url):
    temp = url.find('/')
    path = url[temp+1:]

    path_tokens = path.split('/')
    return path_tokens

# Function name: token_characteristics
# Input: List of tokens (called separately for domain tokens and path tokens)
# Output: List containing token count, total length, average length and max length

def token_characteristics(tokens):
    token_chars = []
    token_count = len(tokens)	                # Domain token count

    total_length = 0
    avg_length = 0
    max_length = 0

    for token in tokens:
        length = len(token)
        total_length += length
        if max_length < length:
            max_length = length

    avg_length = total_length/token_count
    total_length = total_length + token_count - 1

    token_chars.append(token_count)
    token_chars.append(total_length)
    token_chars.append(avg_length)
    token_chars.append(max_length)
    return token_chars

# Function name: character_frequencies
# Input: String and length of string(excluding '.' and '/')
# Output: List containing percentage of special characters, digits and all alphabets in the string

def character_frequencies(input_str, total_length):
    char_freq = []
    char_freq.extend([0] * 26)
    digit_count = 0
    special_char_count = 0

    for char in input_str:
        ascii_value = ord(char)
        if(ascii_value >= 97 and ascii_value <= 122):       # To find occurrences of [a-z]
            char_freq[ascii_value - 97] += 1
        elif(ascii_value >= 65 and ascii_value <= 90):      # To find occurrences of [A-Z]
            char_freq[ascii_value - 65] += 1
        elif(ascii_value >= 48 and ascii_value <= 57):
            digit_count += 1
        elif(char in "!@#$%^&*()-_=+{}[]|\':;><,?"):        # To find occurrences of special characters
            special_char_count += 1

    char_freq.insert(0, digit_count)
    char_freq.insert(0,special_char_count)
    for i in range(0, len(char_freq)):
        char_freq[i] = char_freq[i] * 100 / total_length

    return char_freq

# Function name: check_brand_name
# Input: URL
# Output: 1 if a popular brand name in present in the path. 0 otherwise

def check_brand_name(url):
    index = url.find('/')
    path = url[index+1:]
    path = path.lower()
    brand_names = ['atmail','contactoffice','fastmail','gandi','gmail','gmx','hushmail','lycos','outlook','rackspace','rediff','yandex','zoho','shortmail','myway','zimbra','boardermail','flashmail','caramail','computermail','emailchoice','facebook','myspace','linkedin','twitter','bing','glassdoor','friendster','myyearbook','flixster','myheritage','orkut','blackplanet','skyrock','perfspot','zorpia','netlog','tuenti','nasza-klasa','studivz','renren','kaixin001','hyves','ibibo','sonico','wer-kennt-wen','cyworld','iwiw','pinterest','tumblr','instagram','flickr','dropbox','woocommerce','2checkout','ach-payments','wepay','dwolla','braintree','feefighters','amazon','rupay','stripe','webmoney','worldpay','westernunion','verifone','transferwise','jpmorgan','bankofamerica','citibank','pnc','bnymellon','suntrust','capitalone','usbank','statestreet','tdbank','icici','bnpparibas','comerica','mitsubishi','credit-agricole','ca-cib','barclays','abchina','japanpost','societegenerale','apple','wellsfargo','pkobp','resbank','paypal','paypl','pypal','barclay','sars','google','chase','aol','microsoft','allegro','pko','ebay','cartasi','lloyds','visa','mastercard','bbamericas','voda','vodafone','hutch','walmart','hmrc','rbc','rbs','americanexpress','american','express','standard','relacionamento','itunes','morgan','commbank','cielo','santander','deutsche','asb','nwolb','irs','hsbc','verizon','att','hotmail','yahoo','kroger','citi','nyandcompany','walgreens','bestbuy','abebooks','dillons','lacoste','exxon','radioshack','shell','abercrombie']
    for name in brand_names:
        if(name in path):
            return 1
    return 0





