from flask_restful import reqparse, abort, Resource

class getEverythingLeague(Resource):
	'''get all information based on league'''
	@staticmethod
	def get(cur, LID):
		""" 
        Args:
            lid (int) : the ID of the league

        Returns:
			"All information about the league"
        """
		cur.execute("SELECT userprefs.friends, userprefs.email, userprefs.messages, userprefs.notifications, userprefs.username, userprefs.imageurl, userprefs.vip, userprefs.description, players.pid, players.uid, players.lid, players.holdings, players.notifications, players.availbalance, players.pendingorders, players.translog, players.reppoints FROM players INNER JOIN userprefs ON players.uid = userprefs.uid WHERE players.lid = %s ORDER BY reppoints DESC;", (LID,))
		return cur.fetchall()
