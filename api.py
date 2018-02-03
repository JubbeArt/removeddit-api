import falcon
import BannedSubreddits

app = falcon.API()
app.add_route('/route/banned', BannedSubreddits())