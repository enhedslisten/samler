# -*- coding: utf-8 -*-
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, make_response
from models import Posts as Post
import requests, json, datetime, ConfigParser, time

# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
Config = ConfigParser.ConfigParser()
Config.read('config.ini')
    
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY=Config.get('Secrets', 'secret_key'),
    USERNAME='',
    PASSWORD=''
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

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

@app.route('/')
def show_posts_beta():
    posts = Post.select().order_by(Post.date.desc())
    return object_list('show_posts.html', posts, 'posts', is_admin=('username' in session))

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
