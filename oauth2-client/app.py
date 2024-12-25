from flask import Flask, url_for, session, render_template, redirect, abort
from authlib.integrations.flask_client import OAuth, OAuthError
from authlib.oauth2.rfc7636 import create_s256_code_challenge
from authlib.common.security import generate_token
from datetime import timedelta

app = Flask(__name__)
app.secret_key = '!secret'
app.config.from_object('config')
app.config['SESSION_REFRESH_EACH_REQUEST'] = False
app.config['SESSION_COOKIE_SECURE'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=2)

oauth = OAuth(app)

oauth.register(
    name='oauth_server',
    client_id=app.config['MYSERVER_CLIENT_ID'],
    client_secret=app.config['MYSERVER_CLIENT_SECRET'],
    api_base_url='http://localhost:5001/', 
    authorize_url='http://localhost:5001/oauth/authorize',
    access_token_url='http://localhost:5001/oauth/token',
    userinfo_endpoint='http://localhost:5001/api/me',
    client_kwargs={'scope': 'profile admin'}, 
    fetch_token=lambda: session.get('token'),
)

oauth.register(
    name='twitter',
    client_id=app.config['TWITTER_CLIENT_ID'],
    client_secret=app.config['TWITTER_CLIENT_SECRET'],
    api_base_url='https://api.twitter.com/2/',
    authorize_url='https://twitter.com/i/oauth2/authorize',
    access_token_url='https://api.twitter.com/2/oauth2/token',
    userinfo_endpoint='https://api.twitter.com/2/users/me',
    client_kwargs={'scope': 'tweet.read users.read follows.read'},
    fetch_token=lambda: session.get('token')
)

oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    userinfo_endpoint='https://www.googleapis.com/userinfo/v2/me',
    client_kwargs={ 'scope': 'email profile' },
    fetch_token=lambda: session.get('token')
)

oauth.register(
    name='discord',
    client_id=app.config['DISCORD_CLIENT_ID'],
    client_secret=app.config['DISCORD_CLIENT_SECRET'],
    api_base_url='https://discord.com/api/',
    authorize_url='https://discord.com/api/oauth2/authorize',
    access_token_url='https://discord.com/api/oauth2/token',
    userinfo_endpoint='https://discord.com/api/users/%40me',
    client_kwargs={ 'scope': 'identify email connections' },
    fetch_token=lambda: session.get('token')
)

@app.errorhandler(OAuthError)
def handle_error(error):
    return render_template('error.html', error=error)

@app.route('/')
def homepage():
    user = session.get('user')
    provider = session.get('provider')
    return render_template('home.html', user=user, provider=provider)

@app.route('/login/<name>')
def login(name: str):
    client = oauth.create_client(name.lower())
    if not client:
        abort(404)

    code_verifier = generate_token(48)
    code_challenge = create_s256_code_challenge(code_verifier)
    session['code_verifier'] = code_verifier

    redirect_uri = url_for('auth', name=name, _external=True)

    return client.authorize_redirect(
        redirect_uri,
        code_challenge=code_challenge,
        code_challenge_method='S256'
    )

@app.route('/auth/<name>')
def auth(name: str):
    client = oauth.create_client(name)
    if not client:
        abort(404)

    token = client.authorize_access_token(
        code_verifier=session['code_verifier'] 
    )

    session.pop('code_verifier', None)

    user_info = client.userinfo(token=token)
    
    session['token'] = token
    session['user'] = user_info
    session['provider'] = name
    session.permanent = True
    
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# twitter
@app.route('/tweets')
def list_tweets():
    resp = oauth.twitter.get(f"users/{session['user']['data']['id']}/tweets")

    tweets = resp.json()
    return render_template('tweets.html', tweets=tweets)

# discord
@app.route('/disc')
def list_connections():
    resp = oauth.discord.get("users/@me/connections") 

    discord = resp.json()
    return render_template('discord.html', discord=discord)
