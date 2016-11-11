import time
import datetime

# post_time is an int in Unix time format
# returns a string with the timestamp of the post
# with different formats depending on how long ago the post was made
def timestamp(post_time):
    curr_time = int(time.time())
    diff = curr_time - post_time
    if (diff < 60):
        return "1 second ago" if diff==1 else "%d seconds ago"%(diff)
    
    diff = diff/60 #num of minutes
    if (diff < 60):
        return "1 minute ago" if diff==1 else "%d minutes ago"%(diff)

    diff = diff/60 #num of hours
    if (diff < 24):
        return "1 hour ago" if diff==1 else "%d hours ago"%(diff)

    diff = diff/24 #num of days
    if (diff < 2):
        return "yesterday"

    return "on %s"%(datetime.datetime.fromtimestamp(post_time).strftime('%B %d'))

