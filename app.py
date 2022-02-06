from flask import Flask, render_template
from blueprints.users import users_bp
from blueprints.media import media_bp
from blueprints.review import reviews_bp

app = Flask(__name__)

app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(media_bp, url_prefix='/media')
app.register_blueprint(reviews_bp, url_prefix='/reviews')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=8001, debug=True)
