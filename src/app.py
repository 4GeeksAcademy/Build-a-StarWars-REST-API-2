"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Vehicle, FavoriteCharacter, FavoritePlanet, FavoriteVehicle
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#------------------------------------------------------------ENDPOINTS-----------------------------------------------------------------------------

#codigo de ejemplo para probar los endpoints en postman
@app.route('/prueba', methods=['GET'])
def handle_hello():
    response_body = {
        "msg": "ok, esta funcionando "
    }
    return jsonify(response_body), 200

#-----------------------USER------------------------------------
#Obtiene información de todos los usuarios
@app.route('/users', methods=['GET'])
def get_users():
    try:
        #consultar al modelo todos los registros de usuarios
        query_results= User.query.all()
        #print(query_results)  #[<User 'Pepita'>, <User 'Lolita'>] se obtiene un array y para procesarlo y trabajar con esa info del array lo recorremos con el map
        results = list(map(lambda item: item.serialize(), query_results)) #al map en python le tenemos que pasar 2 valores primero la funcion lambda con su parametro item y a este parametro yo le voy a decir cada vez que te posiciones sobre ese valor que se esta consultando aplicale el metodo serialize() y en el segundo valor vendria a ser nombre del array que yo quiero que recorra 
        #print(results)#<map object at 0x79991ab0f1c0>  me arroja un valor ilegible por eso se tiene que castear(formatear) usando el list (envolviendo todo el map)
        if results:    
            response_body = {
                "msg": "ok",
                "results": results,
            }
            return jsonify(response_body), 200
        return jsonify({'error':'Users not found'}),404
    except Exception as e:
        return jsonify({'error':'Internal server error', 'message': str(e)}),500
    
#Obtiene la información de un solo usuario según su id
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    print(id)#1
    try:
        query_user = User.query.filter_by(id=id).first()
        #print(query_user.serialize())
        if query_user is None:
            return jsonify({'error':'User not found'}),404
        response_body = {
            "msg" : "ok",
            "result":query_user.serialize()
        }
        return jsonify(response_body),200
    except Exception as e:
        return jsonify({'error':'Internal server error', 'message': str(e)}),500
    
#Ruta POST new user  para crear un usuario
@app.route('/users', methods=['POST'])
def create_user():
    try:
        email = request.json.get('email')
        password = request.json.get('password')
        name = request.json.get('name')

        if not email or not password or not name:
            return jsonify({'error': 'Email, password and Name are required.'}), 400

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'error': 'Email already exists.'}), 409

        # password_hash = bcrypt.generate_password_hash(password).decode('utf-8') 

        # Ensamblamos el usuario nuevo
        new_user = User(email=email, password=password, name=name)

        db.session.add(new_user)
        db.session.commit()

        good_to_share_user = {
            'id': new_user.id,
            'name':new_user.name,
            'email':new_user.email,
        }

        return jsonify({'message': 'User created successfully.','user_created':good_to_share_user}), 201

    except Exception as e:
        return jsonify({'error': 'Error in user creation: ' + str(e)}), 500

#Elimina un usuario por su id 
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        #Buscamos al usuario por el ID
        user = User.query.get(id)
        if not user:
            return jsonify({'error':'User not found'}),404
        #Eliminamos al usuario
        db.session.delete(user)
        #Confirmamos  y subimos los cambios
        db.session.commit()
        return jsonify({'message':'User deleted successfully'}),200

    except Exception as e:
        return jsonify({'error':'Internal server error', 'message': str(e)}),500

#-----------------------------PERSONAJES--------------------------
#Obtiene todos los personajes
@app.route('/characters', methods=['GET'])
def get_characters():
    try:
        characters_results=Character.query.all()
        #print(characters_results)
        results = list(map(lambda item: item.serialize(), characters_results))
        #print(results)
        if results:    
            response_body = {
                "msg": "ok",
                "results": results,
            }
            return jsonify(response_body), 200
        return jsonify({'error':'Users not found'}),404

    except Exception as e:
        return jsonify({'error':'Internal server error', 'message': str(e)}),500
    
#Obtiene informacion de un solo personaje por su id    

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    print(character_id)#1
    try:
        query_character = Character.query.filter_by(id=character_id).first()
        print(query_character.serialize())
        if query_character is None:
            return jsonify({'error':'Character not found'}),404
        response_body = {
            "msg" : "ok",
            "result":query_character.serialize()
        }
        return jsonify(response_body),200
    except Exception as e:
        return jsonify({'error':'Internal server error', 'message': str(e)}),500

#Ruta POST new character  para crear nuevo personaje
@app.route('/characters', methods=['POST'])
def create_character():
    try:
        name = request.json.get('name')
        height = request.json.get('height')
        mass = request.json.get('mass')
        hair_color = request.json.get('hair_color')
        skin_color = request.json.get('skin_color')
        eye_color = request.json.get('eye_color')
        birth_year = request.json.get('birth_year')
        gender = request.json.get('gender')
        
        if not height or not mass or not name or not hair_color or not skin_color or not eye_color or not birth_year or not gender:
            return jsonify({'error': 'height, mass,hair_color,skin_color,eye_color, birth_year, gender  and Name are required.'}), 400

        existing_character= Character.query.filter_by(name=name).first()
        if existing_character:
            return jsonify({'error': 'Name already exists.'}), 409


        # Ensamblamos el personaje nuevo
        new_character = Character(height=height, mass=mass, hair_color=hair_color, skin_color=skin_color, eye_color=eye_color, birth_year=birth_year, gender=gender, name=name)

        db.session.add(new_character)
        db.session.commit()

        good_to_share_character = {
            'id': new_character.id,
            'name':new_character.name,
            'height':new_character.height,
            'mass': new_character.mass,
            'hair_color' : new_character.hair_color,
            'skin_color': new_character.skin_color,
            'eye_color' : new_character.eye_color,
            'birth_year': new_character.birth_year,
            'gender' : new_character.gender
        }

        return jsonify({'message': 'Character created successfully.','character_created':good_to_share_character}), 201

    except Exception as e:
        return jsonify({'error': 'Error in Character creation: ' + str(e)}), 500

#-----------------------------PLANETAS--------------------------
#Obtiene todos los planetas
@app.route('/planets', methods=['GET'])
def get_planets():
    try:
        planets_results = Planet.query.all()
        # print(planets_results)
        results = list(map(lambda item: item.serialize(), planets_results))
        # print(results)
        if results:
            response_body = {
                "msg": "ok",
                "results": results
            }
            return jsonify(response_body), 200
        return jsonify({'error': 'Planets not found'}), 404
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

#Obtiene informacion de un solo planeta
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    # print(planet_id)
    try:
        query_planet = Planet.query.filter_by(id = planet_id).first()
        # print(query_planet.serialize())
        if query_planet is None:
            return jsonify({'error': 'Planet not found'}), 404
        response_body = {
            "msg": "ok",
            "result": query_planet.serialize()
        }
        return jsonify(response_body), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

#-----------------------------VEHICULOS--------------------------
#Obtiene todos los vehiculos
@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    try:
        vehicles_results = Vehicle.query.all()
        # print(vehicles_results)
        results = list(map(lambda item: item.serialize(), vehicles_results))
        # print(results)
        if results:
            response_body = {
                "msg": "ok",
                "results": results
            }
            return jsonify(response_body), 200
        return jsonify({'error': 'Vehicles not found'}), 404
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500
    
#Obtiene informacion de un solo vehiculo
@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    # print(vehicle_id)
    try:
        query_vehicle = Vehicle.query.filter_by(id = vehicle_id).first()
        # print(query_vehicle.serialize())
        if query_vehicle is None:
            return jsonify({'error': 'Vehicle not found'}), 404
        response_body = {
            "msg": "ok",
            "result": query_vehicle.serialize()
        }
        return jsonify(response_body), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

#-----------------------------FAVORITOS--------------------------
#Obtiene todos los favoritos de un usuario segun su id
@app.route('/favorites/<int:user_id>')
def get_fav(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found. Please enter a valid user ID to view their favorites."}), 404
        
        fav_characters = FavoriteCharacter.query.filter_by(user_id = user_id).all()
        fav_planets = FavoritePlanet.query.filter_by(user_id = user_id).all()
        fav_vehicles = FavoriteVehicle.query.filter_by(user_id = user_id).all()
        # print(fav_characters)
        favorites_characters = list(map(lambda item: item.serialize(), fav_characters))
        favorites_planets = list(map(lambda item: item.serialize(), fav_planets))
        favorites_vehicles = list(map(lambda item: item.serialize(), fav_vehicles))
        # print(favorites_characters)

        if not favorites_characters and not favorites_planets and not favorites_vehicles:
            return jsonify({'message': 'Favorites not found'}), 404

        response_body = {
            "favorites_characters": favorites_characters,
            "favorites_planets": favorites_planets,
            "favorites_vehicles": favorites_vehicles
        }
        return jsonify(response_body), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

#Agregar personajes, planetas y vechiculos favoritos
@app.route('/favorites', methods=['POST'])
def add_favorite():
    try:
        # Obteniendo y guardando el id del body ingresado
        user_id_new = request.json.get("user_id")
        if not  user_id_new :
            return jsonify({"message":"Please enter a user ID"}), 400
        
        user = User.query.get(user_id_new)
        if not user:
            return jsonify({"error": "User not found. Please enter a valid user ID to view their favorites."}), 404
        
        character_id_new = request.json.get("character_id")
        planet_id_new = request.json.get("planet_id")
        vehicle_id_new = request.json.get("vehicle_id")
        
        if not character_id_new and not planet_id_new and not vehicle_id_new:
            return jsonify({'message': 'Favorite field not found'}), 404

        
        if character_id_new:
            #Creando y guardando un nuevo favorito
            new_fav = FavoriteCharacter(user_id = user_id_new, character_id = character_id_new)
            db.session.add(new_fav)
            db.session.commit()
            response_body = new_fav.serialize()
            return jsonify(response_body), 201
        
        elif planet_id_new:
            new_fav = FavoritePlanet(user_id = user_id_new, planet_id = planet_id_new)
            db.session.add(new_fav)
            db.session.commit()
            response_body = new_fav.serialize()
            return jsonify(response_body), 201
        
        elif vehicle_id_new:
            new_fav = FavoriteVehicle(user_id= user_id_new, vehicle_id=vehicle_id_new)
            db.session.add(new_fav)
            db.session.commit()
            response_body = new_fav.serialize()
            return jsonify(response_body), 201
        else:
            # Se mando un user id, pero no me mandaste que se debe favoritear
            return jsonify({"message":"You entered the user ID, but you haven't indicated which ID you want to mark as a favorite."}), 400

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

#Elimina un personaje favorito de cada usuario segun su id

@app.route('/favorites/character/<int:id_user>/<int:id_character>',methods =['DELETE'])
def delete_fav_character(id_user, id_character):
    try:
        #Primero verificamos que los id de usuario y de caracter existan para continuar con la busqueda
        user = User.query.get(id_user)
        character = Character.query.get(id_character)

        if not user or not character:
            return jsonify({"error": "The user or character does not exist. Please enter valid ID values."}), 404

        favorite_character = FavoriteCharacter.query.filter_by(user_id = id_user, character_id = id_character).first()
        if not favorite_character:
            return jsonify({'error': 'Character not found in their favorites'}), 404
        
        #Eliminando el favorito de la base de datos (db) 
        db.session.delete(favorite_character)
        db.session.commit()
        return jsonify({'message': 'Favorite character deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

#Elimina un planeta favorito de cada usuario segun su id
@app.route('/favorite/planet/<int:id_user>/<int:id_planet>', methods = ['DELETE'])
def delete_fav_planet(id_user, id_planet):
    try:
        user = User.query.get(id_user)
        planet = Planet.query.get(id_planet)
        if not user or not planet:
            return jsonify({"error": "The user or planet does not exist. Please enter valid ID values."}), 404
        
        favorite_planet = FavoritePlanet.query.filter_by(user_id = id_user, planet_id = id_planet).first()
        if not favorite_planet:
            return jsonify({'error':'Planet not found in their favorites'}), 404
        
        db.session.delete(favorite_planet)
        db.session.commit()
        return jsonify({'message': 'Favorite planet deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

#Elimina un vehiculo favorito de cada usuario segun su id
@app.route('/favorite/vehicle/<int:id_user>/<int:id_vehicle>', methods = ['DELETE'])
def delete_fav_vehicle(id_user, id_vehicle):
    try:
        user = User.query.get(id_user)
        vehicle = Vehicle.query.get(id_vehicle)
        if not user or not vehicle:
            return jsonify({"error": "The user or vehicle does not exist. Please enter valid ID values."}), 404

        favorite_vehicle = FavoriteVehicle.query.filter_by(user_id = id_user, vehicle_id = id_vehicle).first()
        if not favorite_vehicle:
            return jsonify({'error':'Vehicle not found in their favorites'}), 404
        
        db.session.delete(favorite_vehicle)
        db.session.commit()
        return jsonify({'message': 'Favorite vehicle deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
