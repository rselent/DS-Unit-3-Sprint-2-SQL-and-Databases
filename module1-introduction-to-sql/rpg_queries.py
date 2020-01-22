"""
Scratch/assignment sql -- 3_2_1
"""

import sqlite3

SLCONN = sqlite3.connect( "rpg_db.sqlite3")			# local file in same dir
SLCURSE = SLCONN.cursor()


def totalChars():
	query = """
	SELECT COUNT( ccChar.character_id) 
	FROM charactercreator_character AS ccChar;
	"""
	return SLCURSE.execute( query).fetchall()

def totalSubclass( subclass):
	if subclass == "charactercreator_necromancer":
		query = """
		SELECT COUNT( mage_ptr_id)
		FROM """ + subclass + ";"
	else:
		query = """
		SELECT COUNT( character_ptr_id)
		FROM """ + subclass + ";"
	return SLCURSE.execute( query).fetchall()
	
def totalItems():
	query = """
	SELECT COUNT( arm.item_id) 
	FROM armory_item AS arm;
	"""
	return SLCURSE.execute( query).fetchall()

def totalWeapons():
	query = """
	SELECT COUNT( wep.item_ptr_id) 
	FROM armory_weapon AS wep;
	"""
	return SLCURSE.execute( query).fetchall()

def char_totalItems():
	query = """
	SELECT ccChar.name, ccChar.character_id, COUNT( arm.item_id)
	FROM charactercreator_character AS ccChar,
	armory_item AS arm,
	charactercreator_character_inventory AS ccCharInv
	WHERE ccChar.character_id = ccCharInv.character_id
	AND arm.item_id = ccCharInv.item_id
	GROUP BY ccChar.character_id
	ORDER BY COUNT( arm.item_id) DESC, ccChar.character_id
	LIMIT 20;
	"""
	return SLCURSE.execute( query).fetchall()

def char_totalWeapons():
	query = """
	SELECT ccChar.name, ccChar.character_id, COUNT( wep.item_ptr_id)
	FROM charactercreator_character AS ccChar,
	armory_weapon AS wep,
	charactercreator_character_inventory AS ccCharInv
	WHERE ccChar.character_id = ccCharInv.character_id
	AND wep.item_ptr_id = ccCharInv.item_id
	GROUP BY ccChar.character_id
	ORDER BY COUNT( wep.item_ptr_id) DESC, ccChar.character_id
	LIMIT 20;
	"""
	return SLCURSE.execute( query).fetchall()

def char_avgGear( type):
	if type == "items":
		query = """
		SELECT COUNT( arm.item_id)
		FROM armory_item AS arm,
		charactercreator_character_inventory AS ccCharInv
		WHERE arm.item_id = ccCharInv.item_id
		"""
	elif type == "weapons":
		query = """
		SELECT COUNT( wep.item_ptr_id)
		FROM armory_weapon AS wep,
		charactercreator_character_inventory AS ccCharInv
		WHERE wep.item_ptr_id = ccCharInv.item_id
		"""
	return SLCURSE.execute( query).fetchall()


def main():

# SUPPLEMENTAL MATH (because sql functions like AVG return wonky results atm)
	itemsNotWep = (int( str( totalItems()).strip( "[(,)]")) - 
				   int( str( totalWeapons()).strip( "[(,)]")) 
				  )
	avgItems = (int( str( char_avgGear( "items")).strip( "[(,)]")) / 
				int( str( totalChars()).strip( "[(,)]")) 
			   )
	avgWeapons = (int( str( char_avgGear( "weapons")).strip( "[(,)]")) / 
				  int( str( totalChars()).strip( "[(,)]")) 
				 )

# MAIN OUTPUT
	print( "\n\nTotal number of characters: {}".format( 
					str( totalChars()).strip( "[(,)]") )
	)
	print( "\nTotal number of each specific subclass:", 
			"\n\tMage:\t {}".format( str( totalSubclass( 
							"charactercreator_mage")).strip( "[(,)]")),
			"\t({} are Necromancers)".format( str( totalSubclass(
							"charactercreator_necromancer")).strip( "[(,)]")),
			"\n\tThief:\t  {}".format( str( totalSubclass( 
							"charactercreator_thief")).strip( "[(,)]")),
			"\n\tCleric:   {}".format( str( totalSubclass( 
							"charactercreator_cleric")).strip( "[(,)]")),
			"\n\tFighter:  {}".format( str( totalSubclass( 
							"charactercreator_fighter")).strip( "[(,)]"))
	)
	print( "\nTotal number of items in rpg: {}".format( 
					str( totalItems()).strip( "[(,)]"))
	)
	print( "\nTotal number of items that are weapons:  {}".format( 
					str( totalWeapons()).strip( "[(,)]")),
			"\nTotal that are not:\t\t\t{}".format( itemsNotWep) 
	)
	print( "\nTop 20 characters with the most items",
			"(sorted by character_id): \n\n {}".format( 
					str( char_totalItems()).
					strip( "[(,)]").
					replace( "),", "\n").
					replace( "(", "").
					replace( "'", ""))
	)
	print( "\nTop 20 characters with the most weapons",
			"(sorted by character_id): \n\n {}".format( 
					str( char_totalWeapons()).
					strip( "[(,)]").
					replace( "),", "\n").
					replace( "(", "").
					replace( "'", ""))
	)
	print( "\nThe average number of items each character has:    {:.2f}".format( 
					avgItems)
	)
	print( "The average number of weapons each character has:  {:.2f}\n".format( 
					avgWeapons)
	)
	return 0


if __name__ == "__main__":
	main()
