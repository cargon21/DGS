# This connection.py file contains the code to connect to the database as well as the functions necessary to perform
# various MYSQL functions such as insertion and deletion into the video games database

import mysql.connector

# connects to the MYSQL database
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="1053500Sy!",
        database='gameschama'
    )
except:
    print("there was a connection error")

mycursor = mydb.cursor() #cursor that will execute the MYSQL expressions

def categoryGames(category):
    categoryGames = []
    
    # Selects the games from the database
    if category == "Explore All":
        categoryFomula = "SELECT g.imageURL, g.title, c.developer, ge.genreName, p.price\
                         FROM game g \
                         JOIN creator c \
                         ON g.title = c.gameTitle \
                         JOIN genre ge \
                         ON g.title = ge.gameTitle \
                         JOIN rating r \
                         ON g.title = r.gameTitle \
                         JOIN price p \
                         ON g.title = p.gameTitle\
                         WHERE g.title = p.gameTitle\
                         AND   p.price = ( SELECT MIN(p1.price) \
                                           FROM price p1, game g1\
                                           WHERE p1.gameTitle = g1.title\
                                           AND g.title = g1.title ) \
                         ORDER BY r.rating DESC;"
    else:
        categoryFomula = "SELECT g.imageURL, g.title, c.developer, ge.genreName, p.price\
                         FROM game g \
                         JOIN creator c \
                         ON g.title = c.gameTitle \
                         JOIN genre ge \
                         ON g.title = ge.gameTitle \
                         JOIN rating r \
                         ON g.title = r.gameTitle \
                         JOIN price p \
                         ON g.title = p.gameTitle \
                         WHERE g.title = p.gameTitle\
                         AND ge.genreName = '%s' \
                         AND   p.price = ( SELECT MIN(p1.price) \
                                           FROM price p1, game g1\
                                           WHERE p1.gameTitle = g1.title\
                                           AND g.title = g1.title ) \
                         ORDER BY r.rating DESC;" % category

    mycursor.execute(categoryFomula) # Excecutes the statement

    for i in mycursor:
        categoryGames.append(i)  

    return categoryGames # Returns the list of games

def gameContent(gameTitle): 
    gamePrices = []
    gameFormula = "SELECT g.imageURL, g.title, g.releaseDate, g.descript, c.developer, c.publisher, ge.genreName, r.rating, p.price\
                        FROM game g \
                        JOIN creator c \
                        ON g.title = c.gameTitle \
                        JOIN genre ge \
                        ON g.title = ge.gameTitle \
                        JOIN rating r \
                        ON g.title = r.gameTitle \
                        JOIN price p \
                        ON g.title = p.gameTitle \
                        WHERE title = '%s' \
                        AND p.price = ( SELECT MIN(p1.price) \
                                        FROM price p1, game g1\
                                        WHERE p1.gameTitle = g1.title\
                                        AND g.title = g1.title );" % gameTitle
    mycursor.execute(gameFormula)
    gameContent = mycursor.fetchone()

    pricesFormula = "SELECT name, url, price \
                     FROM price\
                     JOIN website\
                     ON siteID = id\
                     WHERE gameTitle = '%s'\
                     ORDER BY\
                     price ASC;" % gameTitle

    mycursor.execute(pricesFormula)

    for i in mycursor:
        gamePrices.append(i)

    return gameContent, gamePrices

def addGameToDB(title, developer, publisher, genre, releaseDate, price, rating, siteName, siteURL, imageURL, description):
    try:
        arr = []
        gameFormula = "INSERT INTO game VALUES (%s, %s, %s, %s)" # formula with MYSQL expression
        newGame = ( title, releaseDate, imageURL, description)
        mycursor.execute(gameFormula, newGame) # Executes the statement and adds the game to the database
        
        # Other insertion expressions with similar structure
        ratingFormula = "INSERT INTO rating VALUES (%s, %s)"
        newRating = (title, rating)
        mycursor.execute(ratingFormula, newRating)

        developerFormula = "INSERT INTO creator VALUES (%s, %s, %s)"
        newCreator = (title, developer, publisher)
        mycursor.execute(developerFormula, newCreator)

        genreFormula = "INSERT INTO genre VALUES (%s,%s)"
        newGenre = (title, genre)
        mycursor.execute(genreFormula, newGenre)

        websiteFormula = "INSERT INTO website (name, url) VALUES (%s, %s)"
        newWebsite = (siteName, siteURL)
        mycursor.execute(websiteFormula, newWebsite)

        fetchSiteID = "SELECT id from website WHERE url = '%s'" % siteURL
        # set a cleared cursor to execute and get data for fetching the site ID
        clearCursor = mydb.cursor(buffered=True)
        clearCursor.execute(fetchSiteID)
        siteID = clearCursor.fetchall()[0][0]

        priceFormula = "INSERT INTO price VALUES (%s, %s, %s)"
        newPrice = (siteID, price, title)
        mycursor.execute(priceFormula, newPrice)
            
        mydb.commit() #Commits the changes so they are reflected in the database
        return True
    except:
        return False

    return True

# Adds a price to the DB if it doesn't exist. Updates the price if it does exist
def addPriceToDB(title, price, siteName, siteURL):
    
    websiteFormula = "INSERT INTO website (name, url) SELECT %s, %s WHERE NOT EXISTS ( \
                      SELECT url FROM website WHERE url = %s) LIMIT 1;"    
    
    newWebsite = (siteName, siteURL, siteURL)
    mycursor.execute(websiteFormula, newWebsite)
        
    priceFormula = "CALL SetLeastPrice(%s, %s, %s, %s)"
    newPrice = (title, price, siteName, siteURL)
    mycursor.execute(priceFormula, newPrice)

    # Below is the code for the stored procedure
    # UPDATE price, website
    # SET price = newPrice
    # WHERE website.id = price.siteID
    # AND website.url = siteURL;
    #
    # INSERT INTO price
    # SELECT website.id, newPrice, title
    # FROM website
    # WHERE website.url = siteURL
    # AND website.id NOT IN (SELECT siteID FROM price);

    mydb.commit()

# Removes a game from the DB
def deleteGameFromDB(title):

    deleteCreatorFormula = "DELETE FROM creator WHERE gameTitle = '%s'" % title
    mycursor.execute(deleteCreatorFormula)

    deleteGenreFormula = "DELETE FROM genre WHERE gameTitle = '%s'" % title
    mycursor.execute(deleteGenreFormula)

    deleteRatingFormula = "DELETE FROM rating WHERE gameTitle = '%s'" % title
    mycursor.execute(deleteRatingFormula)

    deletePriceAndWebsiteFormula = "DELETE website.*, price.* \
                             FROM price JOIN website ON id = siteID \
                             WHERE gameTitle = '%s';" % title

    mycursor.execute(deletePriceAndWebsiteFormula)
    
    deleteGameFormula = "DELETE FROM game WHERE title = '%s'" % title
    mycursor.execute(deleteGameFormula)
    mydb.commit()

# Deletes a game from the database
def deletePriceFromDB(title, price):
    deletePriceAndWebsiteFormula = "DELETE website.*, price.* \
                             FROM price JOIN website ON id = siteID \
                             WHERE gameTitle = '%s' AND price >= '%s' AND price <= '%s' + 0.01;" % (title, price, price)    

    mycursor.execute(deletePriceAndWebsiteFormula)
    mydb.commit()

# Returns the game library
def getLibrary():
    gamesLibrary = []
    getGamesFormula = "SELECT g.title, g.releaseDate, g.imageURL, g.descript, c.developer, c.publisher, ge.genreName, r.rating, w.id, w.name, p.price, w.url \
                       FROM game g \
                       JOIN creator c \
                       ON g.title = c.gameTitle \
                       JOIN genre ge \
                       ON c.gameTitle = ge.gameTitle \
                       JOIN rating r \
                       ON ge.gameTitle = r.gameTitle \
                       JOIN price p \
                       ON g.title = p.gameTitle \
                       JOIN website w \
                       ON p.siteID = w.id \
                       ORDER BY \
                       g.title ASC;"

    mycursor.execute(getGamesFormula)  

    for i in mycursor:
        gamesLibrary.append(i)  
    return gamesLibrary