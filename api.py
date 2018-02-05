import falcon
#import BannedSubreddits
import RemovedThreads

app = falcon.API()
#app.add_route('/route/banned', BannedSubreddits())
app.add_route('/api/threads', RemovedThreads.RemovedThreads())