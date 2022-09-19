import os
from uuid0 import generate
from time import sleep
from faker import Faker
from typing import List, Union
from inspect import getdoc
from fastapi import FastAPI,Request,Query,BackgroundTasks
from fastapi.responses import HTMLResponse,FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# `app` instance 
app = FastAPI()
# For serve static Files 
app.mount("/static", StaticFiles(directory="static"), name="static")
# `faker` instance 
faker = Faker()

# `template` instance 
template = Jinja2Templates(directory='templates')

@app.get('/',response_class=HTMLResponse)
def root(request:Request):
    return template.TemplateResponse('index.html',{'request':request})

@app.get('/available')
def get_method_with_description():
    # suitable method 
    methods = ['aba', 'address', 'administrative_unit', 'am_pm', 'android_platform_token', 'ascii_company_email', 'ascii_email', 'ascii_free_email', 'ascii_safe_email', 'bank_country', 'bban', 'bothify', 'bs', 'building_number', 'catch_phrase', 'century', 'chrome', 'city', 'city_prefix', 'city_suffix', 'color', 'color_name', 'company', 'company_email', 'company_suffix', 'country', 'country_calling_code', 'country_code', 'credit_card_expire', 'credit_card_full', 'credit_card_number', 'credit_card_provider', 'credit_card_security_code', 'cryptocurrency_code', 'cryptocurrency_name', 'currency_code', 'currency_name', 'currency_symbol', 'current_country', 'current_country_code', 'date', 'day_of_month', 'day_of_week', 'dga', 'domain_name', 'domain_word', 'ean', 'ean13', 'ean8', 'ein', 'email', 'file_extension', 'file_name', 'file_path', 'firefox', 'first_name', 'first_name_female', 'first_name_male', 'first_name_nonbinary', 'fixed_width', 'free_email', 'free_email_domain', 'hex_color', 'hexify', 'hostname', 'http_method', 'iana_id', 'iban', 'image_url', 'internet_explorer', 'invalid_ssn', 'ios_platform_token', 'ipv4', 'ipv4_network_class', 'ipv4_private', 'ipv4_public', 'ipv6', 'isbn10', 'isbn13', 'iso8601', 'itin', 'job', 'language_code', 'language_name', 'last_name', 'last_name_female', 'last_name_male', 'last_name_nonbinary', 'lexify', 'license_plate', 'linux_platform_token', 'linux_processor', 'locale', 'localized_ean', 'localized_ean13', 'localized_ean8', 'mac_address', 'mac_platform_token', 'mac_processor', 'md5', 'military_apo', 'military_dpo', 'military_ship', 'military_state', 'mime_type', 'month', 'month_name', 'msisdn', 'name', 'name_female', 'name_male', 'name_nonbinary', 'nic_handle', 'numerify', 'opera', 'paragraph', 'password', 'phone_number', 'port_number', 'postalcode', 'postalcode_in_state', 'postalcode_plus4', 'postcode', 'postcode_in_state', 'prefix', 'prefix_female', 'prefix_male', 'prefix_nonbinary', 'pricetag', 'random_digit', 'random_digit_not_null', 'random_digit_not_null_or_empty', 'random_digit_or_empty', 'random_element', 'random_int', 'random_letter', 'random_lowercase_letter', 'random_number', 'random_uppercase_letter', 'randomize_nb_elements', 'rgb_color', 'rgb_css_color', 'ripe_id', 'safari', 'safe_color_name', 'safe_domain_name', 'safe_email', 'safe_hex_color', 'secondary_address', 'sentence', 'sha1', 'sha256', 'slug', 'ssn', 'state', 'state_abbr', 'street_address', 'street_name', 'street_suffix', 'suffix', 'suffix_female', 'suffix_male', 'suffix_nonbinary', 'swift', 'swift11', 'swift8', 'text', 'time', 'timezone', 'tld', 'unix_device', 'unix_partition', 'unix_time', 'upc_a', 'upc_e', 'uri', 'uri_extension', 'uri_page', 'uri_path', 'url', 'user_agent', 'user_name', 'uuid4', 'windows_platform_token', 'word', 'year', 'zipcode', 'zipcode_in_state', 'zipcode_plus4']
    method_with_desc = []
    for method in methods:
        doc = eval(f'getdoc(faker.{method})')
        if not doc is None and doc.startswith('Generate'):
            doc = doc.split('.')[0]
        else:
            article = 'an' if method[0] in ['a','e','i','o','u'] else 'a'
            doc = f'Generate {article} {method}'
        method_with_desc.append({'method':method,'desc':doc})
    return method_with_desc

def delete_file(path):
    sleep(10)
    os.remove(path)

@app.get('/gen')
async def genarate_sql(rowqty:int,backgroundTasks:BackgroundTasks,table:str,field:Union[List[str], None]=Query(default=None),notnull:Union[List[int], None]=Query(default=None)):
    file = generate().base62 + '.sql'
    path = f'/tmp/{file}'
    with open(path,'w') as fl:
        fl.write(f'CREATE TABLE {table} (\n')
        fl.write('\bid uuid PRIMARY KEY DEFAULT uuid_generate_v4(),\n')
        i = 1
        field_copy = field.copy()
        last = field_copy.pop()
        for f in field:
            datatype = 'TEXT' if eval(f'type(faker.{f}())') == str else 'INT' if eval(f'type(faker.{f}())') == int else 'FLOAT'
            if f == last:
                if i in notnull:
                    fl.write(f'\b{f} {datatype} NOT NULL\n')
                else:
                    fl.write(f'\b{f} {datatype}\n')
            else:
                if i in notnull:
                    fl.write(f'\b{f} {datatype} NOT NULL,\n')
                else:
                    fl.write(f'\b{f} {datatype},\n')
            i+=1
        fl.write(');\n')
        for i in range(rowqty):
            fl.write(f'INSERT INTO {table} (')
            for f in field:
                if f == last:
                    fl.write(f'{f})')
                else:
                    fl.write(f'{f},')
            fl.write(' VALUES (')
            for f in field:
                value = eval(f'faker.{f}()')
                dtype = type(value)
                if f == last:
                    if dtype == str:
                        fl.write(f"\'{value}\');\n")
                    else:
                        fl.write(f'{value});\n')
                else:
                    if dtype == str:
                        fl.write(f"\'{value}\',")
                    else:
                        fl.write(f'{value},')
        fl.close()
        backgroundTasks.add_task(delete_file,path)
        return FileResponse(path,filename=f"{table}.sql")