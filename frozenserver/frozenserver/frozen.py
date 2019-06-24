from flask import Flask, render_template, redirect, url_for, request, flash, \
    jsonify
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from setup import User, Base, Item, Category
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('/var/www/frozenserver/frozenserver/client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Frozen Market App"

engine = create_engine('postgresql+psycopg2://postgres:test@localhost/frozen')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    """ Create anti-forgery state token """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    print
    "The current session state is %s" % login_session['state']
    return render_template('login.html', state=state)


@app.route('/gconnect', methods=['GET', 'POST'])
def gconnect():
    """ Validate state token"""
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        print
        response
        return response
    """ Obtain authorization code"""
    code = request.data

    try:
        """ Upgrade the authorization code into a credentials object"""
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    """ Check that the access token is valid."""
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    print
    "access token result %s" % result
    """ If there was an error in the access token info, abort."""
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    """ Verify that the access token is used for the intended user."""
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    """ Verify that the access token is valid for this app."""
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print
        "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    """ Store the access token in the session for later use."""
    login_session['provider'] = 'google'
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    # print "gplus_id: %s" % login_session['gplus_id']

    """ Get user info"""
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    # print 'data is %s' % data
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    """ see if user exists"""

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
        login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += '" style = "width: 300px; height: 300px;border-radius: ' \
              '150px;-webkit-border-radius: 150px;-moz-border-radius: ' \
              '150px;">'
    flash("You are now logged in as %s" % login_session['username'])
    return output


def createUser(login_session):
    """ Helper Functions for New User"""
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    """ Helper Functions for getting User info based on user_id"""
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    """ Helper Functions for getting User ID based on email"""
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/gdisconnect')
def gdisconnect():
    """ Revoke a current user's token and reset their login_session"""
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % \
          login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print "result %s" % result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/')
@app.route('/categories/', methods=['GET', 'POST'])
def showAll():
    categories = session.query(Category).all()
    return render_template('home1.html', categories=categories)


@app.route('/')
@app.route('/categories/JSON')
def showAllJSON():
    categories = session.query(Category).all()
    return jsonify(Category=[i.serialize for i in categories])


@app.route('/')
@app.route('/users/JSON')
def showUserJSON():
    users = session.query(User).all()
    return jsonify(User=[i.serialize for i in users])


@app.route('/category/new', methods=['GET', 'POST'])
def newCatF():
    if 'email' not in login_session:
        return redirect('/login')
    user = getUserInfo(getUserID(login_session['email']))
    if request.method == 'POST':
        newC = Category(name=request.form['name'],
                        description=request.form['description'],
                        user_id=user.id)
        session.add(newC)
        session.commit()
        return redirect(url_for('showAll'))
        flash('New Category %s Successfully Created.' % newC.name)

    else:
        return render_template('newCategory.html')


@app.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
def editCatF(category_id):
    if 'email' not in login_session:
        return redirect('/login')
    categories = session.query(Category).filter_by(id=category_id).one()
    editedCat = session.query(Category).filter_by(id=category_id).one()
    creator = session.query(User).filter_by(
        email=login_session['email']).one()
    print
    "diffrence: %s %s" % (editedCat.user_id, creator.id)
    if editedCat.user_id != creator.id:
        return "<script>function myFunction() {alert('You are not " \
               "authorized " \
               "to delete or modify this " \
               "page.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedCat.name = request.form['name']
            editedCat.description = request.form['description']
            session.add(editedCat)
            session.commit()
            flash('Selected category has been edited successfully.')
        return redirect(url_for('showAll'))
    else:
        return render_template('editCategory.html',
                               category_id=categories.id,
                               categories=categories,
                               cat=editedCat)


@app.route('/category/<int:category_id>/delete', methods=['GET', 'POST'])
def deleteCatF(category_id):
    if 'email' not in login_session:
        return redirect('/login')
    categories = session.query(Category).filter_by(id=category_id).one()
    deletedCat = session.query(Category).filter_by(id=category_id).one()
    creator = session.query(User).filter_by(
        email=login_session['email']).one()
    if deletedCat.user_id != creator.id:
        return "<script>function myFunction() {alert('You are not " \
               "authorized " \
               "to delete or modify this " \
               "page.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(deletedCat)
        session.commit()
        return redirect(url_for('showAll'))
        flash('Selected category has been removed successfully.')
    else:
        return render_template('deleteCategory.html',
                               category_id=categories.id,
                               categories=categories,
                               cat=deletedCat)


@app.route('/category/<int:category_id>/items/', methods=['GET', 'POST'])
def showItems(category_id):
    categories = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template('items.html', categories=categories, items=items,
                           category_id=categories.id)


@app.route('/category/<int:category_id>/items/JSON', methods=['GET', 'POST'])
def showItemsJSON(category_id):
    categories = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(Item=[i.serialize for i in items])


@app.route('/category/<int:category_id>/items/<int:item_id>/',
           methods=['GET', 'POST'])
def soloItemF(category_id, item_id):
    categories = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(id=item_id).one()
    return render_template('soloItem.html', categories=categories, items=items,
                           category_id=categories.id, item_id=items.id)


@app.route('/category/<int:category_id>/items/<int:item_id>/JSON',
           methods=['GET', 'POST'])
def soloItemJSON(category_id, item_id):
    categories = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(id=item_id).one()
    return jsonify(Item=[items.serialize])


@app.route('/category/<int:category_id>/items/new', methods=['GET', 'POST'])
def newItemF(category_id):
    if 'email' not in login_session:
        return redirect('/login')
    categories = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    user = getUserInfo(getUserID(login_session['email']))

    if request.method == 'POST':
        newI = Item(name=request.form['name'],
                    nutrients=request.form['nutrients'],
                    price=request.form['price'],
                    weight=request.form['weight'],
                    user_id=user.id,
                    category_id=category_id)
        session.add(newI)
        session.commit()
        return redirect(url_for('showItems', category_id=categories.id))
        flash('New item has been added successfully.')
    else:
        return render_template('newItem.html', category_id=category_id,
                               categories=categories, items=items)


@app.route('/category/<int:category_id>/items/<int:item_id>/edit',
           methods=['GET', 'POST'])
def editItemF(category_id, item_id):
    if 'email' not in login_session:
        return redirect('/login')
    categories = session.query(Category).filter_by(id=category_id).one()
    editedItem = session.query(Item).filter_by(id=item_id).one()
    creator = session.query(User).filter_by(
        email=login_session['email']).one()
    if editedItem.user_id != creator.id:
        return "<script>function myFunction() {alert('You are not " \
               "authorized " \
               "to delete or modify this " \
               "page.');}</script><body onload='myFunction()''>"

    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
            editedItem.nutrients = request.form['nutrients']
            editedItem.price = request.form['price']
            editedItem.weight = request.form['weight']
            session.add(editedItem)
            session.commit()
            flash('Selected item has been edited successfully.')
        return redirect(url_for('showItems', category_id=categories.id))
    else:
        return render_template('editItem.html',
                               item_id=item_id,
                               category_id=categories.id,
                               categories=categories,
                               items=editedItem)


@app.route('/category/<int:category_id>/items/<int:item_id>/delete',
           methods=['GET', 'POST'])
def deleteItemF(category_id, item_id):
    if 'email' not in login_session:
        return redirect('/login')
    categories = session.query(Category).filter_by(id=category_id).one()
    deletedItem = session.query(Item).filter_by(id=item_id).one()
    creator = session.query(User).filter_by(
        email=login_session['email']).one()
    if deletedItem.user_id != creator.id:
        return "<script>function myFunction() {alert('You are not " \
               "authorized to delete or modify this " \
               "page.');}</script><body onload='myFunction()''>"

    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash(
            'Selected item has been removed successfully from this category.')
        return redirect(url_for('showItems', category_id=categories.id))
    else:
        return render_template('deleteItem.html',
                               item_id=item_id,
                               category_id=categories.id,
                               categories=categories,
                               items=deletedItem)


@app.route('/disconnect')
def disconnect():
    """ Disconnect based on provider """
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
        # del login_session['gplus_id']
        # del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
        # del login_session['facebook_id']
        # del login_session['username']
        # del login_session['email']
        # del login_session['picture']
        # del login_session['user_id']
        # del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showAll'))
    else:
        return redirect(url_for('showAll'))
        flash("You were not logged in")


if __name__ == '__main__':
    app.run()
