from hashlib import md5
from flask import Flask, jsonify, request
from flask.views import MethodView
from storage_db.storage_db import DbClient, Advertisement, User


PG_DSN = 'postgresql://postgres:postgres@127.0.0.1:5431/netology'
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
db_client = DbClient(PG_DSN)


class AdvertisementApiClient(MethodView):
    def get(self):
        id_advertisement = request.args.get('id')
        if not id_advertisement:
            advertisements = db_client.session.query(Advertisement).all()
            advertisements = [{'id': advertisement.id, 'description': advertisement.description, 'create_date':
                              advertisement.create_date, 'owner_id': advertisement.owner_id} for advertisement
                              in advertisements]
            db_client.session.close()
            return jsonify(advertisements)

        try:
            advertisement = db_client.session.query(Advertisement).filter(
                Advertisement.id == id_advertisement
            ).first()
            advertisement = {'id': advertisement.id, 'description': advertisement.description, 'create_date':
                             advertisement.create_date, 'owner_id': advertisement.owner_id}
        except AttributeError:
            response = jsonify({'result': 'There is no ad with the specified id'})
            response.status_code = 404
            return response
        db_client.session.close()
        return jsonify(advertisement)

    def post(self):
        advertisement_data = request.get_json()
        data_for_db = Advertisement(description=advertisement_data['description'],
                                    owner_id=advertisement_data['owner_id'])
        db_client.session.add(data_for_db)
        db_client.session.commit()
        db_client.session.close()
        response = jsonify()
        response.status_code = 201
        return response

    def delete(self):
        id_advertisement = request.args.get('id')
        if not id_advertisement:
            advertisements = db_client.session.query(Advertisement).delete(synchronize_session='fetch')
            db_client.session.commit()
            db_client.session.close()
            return jsonify()
        advertisement = db_client.session.query(Advertisement).filter(
            Advertisement.id == id_advertisement
        ).first()
        db_client.session.delete(advertisement)
        db_client.session.commit()
        db_client.session.close()
        return jsonify()


class UserApiClient(MethodView):
    def post(self):
        user_data = request.get_json()
        user_name = user_data['name']
        user_password = str(md5(user_data['password'].encode()).hexdigest())
        data_for_db = User(name=user_name, password=user_password)
        db_client.session.add(data_for_db)
        db_client.session.commit()
        db_client.session.close()
        response = jsonify()
        response.status_code = 201
        return response

    def get(self):
        id_user = request.args.get('id')
        if not id_user:
            users = db_client.session.query(User).all()
            users = [{'id': user.id, 'name': user.name} for user in users]
            db_client.session.close()
            return jsonify(users)


app.add_url_rule('/api/advertisements/', view_func=AdvertisementApiClient.as_view('advertisements'),
                 methods=['GET', 'POST', 'DELETE'])
app.add_url_rule('/api/users/', view_func=UserApiClient.as_view('users'), methods=['GET', 'POST'])

if __name__ == "__main__":
    app.run(host='0.0.0.0')
