import copy

from flask import Flask, request
from flask import jsonify
from flask_pymongo import PyMongo
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# db_host = '0.0.0.0'
db_host = 'mongo'

app.config["MONGO_URI"] = f"mongodb://{db_host}:27017/fms"
mongo = PyMongo(app)


class Cars(Resource):
    @staticmethod
    def get(car_id):
        result = mongo.db.cars.find_one({"car_id": car_id})
        if not result:
            return {'error': 'Car does not exists.'}
        else:
            return {'result': {'car_id': result['car_id'], 'driver_id': result['driver_id']}}

    @staticmethod
    def post(car_id):
        driver_id = request.form.get('driver_id')
        result = mongo.db.cars.find_one({"car_id": car_id})
        if result:
            return {'error': 'This car already exists.'}
        car = {'car_id': car_id}
        if driver_id:
            car.update({'driver_id': driver_id})
        mongo.db.cars.insert(copy.deepcopy(car))
        return {'result': car}

    @staticmethod
    def patch(car_id):
        if 'driver_id' in request.form:
            car = {'car_id': car_id, 'driver_id': request.form['driver_id']}
            result = mongo.db.cars.update({"car_id": car_id}, copy.deepcopy(car))
            if not result['n']:
                return {'error': 'Car does not exists.'}
            return {'result': car}
        else:
            return {'error': 'No data for update.'}

    @staticmethod
    def delete(car_id):
        result = mongo.db.cars.delete_one({"car_id": car_id})
        return {'result': {'deleted': result.deleted_count}}


api.add_resource(Cars, '/cars/<string:car_id>')


@app.route('/assign', methods=['POST'])
def assign():
    driver_id = request.form.get('driver_id')
    car_id = request.form.get('car_id')
    if driver_id and car_id:
        mongo.db.cars.update(
            {'car_id': car_id},
            {'$set': {'driver_id': driver_id}},
            upsert=True
        )
        return jsonify({'result': {"car_id": car_id, "driver_id": driver_id}})
    else:
        return jsonify({'error': 'Use driver_id and car_id in query params.'})


@app.route('/drivers', methods=['GET'])
def drivers():
    driver_id = request.args.get('driver_id')
    return jsonify({'result': [
        {'driver_id': x['driver_id'], 'penalty': x['penalty']}
        for x in mongo.db.drivers.find(
            {"driver_id": driver_id} if driver_id else {}
        )
    ]})


@app.route('/cars', methods=['GET'])
def fleet():
    car_id = request.args.get('car_id')
    return jsonify({'result': [
        {'car_id': x['car_id'], 'driver_id': x['driver_id']}
        for x in mongo.db.cars.find(
            {"car_id": car_id} if car_id else {}
        )
    ]})


if __name__ == "__main__":
    app.run(host='0.0.0.0')
