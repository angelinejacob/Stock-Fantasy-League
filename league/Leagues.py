from flask_restful import reqparse, abort, Resource
import json

class Leagues(Resource):

    @staticmethod  # getAllLeaguesInfo
    def get(cur):
        cur.execute("select lid,uid,pid,startbal,leaguename,description,owneruid,ownerpid,type from leagues;")

        #leagues = cur.fetchall()
        return json.dumps({"Leagues": cur.fetchall()})
        #return "{'leagues':" + str(leagues) + "}"


        # returning all json strings as one large json string


