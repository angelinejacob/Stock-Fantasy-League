from flask_restful import reqparse, abort, Resource

class joinLeague(Resource):

    @staticmethod   #method to join a league
    def post(cur, UID):

        parser = reqparse.RequestParser()
        parser.add_argument('lid') #important just so database knows which lid to put uid in (remember this is joinLeague not createLeague)
        args = parser.parse_args()

        cur.execute("INSERT INTO players (uid) VALUES (%s);", [UID])
        cur.execute("SELECT pid FROM players WHERE uid=%s;", [UID])
        createdPID = cur.fetchall()
        cur.execute("UPDATE leagues SET pid = pid  || %s WHERE lid = %s;", (createdPID[-1]['pid'], args['lid']))
        cur.execute("UPDATE userprefs SET pid = pid || %s WHERE uid = %s;", (createdPID[-1]['pid'], UID))
        cur.execute("UPDATE leagues SET uid = uid || %s WHERE lid = %s;", ([UID], args['lid'])) 
        cur.execute("UPDATE userprefs SET lid = lid || %s WHERE uid = %s;", ([int(args['lid'])], UID))
        cur.execute("UPDATE players SET lid = %s WHERE pid = %s;", ((args['lid']), createdPID[-1]['pid']))

        """
        Achievment Code:
        
        cur.execute("SELECT ticker FROM userprefs WHERE uid = %s", [UID])
        tickerVal = cur.fetchone();
        
        if tickerVal == 0
            println("Achievement Unlocked:\n" + "Join a League!\n" + "Points Earned: 5")
        """

        return createdPID
        pass