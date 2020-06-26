from flask_restful import Resource,reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,jwt_required
from db import query

class Seminars(Resource):
    @jwt_required
    def get(self):
        try:
            return query(f"""SELECT * FROM timetable.seminars WHERE availibility='0'""")
        except:
            return {"message":"there was an error retrieving the data"},500

    @jwt_required
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('user_id',type=int,required=True,help="User_id name cannot be left blank!")
        parser.add_argument('room_id',type=int,required=True,help="room_id cannot be left blank!")
        parser.add_argument('club_name',type=str,required=True,help="club_name cannot be left blank!")
        parser.add_argument('purpose',type=str,required=True,help="fine can't be left blank!")
        data=parser.parse_args()
        try:
            query(f"""INSERT INTO timetable.requests(user_id, room_id, club_name, purpose, req_status)
                                VALUES({data['user_id']},{data['room_id']},'{data['club_name']}',
                                            '{data['purpose']}','pending')""")
        except:
            return {"message": "An error occurred."}, 500
        return {"message": "successfully added request."}, 201
            
    
class RequestStatus(Resource):
    
    @jwt_required
    def get(self):
        try:
            return query(f"""SELECT * FROM timetable.requests WHERE req_status='pending'""")
        except:
            return {"message":"There was an error displaying the data"},500

    @jwt_required
    def put(self):
        parser=reqparse.RequestParser()
        parser.add_argument('user_id',type=int,required=True,help="please give reg_id")
        data=parser.parse_args()
        try:
            query(f"""UPDATE timetable.requests SET req_status='Approved' WHERE user_id={data['user_id']}""")
        except:
            return {"message":"there was an error updating the req_status"},500
        return {"message":"successfully updated"},201