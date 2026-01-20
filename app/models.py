from sqlalchemy.orm import relationship
from enum import Enum
from app import db
 
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), unique = True, nullable = False)
    password = db.Column(db.String(200), nullable = False)
    created_at = db.Column(db.DateTime(timezone = True))  

class Properties(db.Model):
    id = db.Column(db.Integer, primary_key = True )
    name = db.Column(db.String(200), unique = True, nullable = False)
    type = db.Column(db.String(40), nullable = False)
    images = relationship("Property_Images", back_populates="property")
    transaction = db.Column(db.String(10), nullable = False) 
    city = db.Column(db.String(50), nullable = False)
    neighbourhood = db.Column(db.String(50))
    price = db.Column(db.Float, nullable = False)
    beds = db.Column(db.Integer, nullable = False)
    baths = db.Column(db.Integer, nullable = False)
    sqmt = db.Column(db.Integer, nullable = False)
    features = relationship("Property_Features", back_populates="property")
    description = db.Column(db.String(255))
    active = db.Column(db.Boolean, default = True)
    created_at = db.Column(db.DateTime(timezone = True))  
    
class Property_Images(db.Model): 
    id = db.Column(db.Integer, primary_key = True )
    image = db.Column(db.String(255), nullable = False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'))
    property = relationship('Properties', back_populates='images')    
    
class Property_Features(db.Model):
    id = db.Column(db.Integer, primary_key = True )
    feature = db.Column(db.String(50), nullable = False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'))
    property = relationship('Properties', back_populates='features')

