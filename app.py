import os
from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv

load_dotenv()  # Cargar variables de entorno desde .env

app = Flask(__name__)

# Configura la clave secreta de Flask y las variables de Auth0
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'secret_key')
app.config['SESSION_COOKIE_NAME'] = 'your_session_cookie'

oauth = OAuth(app)

# Configurar Auth0
auth0 = oauth.register(
    'auth0',
    client_id=os.environ['AUTH0_CLIENT_ID'],
    client_secret=os.environ['AUTH0_CLIENT_SECRET'],
    client_kwargs={
        'scope': 'openid profile email',
    },
    server_metadata_url=f'https://{os.environ["AUTH0_DOMAIN"]}/.well-known/openid-configuration'
)


@app.route('/')
def home():
    user = session.get('user')
    if user:
        return f"Hola, {user['name']}!"
    else:
        return redirect('/login')


@app.route('/login')
def login():
    redirect_uri = url_for('callback', _external=True)
    return auth0.authorize_redirect(redirect_uri)

@app.route('/callback')
def callback():
    token = auth0.authorize_access_token()
    userinfo = auth0.userinfo(token=token)  # ✅ Esto es lo correcto
    session['user'] = userinfo
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
