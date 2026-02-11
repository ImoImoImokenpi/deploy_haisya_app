import os
from flask import Flask, send_from_directory
from app import create_app, db

app = create_app()

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                            'favicon.ico', mimetype='image/vnd.microsoft.icon')

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()

