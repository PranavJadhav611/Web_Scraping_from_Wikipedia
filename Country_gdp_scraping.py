# Importing the necessary libraries

from bs4 import BeautifulSoup  # BeautifulSoup is a library for pulling data out of HTML and XML files.
import requests  # Requests is a simple HTTP library for making requests to URLs.
import pandas as pd

scrape_page = requests.get(
    "https://en.wikipedia.org/wiki/List_of_countries_by_largest_historical_GDP")  # Making a GET request to the specified URL
page = BeautifulSoup(scrape_page.text, "html.parser")  # Creating a BeautifulSoup object to parse the HTML content

# Extracting all the quotes from the page using the specified HTML element and class attributes

table_1= page.find_all('table',{'class':'wikitable'})[0]
table = table_1.find('tbody')
rows = table.find_all('tr')
columns = [v.text.replace('\n','') for v in rows[0].find_all('td')]
# print(columns)

df  = pd.DataFrame(columns = columns)
for i in range(1,len(rows)):
    tds = rows[i].find_all('td')
    values =  [td.text.replace('\n','').replace('\xa0','') for td in tds]
    # print(values)
    df.loc[i, 'Year'] = values[0]
    df.loc[i, columns[1:]] = values[1:]
print(df)

df_names = df.iloc[:, :1].copy()
df_names[df.columns[1:]] = df[df.columns[1:]].apply(lambda x: x.str.extract(r'([a-zA-Z ]+)', expand=False))
file_path = "P:/PortFolio Projects/Top_Gdp/Top_gdp_names.csv"
df_names.to_csv(file_path, index=False)

df_gdp = df.iloc[:, :1].copy()
df_gdp[df.columns[1:]] = df[df.columns[1:]].apply(lambda x: x.str.extract(r'([\d,.]+)', expand=False))
file_path = "P:/PortFolio Projects/Top_Gdp/Top_gdp_values.csv"
df_gdp.to_csv(file_path, index=False)

file_path = "P:/PortFolio Projects/Top_Gdp/Top_gdp.csv"
df.to_csv(file_path, index=False)


