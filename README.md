# Data Scraping and Loading of pokemondb.net data
This is my small, short-term personal project which I undertook as part of a data engineering challenge posted on Facebook.

The steps are straightforward:
1. Scrape all Pokemon data (number, name, type, stats) from Pokemon database (https://pokemondb.net/pokedex/all).
2. Store the results in an SQL database. For simplicity, use just a .db or .sqlite file.

The result of this project is the pokemon.db file.

When you look at the website, there are duplicate pokedex IDs referring to different versions of the same pokemon. I dealt with this by only keeping the 1st instance of the values and removing the rest. Hence, the output db file is not entirely accurate. This is evident in pokemon having different versions with no default typing e.g. Oricorio.

I included an environment file to assist people who want to get started on this with a blank slate. 