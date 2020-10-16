from api3 import db,app

db.create_all()
app.run(debug=True)
