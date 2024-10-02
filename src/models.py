from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    # is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorite_character = db.relationship('FavoriteCharacter', backref='user', lazy=True)
    favorite_planet = db.relationship('FavoritePlanet', backref='user', lazy=True)
    favorite_vehicle = db.relationship('FavoriteVehicle', backref='user', lazy=True)


    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name":self.name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
class FavoriteCharacter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #relacion de uno User a muchos con Favorite_character
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #relacion de uno Character a muchos con Favorite_character
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)

    def __repr__(self):
        return '<FavoriteCharacter %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id
        }


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    height = db.Column(db.String(120), nullable=False)
    mass = db.Column(db.String(120), nullable=False)
    hair_color = db.Column(db.String(120), nullable=False)
    skin_color = db.Column(db.String(120), nullable=False)
    eye_color = db.Column(db.String(120), nullable=False)
    birth_year = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(120), nullable=False)
    favorite_character = db.relationship('FavoriteCharacter', backref='character', lazy=True)
    
    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name":self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color":self.hair_color,
            "skin_color":self.skin_color,
            "eye_color" :self.eye_color,
            "birth_year":self.birth_year,
            "gender":self.gender,
        }

class FavoritePlanet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=False)

    def __repr__(self):
        return '<FavoritePlanet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id
        }



class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    rotation_period = db.Column(db.String(120), nullable=False)
    diameter = db.Column(db.String(120), nullable=False)
    climate = db.Column(db.String(120), nullable=False)
    gravity = db.Column(db.String(120), nullable=False)
    terrain = db.Column(db.String(120), nullable=False)
    population = db.Column(db.String(120), nullable=False)
    favorite_planet = db.relationship('FavoritePlanet', backref='planet', lazy=True)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name":self.name,
            "rotation_period": self.rotation_period,
            "diameter": self.diameter,
            "climate":self.climate,
            "gravity":self.gravity,
            "terrain" :self.terrain,
            "population":self.population,
        }
    
class FavoriteVehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)

    def __repr__(self):
        return '<FavoriteVehicle %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "vehicle_id": self.vehicle_id
        }


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    model = db.Column(db.String(120), nullable=False)
    length = db.Column(db.String(120), nullable=False)
    cargo_capacity = db.Column(db.String(120), nullable=False)
    vehicle_class= db.Column(db.String(120), nullable=False)
    manufacturer= db.Column(db.String(120), nullable=False)
    favorite_vehicle = db.relationship('FavoriteVehicle', backref='vehicle', lazy=True)


    def __repr__(self):
        return '<Vehicle %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name":self.name,
            "model": self.model,
            "length": self.length,
            "cargo_capacity":self.cargo_capacity,
            "vehicle_class":self.vehicle_class,
            "manufacturer":self.manufacturer,
        }


