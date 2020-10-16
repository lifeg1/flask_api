from flask import Flask
from flask_restful import Resource,Api
from secure import authenticate,identity
from flask_jwt import JWT,jwt_required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os



app=Flask(__name__)
app.config['SECRET_KEY']='mysecretkey'
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqllite')
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False

db=SQLAlchemy(app)
# Migrate(app,db)
api=Api(app)
jwt=JWT(app,authenticate,identity)


class Product(db.Model):                                   #model
    __tablename__="product"
    product_name=db.Column(db.String(80),primary_key=True)


    def __init__(self,product_name):
        self.product_name=product_name

    def json(self):
        return {'PRODUCT NAME':self.product_name}



class ProductName(Resource):
    def get(self,name):
        pro=Product.query.filter_by(product_name=name).first()
        if pro:
            return pro.json()
        else:
            return {'PRODUCT NAME':None},404

    def post(self,name):
        pro=Product(product_name=name)
        db.session.add(pro)
        db.session.commit()

        return pro.json()

    def delete(self,name):
        pro=Product.query.filter_by(product_name=name).first()
        db.session.delete(pro)
        db.session.commit()
        return {'note':'delete success'}

class AllNames(Resource):
    @jwt_required()
    def get(self):
        products=Product.query.all()
        if products:
            return [pro.json() for pro in products]
        else:
            return {'note':'fetch unsuccess'},404

api.add_resource(ProductName,'/product/<string:name>')
api.add_resource(AllNames,'/products')


if __name__=='__main__':
    app.run(debug=True)
