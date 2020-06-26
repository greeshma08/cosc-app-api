from flask_restful import Resource,reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,jwt_required
from db import query

class Labs(Resource):
    @jwt_required
    def get(self):
        try:
            return query(f"""SELECT * FROM timetable.labs WHERE availibility='0'""")
        except:
            return {"message":"there was an error retrieving the data"},500

    @jwt_required
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('user_id',type=int,required=True,help="User_id name cannot be left blank!")
        parser.add_argument('room_id',type=int, required=True,help="lab number cannot be left blank!")
        parser.add_argument('purpose',type=str,required=True,help="purpose can't be left blank!")
        data=parser.parse_args()
        try:
            query(f"""INSERT INTO timetable.REQUESTS(user_id, room_id, purpose, req_status)
                                VALUES({data['user_id']},{data['room_id']},
                                            '{data['purpose']}','pending')""")
        except:
            return {"message": "An error occurred."}, 500
        return {"message": "successfully added request."}, 201