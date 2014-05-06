# -*- coding: utf-8 -*-
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, make_response
from models import Posts as Post
import requests, json, datetime, ConfigParser, time, codecs

# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
Config = ConfigParser.ConfigParser()
Config.readfp(codecs.open('config.ini', 'r', 'utf8'))
    
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY=Config.get('Secrets', 'secret_key'),
    USERNAME='',
    PASSWORD=''
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def is_number(str):
    try:
        int(str)
    except ValueError:
        return False
    
    return True

def object_list(template_name, qr, var_name='object_list', **kwargs):
    kwargs.update(
        page=int(request.args.get('page', 1)),
        pages=qr.count() / 30 + 1
    )
    kwargs[var_name] = qr.paginate(kwargs['page'], 30)
    return render_template(template_name, **kwargs)

def confirm_password(username, password):
    try:
        password_in_file = Config.get('Users', username)
        return password == password_in_file
    except:
        return False

def get_selected_post(id):
    if id and is_number(id): 
        q = Post.select().where(Post.id == int(id))
        selected_post = [u for u in q][0]
    else: 
        selected_post = None 
    return selected_post

@app.route('/', defaults={'id' : None})
@app.route('/<id>')
def show_posts_beta(id):
    posts = Post.select().where(Post.hidden != 1).order_by(Post.date.desc())
    selected_post = get_selected_post(id)
    return object_list('show_posts.html', posts, 'posts', is_admin=('username' in session), selected_post=selected_post)

@app.route('/setup')
def setup():
    if ('username' in session):
        search_terms = Config.get('Search_Terms', 'search_terms').split(',')
        return render_template('setup.html', search_terms=search_terms, is_admin=True)
    else:
      return redirect(url_for('show_posts_beta'))  

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('show_posts_beta'))


@app.route('/authenticate', methods=['POST'])
def authenticate():
    if (confirm_password(request.form['username'], request.form['password'])):
        session['username'] = request.form['username']
        return redirect(url_for('show_posts_beta'))
    else:
        time.sleep(2)
        flash('Incorrect username or password.', 'error')
        return redirect(url_for('login'))

@app.route('/hide/<id>')
def hide(id):
    app.logger.debug("getting to hide post id is %s" % id)
    if ('username' in session):
        q = Post.update(hidden=True).where(Post.id == id)
        q.execute()
    return redirect(url_for('show_posts_beta'))

@app.route('/promote/<id>')
def promote(id):
    app.logger.debug("getting to promote post, id is %s" % id)
    if ('username' in session):
        q = Post.update(promoted=True).where(Post.id == id)
        q.execute()
    return redirect(url_for('show_posts_beta'))

@app.route('/demote/<id>')
def demote(id):
    app.logger.debug("getting to demote post, id is %s" % id)
    if ('username' in session):
        q = Post.update(promoted=False).where(Post.id == id)
        q.execute()
    return redirect(url_for('show_posts_beta'))
    
@app.route('/showtweet/<id>')
def showtweet(id):
    resp = requests.get("https://api.twitter.com/1/statuses/oembed.json?id={0}&align=center".format(id))
    if resp.status_code == 200:
        resp_json = json.loads(resp.text)
        return make_response(resp_json['html'])


@app.route('/instagram', methods=['GET', 'POST'])
def instagram_updates():
    if request.method == 'GET':
        challenge = request.args.get('hub.challenge', '')
        app.logger.debug(challenge)
        return make_response(challenge)

@app.template_filter('dateformat')
def datetimeformat(value, format='%d-%m-%Y %H:%M'):
    date = datetime.datetime.fromtimestamp(value)
    return date.strftime(format)


@app.template_filter('https')
def httpsfilter(value):
    return value.replace('http://', 'https://')

#inject our template vars, making sure to encode as unicode
@app.context_processor
def inject_strings():
	name = u"Rødt KBH"
	subtitle = u"Hashtag og del dit billede af et #RødtKbh, så deltager du i konkurrencen om 5 biografbilletter." 
	return dict(app_name = name, subtitle = subtitle)

if __name__ == '__main__':
#    init_db()
    app.run(host="0.0.0.0", port=8088)
