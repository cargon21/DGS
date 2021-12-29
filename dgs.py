# This dgs.py file contains the locations for all the web pages as well as the executions of their functionality. 
# This includes adding to the db, deleting from the db, redirecting users to different pages, and saving game images

import secrets
import os
from flask import Flask, render_template,  flash, url_for, redirect
from connection import *
from forms import *

app = Flask(__name__) # __name__ is a module
app.config['SECRET_KEY'] = '6736ba0c224d73bcd33368563b92c044'

# location of home page
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

# Location of admin categories page
@app.route("/home/<string:category>", methods=['GET', 'POST'])
def exploreCategory(category):
    gamesList = categoryGames(category)

    return render_template('category.html', categoryName = category, gameList = gamesList)

# Location of admin game page
@app.route("/home/game-<string:theTitle>", methods=['GET', 'POST'])
def gamePage(theTitle):
    gameData, gamePrices = gameContent(theTitle)
    return render_template('gamePage.html', titleName = theTitle, gameData = gameData, gamePrices =  gamePrices)

# Location of admin login page
@app.route("/adminLogin", methods=['GET', 'POST'])
def adminLogin():
    form = Login()
    if form.validate_on_submit():
        if form.username.data == "admin" and form.password.data == "admin123":
            return redirect(url_for('admin'))
        else:
            flash('Incorrect Login, Please Try Again!')
            return redirect(url_for('adminLogin'))
    return render_template('adminLogin.html', form = form)

# Location of admin login page
@app.route("/admin", methods=['GET', 'POST'])
def admin():
    return render_template('Admin/admin.html')

# function that saves image to file system
def savePicture(formImage):
    randomHex = secrets.token_hex(8)
    _, fExt = os.path.splitext(formImage.filename)
    imageFile = randomHex + fExt
    picturePath = os.path.join(app.root_path, 'static/Images', imageFile)
    formImage.save(picturePath)
    return imageFile

# Location of add game page
@app.route("/admin/addGame", methods=['GET', 'POST'])
def addGame():
    form = AddGame()
    if form.validate_on_submit():
        if form.imageURL.data:
            form.imageURL.data = savePicture(form.imageURL.data)
        
        if addGameToDB(form.title.data, form.developer.data, form.publisher.data, form.genre.data, form.releaseDate.data, 
                    form.price.data, form.rating.data, form.siteName.data, form.siteURL.data, form.imageURL.data, 
                    form.description.data):
            flash(f'The Game: {form.title.data} Was Added!')
            return redirect(url_for('admin'))
        else:
            flash(f'Duplicate Entry: {form.title.data} was not added')
            return redirect(url_for('admin'))
    return render_template('Forms/addGame.html', title = 'Add a Game', form = form)

# Location of add price page
@app.route("/admin/addPrice", methods = ['GET', 'POST'])
def addPrice():
    form = AddPrice()
    if form.validate_on_submit():
        addPriceToDB(form.title.data, form.price.data, form.siteName.data, form.siteURL.data)
        flash(f'The Game: {form.title.data} Has a New Price!')
        return redirect(url_for('admin'))
    return render_template('Forms/addPrice.html', title = 'Add a Price', form = form)

# Location of delete game page
@app.route("/admin/deleteGame", methods = ['GET', 'POST'])
def deleteGame():
    form = DeleteGame()
    if form.validate_on_submit():
        deleteGameFromDB(form.title.data)
        flash(f'The Game: {form.title.data} Has Been Deleted!')
        return redirect(url_for('admin'))
    return render_template('Forms/deleteGame.html', title = 'Delete a Game', form = form)

# Location of delete price page
@app.route("/admin/deletePrice", methods = ['GET', 'POST'])
def deletePrice():
    form = DeletePrice()
    if form.validate_on_submit():
        deletePriceFromDB(form.title.data, form.price.data)
        flash(f'The Price For Game: {form.title.data} Has Been Deleted!')
        return redirect(url_for('admin'))
    return render_template('Forms/deletePrice.html', title = 'Delete a Price', form = form)

@app.route("/admin/displayGames", methods=['GET', 'POST'])
def displayGames():
    library = getLibrary()

    return render_template('Admin/displayGames.html', title = 'Delete a Game', length = len(library), library = library)

# Convenient server startup. Allows the server to start by running this file
if __name__ == '__main__':
    app.run(debug = True)