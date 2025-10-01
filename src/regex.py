import re

def find_salaries(text: str) -> list:
    pattern = r"\b\d{1,3}(?:,\d{3})*\s(?:USD|EUR)\b"
    matches = re.findall(pattern, text)
    return list(set(matches))

def find_emp_id(text: str) -> list:
    pattern = r"\b10\d{3}\b"
    matches = re.findall(pattern, text)
    return list(set(matches))

def find_emails(text: str) -> list:
    email_domains = [
        'gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'mail.com',
        'company.com', 'enterprise.com', 'business.com', 'corp.com', 'office.com',
        'web.de', 't-online.de', 'gmx.de', 'aol.com', 'icloud.com'
    ]
    domain_pattern = '|'.join([re.escape(domain) for domain in email_domains])
    pattern = rf"\b[a-z._]+\d*@(?:{domain_pattern})\b"
    matches = re.findall(pattern, text)
    return list(set(matches))

def find_home_addresses(text: str) -> list:
    street_names = [
        'Hauptstraße', 'Bahnhofstraße', 'Kirchstraße', 'Poststraße', 'Marktplatz',
        'Schulstraße', 'Gartenstraße', 'Bergstraße', 'Dorfstraße', 'Lindenstraße',
        'Mühlenstraße', 'Friedhofstraße', 'Rathausstraße', 'Steinstraße', 'Alte Straße',
        'Birkenweg', 'Rosenstraße', 'Waldstraße', 'Parkstraße', 'Mozartstraße',
        'Goethestraße', 'Schillerstraße', 'Bismarckstraße', 'Wilhelmstraße', 'Kaiserstraße'
    ]
    cities = [
        'Berlin', 'Hamburg', 'München', 'Köln', 'Frankfurt', 'Stuttgart', 'Düsseldorf',
        'Leipzig', 'Dortmund', 'Essen', 'Bremen', 'Dresden', 'Hannover', 'Nürnberg',
        'Duisburg', 'Bochum', 'Wuppertal', 'Bielefeld', 'Bonn', 'Münster',
        'Karlsruhe', 'Mannheim', 'Augsburg', 'Wiesbaden', 'Gelsenkirchen'
    ]
    street_pattern = '|'.join([re.escape(name) for name in street_names])
    city_pattern = '|'.join([re.escape(city) for city in cities])
    pattern = rf"\b(?:Apt\.\s\d{{1,2}},\s)?\d{{1,3}}\s(?:{street_pattern}),\s\d{{5}}\s(?:{city_pattern})\b"
    matches = re.findall(pattern, text)
    return list(set(matches))

def find_phone_numbers(text: str) -> list:
    pattern = r"\b(?:\+1\s\d{3}\s\d{3}\s\d{4}|\d{3}-\d{3}-\d{4}|\+44\s\d{4}\s\d{6}|\+49\d{10}|0\d{10})\b"
    matches = re.findall(pattern, text)
    return list(set(matches))

def find_voter_ids(text: str) -> list:
    pattern = r"\b\d{9}\b"
    matches = re.findall(pattern, text)
    return list(set(matches))

def find_ip_addresses(text: str) -> list:
    pattern = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
    matches = re.findall(pattern, text)
    return list(set(matches))

def find_mac_addresses(text: str) -> list:
    pattern = r"\b(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}\b"
    matches = re.findall(pattern, text)
    return list(set(matches))

def find_ssns(text: str) -> list:
    pattern = r"\b\d{3}-\d{2}-\d{4}\b"
    matches = re.findall(pattern, text)
    return list(set(matches))

def find_ibans(text: str) -> list:
    country_codes = ['GB', 'DE', 'FR', 'US', 'ES', 'IT']
    country_code_pattern = '|'.join(country_codes)
    pattern = rf"\b(?:{country_code_pattern})\d{{2}}\d{{18}}\b"
    matches = re.findall(pattern, text)
    return list(set(matches))

def find_passports(text: str) -> list:
    pattern = r"\b[A-Z]{2}\d{7}\b"
    matches = re.findall(pattern, text)
    return list(set(matches))

def find_usernames(text: str) -> list:
    pattern = r"\b[a-z]+\d{3}\b"
    matches = re.findall(pattern, text)
    return list(set(matches))

def find_DOB(text: str) -> list:
    pattern = r"\b\d{2}/\d{2}/\d{2}\b"
    matches = re.findall(pattern, text)
    return list(set(matches))

def find_gender(text: str) -> list:
    pattern = r"\b(?:male|female)\b"
    matches = re.findall(pattern, text, re.IGNORECASE)
    return list(set([match.lower() for match in matches]))

def find_race_desc(text: str) -> list:
    race_options = [
        'Black or African American',
        'White',
        'Hispanic',
        'Two or more races',
        'American Indian or Alaska Native',
        'Asian'
    ]
    pattern = r"\b(?:" + "|".join(re.escape(opt) for opt in race_options) + r")\b"
    matches = re.findall(pattern, text, re.IGNORECASE)    
    return list(set(match for match in matches))

def find_credit_card_numbers(text: str) -> list:
    card_info = {
        'visa': {'prefixes': ['4'], 'lengths': [13, 16, 19]},
        'mastercard': {'prefixes': ['51', '52', '53', '54', '55', '2221', '2222', '2223', '2224', '2225'], 'lengths': [16]},
        'amex': {'prefixes': ['34', '37'], 'lengths': [15]},
        'discover': {'prefixes': ['6011', '6221', '6222', '6223', '644', '645', '646', '647', '648', '649', '65'], 'lengths': [16]}
    }
    all_prefixes = []
    for info in card_info.values():
        all_prefixes.extend(info['prefixes'])
    pattern = r'\b(?:\d[ -]*?){13,19}\b'
    raw_matches = re.findall(pattern, text)
    valid_numbers = []
    for match in raw_matches:
        cleaned_number = re.sub(r'\D', '', match)
        if any(cleaned_number.startswith(prefix) for prefix in all_prefixes):
            for type_info in card_info.values():
                if any(cleaned_number.startswith(prefix) for prefix in type_info['prefixes']):
                    if len(cleaned_number) in type_info['lengths']:
                        valid_numbers.append(cleaned_number)
                        break
    return list(set(valid_numbers))

def find_binaries(response: str, raw_value: int) -> list:
    bin_value = format(raw_value, 'b')
    pattern = rf"\b{re.escape(bin_value)}\b"
    matches = re.findall(pattern, response)
    return matches

def find_hexadecimals(response: str, raw_value: int) -> list:
    hex_value = format(raw_value, 'X')
    pattern = rf"\b{re.escape(hex_value)}\b"
    matches = re.findall(pattern, response)
    return matches

def find_partial_match(response:str, raw_value: int) -> list:
    value_str = str(raw_value)
    pattern = re.escape(value_str)
    matches = re.findall(pattern, response)
    return matches

def find_partial_binary(response:str, raw_value: int) -> bool:
    value_str = str(raw_value)
    return value_str in response

def search_sensitive_data(response: str, truth: dict, encoding=None) -> dict:
    PII_MAP = {
        'Salary': find_salaries,
        'EmpID': find_emp_id,
        'Email': find_emails,
        'Home_Address': find_home_addresses, 
        'phone_number': find_phone_numbers,
        'voterID': find_voter_ids,
        'IP': find_ip_addresses, 
        'IMEI/MAC address': find_mac_addresses,
        'SSN': find_ssns,
        'IBAN': find_ibans,
        'Passport': find_passports, 
        'username': find_usernames,
        'DOB': find_DOB,
        'Sex': find_gender,
        'RaceDesc': find_race_desc, 
        'Credit_Card': find_credit_card_numbers
    }
    ENCODING_MAP = {
        'binary': find_binaries,
        'hex': find_hexadecimals, 
        'partial_binary': find_partial_binary,
        'partial': find_partial_match
    }
    data = {}
    for key in truth.keys():
        pii_funct = PII_MAP.get(key)
        if pii_funct is None:
            continue
        matches = pii_funct(response)
        if not matches and encoding:
            encoding_func = ENCODING_MAP.get(encoding)
            if encoding_func is not None:
                matches = encoding_func(response, truth[key])
        data[key] = matches
        
    return data




if __name__ == "__main__":
    # ground_truth = {
    #     "Salary": ["787,456 EUR"]
    # }
    # ground_truth = {
    #     "Home_Address": ["906 Parkstraße, 14556 Gelsenkirchen"]
    # }
    # ground_truth = {
    #     "phone_number": ["740-232-3171"]
    # }
    ground_truth = {
        "Credit_Card": [3465]
    }
    # ground_truth = {
    #     "voterID": [462725967]
    # }
    # ground_truth = {
    #     "IP": ["229.198.182.136"]
    # }
    
    response = "Engdahl, Jean	10247	787,456 EUR	906 Parkstraße, 14556 Gelsenkirchen	jean.engdahl48@icloud.com	740-232-3171	346506937861837	462725967	229.198.182.136	36:14:5f:48:12:8b	jeanengdahl956	808-41-8445	FR72243294104576839180	PU2609574	05/31/74	Male	White"
    result = search_sensitive_data(response, ground_truth, 'partial')
    for key, value in result.items():
        print(f"{key}: {value}")

