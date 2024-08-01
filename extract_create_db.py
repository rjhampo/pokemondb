import sqlite3, re, selenium, pandas as pd, numpy as np
from bs4 import BeautifulSoup as bs
import selenium
import selenium.webdriver

def clean_cols(x):
    result = re.sub(r'[^\w]', '', x)
    return result

source_site = 'https://pokemondb.net/pokedex/all'
driver_options = selenium.webdriver.ChromeOptions()
driver_options.add_argument('--headless=new')

driver = selenium.webdriver.Chrome(options=driver_options)
driver.get(source_site)
bs_source = bs(driver.page_source, 'html.parser')
driver.quit()

source_table = bs_source.find('table')

table_cols = source_table.thead.tr.stripped_strings
db_cols = ['Number' if re.match(r'^\W', x) else clean_cols(x) for x in table_cols]

table_vals = source_table.tbody.find_all('tr')
db_vals = [x.find_all('td') for x in table_vals]

stat_vals = [[x.get_text(strip=True) for x in db_row[-7:]] for db_row in db_vals]
id_vals = [int(db_row[0].get_text(strip=True)) for db_row in db_vals]
name_vals = [db_row[1].find('a').get_text(strip=True) for db_row in db_vals]
type_vals = [[x.get_text(strip=True) for x in db_row[2].find_all('a')] for db_row in db_vals]

df = pd.DataFrame(data=zip(id_vals,name_vals,type_vals,*np.array(stat_vals).transpose()), columns=db_cols)
df = df.drop_duplicates(subset=['Number'])

# Had to break down list into two columns for dual typing
df.insert(3, 'secondarytype', [x[1] if len(x) > 1 else '' for x in df['Type']])
df['Type'] = df['Type'].map(lambda x: x[0])
df.rename(columns={'Type': 'primarytype'}, inplace=True)

conn = sqlite3.connect('pokemon.db')
curs = conn.cursor()

df.to_sql(name='pokedex', con=conn, index=False)

output = curs.execute('SELECT * FROM pokedex LIMIT 10')
print(output.fetchall())