from flask_app import app

from flask_app.controllers import parkings, users, pjs, qr

if __name__== '__main__':
    app.run(debug=True)