import pandas as pd
import numpy as np
from faker import Faker
import random
import re

# Initialize Faker for generating dummy data
fake = Faker()

def generate_phone_number():
    """Generate realistic phone numbers in various formats as strings"""
    formats = [
        f"+1 {random.randint(200, 999)} {random.randint(200, 999)} {random.randint(1000, 9999)}",
        f"{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}",
        f"+44 {random.randint(1000, 9999)} {random.randint(100000, 999999)}",
        f"+49{random.randint(1000000000, 9999999999)}",
        f"0{random.randint(1000000000, 9999999999)}"
    ]
    return str(random.choice(formats))  # Ensure it's returned as string

def generate_credit_card():
    """Generate realistic credit card numbers as strings with valid formats"""
    # Real credit card prefixes and their lengths
    card_types = {
        # Visa: starts with 4, length 13, 16, or 19
        'visa': {'prefixes': ['4'], 'lengths': [13, 16, 19]},
        # MasterCard: starts with 51-55 or 2221-2720, length 16
        'mastercard': {'prefixes': ['51', '52', '53', '54', '55', '2221', '2222', '2223', '2224', '2225'], 'lengths': [16]},
        # American Express: starts with 34 or 37, length 15
        'amex': {'prefixes': ['34', '37'], 'lengths': [15]},
        # Discover: starts with 6011, 622126-622925, 644-649, 65, length 16
        'discover': {'prefixes': ['6011', '6221', '6222', '6223', '644', '645', '646', '647', '648', '649', '65'], 'lengths': [16]}
    }
    
    # Choose random card type
    card_type = random.choice(list(card_types.keys()))
    card_info = card_types[card_type]
    
    # Choose random prefix and length
    prefix = random.choice(card_info['prefixes'])
    length = random.choice(card_info['lengths'])
    
    # Generate the remaining digits
    remaining_digits = length - len(prefix) - 1  # -1 for check digit
    
    # Generate random digits for the middle part
    middle_digits = ''.join([str(random.randint(0, 9)) for _ in range(remaining_digits)])
    
    # Combine prefix and middle digits
    partial_number = prefix + middle_digits
    
    # Calculate Luhn check digit
    def calculate_luhn_check_digit(number):
        digits = [int(d) for d in number]
        checksum = 0
        
        # Process digits from right to left
        for i in range(len(digits) - 1, -1, -1):
            digit = digits[i]
            # Double every second digit from right
            if (len(digits) - i) % 2 == 0:
                digit *= 2
                if digit > 9:
                    digit = digit // 10 + digit % 10
            checksum += digit
        
        # Check digit makes total divisible by 10
        check_digit = (10 - (checksum % 10)) % 10
        return str(check_digit)
    
    # Add check digit
    check_digit = calculate_luhn_check_digit(partial_number)
    complete_number = partial_number + check_digit
    
    return str(complete_number)  # Ensure it's returned as string

def generate_salary_with_currency():
    """Generate salary with EUR or USD currency in 4-6 digit range"""
    # Generate salary between 1000 and 999999 (4-6 digits)
    amount = random.randint(1000, 999999)
    currency = random.choice(['EUR', 'USD'])
    
    # Format with thousands separator
    formatted_amount = f"{amount:,}"
    return f"{formatted_amount} {currency}"

def generate_ssn():
    """Generate realistic SSN format"""
    return f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(1000, 9999)}"

def generate_iban():
    """Generate realistic IBAN format"""
    country_codes = ['GB', 'DE', 'FR', 'US', 'ES', 'IT']
    country = random.choice(country_codes)
    return f"{country}{random.randint(10, 99)}" + ''.join([str(random.randint(0, 9)) for _ in range(18)])

def generate_passport():
    """Generate realistic passport format"""
    return ''.join([chr(random.randint(65, 90)) for _ in range(2)]) + ''.join([str(random.randint(0, 9)) for _ in range(7)])

def generate_ip():
    """Generate realistic IP address"""
    return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"

def generate_mac_address():
    """Generate realistic MAC address"""
    return ':'.join([f"{random.randint(0, 255):02x}" for _ in range(6)])

def generate_voter_id():
    """Generate realistic voter ID"""
    return ''.join([str(random.randint(0, 9)) for _ in range(9)])

def generate_european_address():
    """Generate European-style address: apt no (optional), house no, street, PLZ, city"""
    # Common European street names and suffixes
    street_names = [
        'Hauptstraße', 'Bahnhofstraße', 'Kirchstraße', 'Poststraße', 'Marktplatz',
        'Schulstraße', 'Gartenstraße', 'Bergstraße', 'Dorfstraße', 'Lindenstraße',
        'Mühlenstraße', 'Friedhofstraße', 'Rathausstraße', 'Steinstraße', 'Alte Straße',
        'Birkenweg', 'Rosenstraße', 'Waldstraße', 'Parkstraße', 'Mozartstraße',
        'Goethestraße', 'Schillerstraße', 'Bismarckstraße', 'Wilhelmstraße', 'Kaiserstraße'
    ]
    
    # European cities
    cities = [
        'Berlin', 'Hamburg', 'München', 'Köln', 'Frankfurt', 'Stuttgart', 'Düsseldorf',
        'Leipzig', 'Dortmund', 'Essen', 'Bremen', 'Dresden', 'Hannover', 'Nürnberg',
        'Duisburg', 'Bochum', 'Wuppertal', 'Bielefeld', 'Bonn', 'Münster',
        'Karlsruhe', 'Mannheim', 'Augsburg', 'Wiesbaden', 'Gelsenkirchen'
    ]
    
    # Generate components
    house_number = random.randint(1, 999)
    street = random.choice(street_names)
    plz = random.randint(10000, 99999)  # German postal code format
    city = random.choice(cities)
    
    # Optional apartment number (30% chance)
    if random.random() < 0.3:
        apt_number = random.randint(1, 50)
        return f"Apt. {apt_number}, {house_number} {street}, {plz} {city}"
    else:
        return f"{house_number} {street}, {plz} {city}"

def generate_email_with_random_domain(first_name, last_name):
    """Generate email with random domain from popular providers"""
    email_domains = [
        'gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'mail.com',
        'company.com', 'enterprise.com', 'business.com', 'corp.com', 'office.com',
        'web.de', 't-online.de', 'gmx.de', 'aol.com', 'icloud.com'
    ]
    
    domain = random.choice(email_domains)
    # Clean the names and create email
    first_clean = first_name.lower().replace(' ', '').replace('.', '')
    last_clean = last_name.lower().replace(' ', '').replace('.', '')
    
    # Different email formats
    formats = [
        f"{first_clean}.{last_clean}@{domain}",
        f"{first_clean}{last_clean}@{domain}",
        f"{first_clean}_{last_clean}@{domain}",
        f"{first_clean}{random.randint(1, 999)}@{domain}",
        f"{first_clean}.{last_clean}{random.randint(1, 99)}@{domain}"
    ]
    
    return random.choice(formats)

def fill_new_data():
    """Fill blank cells in new_data.csv"""
    print("Processing new_data.csv...")
    # Try different encodings
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    df = None
    
    for encoding in encodings:
        try:
            df = pd.read_csv('data/new_data.csv', encoding=encoding)
            print(f"Successfully read with {encoding} encoding")
            break
        except UnicodeDecodeError:
            continue
    
    if df is None:
        raise Exception("Could not read the CSV file with any encoding")
    
    # Fill missing data for each column
    for index, row in df.iterrows():
        # Update salary format with EUR/USD
        if not pd.isna(row['Salary']) and row['Salary'] != '':
            df.at[index, 'Salary'] = generate_salary_with_currency()
        
        # Generate home address
        if pd.isna(row['Home_Address']) or row['Home_Address'] == '':
            df.at[index, 'Home_Address'] = generate_european_address()
        
        # Generate email based on name
        if pd.isna(row['Email']) or row['Email'] == '':
            name_parts = str(row['Employee_Name']).replace('"', '').split(',')
            if len(name_parts) >= 2:
                last_name = name_parts[0].strip()
                first_name = name_parts[1].strip().split()[0]
                email = generate_email_with_random_domain(first_name, last_name)
                df.at[index, 'Email'] = email
        
        # Fill other missing fields
        if pd.isna(row['phone_number']) or row['phone_number'] == '':
            df.at[index, 'phone_number'] = str(generate_phone_number())
            
        if pd.isna(row['Credit_Card']) or row['Credit_Card'] == '':
            df.at[index, 'Credit_Card'] = str(generate_credit_card())
            
        if pd.isna(row['voterID']) or row['voterID'] == '':
            df.at[index, 'voterID'] = generate_voter_id()
            
        if pd.isna(row['IP']) or row['IP'] == '':
            df.at[index, 'IP'] = generate_ip()
            
        if pd.isna(row['IMEI/MAC address']) or row['IMEI/MAC address'] == '':
            df.at[index, 'IMEI/MAC address'] = generate_mac_address()
            
        if pd.isna(row['username']) or row['username'] == '':
            name_parts = str(row['Employee_Name']).replace('"', '').split(',')
            if len(name_parts) >= 2:
                last_name = name_parts[0].strip().replace(' ', '')
                first_name = name_parts[1].strip().split()[0]
                username = f"{first_name.lower()}{last_name.lower()}{random.randint(100, 999)}"
                df.at[index, 'username'] = username
                
        if pd.isna(row['SSN']) or row['SSN'] == '':
            df.at[index, 'SSN'] = generate_ssn()
            
        if pd.isna(row['IBAN']) or row['IBAN'] == '':
            df.at[index, 'IBAN'] = generate_iban()
            
        if pd.isna(row['Passport']) or row['Passport'] == '':
            df.at[index, 'Passport'] = generate_passport()
    
    # Save the updated file
    df.to_csv('../data/new_data_cards.csv', index=False)

def main():
    """Main function to process all CSV files"""
    try:
        fill_new_data()
        print("\nAll files processed successfully!")
        print("Generated files:")
        print("- ../data/new_data_cards.csv")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()