"""
Scratch db lecture -- 3_2_2
"""

import psycopg2

dbname = "lzvrwfdj"
user = "lzvrwfdj"
password = "j9scE_ptq7yoHj0nyATM36mz4iILxurA"
host = "rajje.db.elephantsql.com"

pgConn = psycopg2.connect( dbname= dbname, user= user, password= password,
						   host= host)

pgCurse = pgConn.cursor()

statement_createTable = """
CREATE TABLE test_table (
  id        SERIAL PRIMARY KEY,
  name  varchar(40) NOT NULL,
  data    JSONB
);
"""

statement_insert = """
INSERT INTO test_table (name, data) VALUES
(
  'A row name',
  null
),
(
  'Another row, with JSON',
  '{ "a": 1, "b": ["dog", "cat", 42], "c": true }'::JSONB
);
"""

pgCurse.execute( statement_createTable)
pgConn.commit()

pgCurse.execute( statement_insert)
pgConn.commit()


query = "SELECT * FROM test_table;"

pgCurse.execute( query)
#print( pgCurse.fetchall())

import sqlite3

slConn = sqlite3.connect( "rpg_db.sqlite3")
slCurse = slConn.cursor()

rowCount = "SELECT COUNT(*) FROM charactercreator_character"
slCurse.execute( rowCount).fetchall()

getCharacters = "SELECT * FROM charactercreator_character"
characters = slCurse.execute( getCharacters).fetchall()

# slCurse.execute("PRAGMA table_info(charactercreator_character);").fetchall()

table_createCharacter = """
CREATE TABLE charactercreator_character (
  character_id SERIAL PRIMARY KEY,
  name VARCHAR(30),
  level INT,
  exp INT,
  hp INT,
  strength INT,
  intelligence INT,
  dexterity INT,
  wisdom INT
);
"""

pgCurse.execute( table_createCharacter)
pgConn.commit()

showTables = """
SELECT
   *
FROM
   pg_catalog.pg_tables
WHERE
   schemaname != 'pg_catalog'
AND schemaname != 'information_schema';
"""
pgCurse.execute(showTables)
#pgCurse.fetchall()

example_insert = """
INSERT INTO charactercreator_character
(name, level, exp, hp, strength, intelligence, dexterity, wisdom)
VALUES """ + str(characters[0][1:]) + ";"


for character in characters:
	character_insert = """
	INSERT INTO charactercreator_character 
	(name, level, exp, hp, strength, intelligence, dexterity, wisdom) 
	VALUES """ + str(characters[0][1:]) + ";"
	pgCurse.execute( character_insert)
pgConn.commit()








## TEST STUFF ##

#print( pgConn)
#print( len(characters))
#print( slCurse.execute("PRAGMA table_info(charactercreator_character);").fetchall())
#print( pgCurse.fetchall())
#print( characters[0])
#print( example_insert)

pgCurse.execute( "SELECT * FROM charactercreator_character")
print( pgCurse.fetchall())