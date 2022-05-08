# Imports
init -20 python:

    # Database Interaction
    import pymongo

    # pymongo dependency for mongodb+srv protocol
    # import dnspython 

    # Connection stuff
    import ssl
    import urllib

# Datetime stuff
init -16 python:

    import datetime

    # Uses strftime to convert datetime object into a string
    def timeToStr(timeGiven):
        return timeGiven.strftime("%A %d, %H:%M:%S")

    # Uses strptime to convert string into a datetime object 
    def strToTime(stringGiven):
        return datetime.strptime(stringGiven, "%A %d, %H:%M:%S")

# Chat and Message Class
init -15 python:

    # Core class.
    # channel - a string, name of a collection in the database
    class Chat():

        def __init__(self, channel):

            self.channel = channel
            self.messages = []

    # Message class.
    # author - string, nick of the sender
    # content - string, content of the message
    # time - datetime object of sending # TODO: Maybe could be defined inside the __init__ directly?
    class Message():

        def __init__(self, author, content, time):

            self.author = author
            self.content = content
            self.time = time

        # Transforms the object into a dict that can be inserted into a collection.
        def toDocument(self):

            return { "author" : self.author,
            "content" : self.content,
            "time" : timeToStr(self.time)
            }

    # Creates a Message object from a document from a collection.
    def MessageFromDocument(self, doc):

        return Message( doc["author"], doc["content"], strToTime(doc["time"]) )


# Test
init python:

    # Variable that runs the test.
    testItOut = True 

    # Connection info
    connectionProtocol = "mongodb+srv"
    userName = "doadmin"
    userPass = open("pass.txt").read()
    hostName = "db-mongodb-lon1-02074-eea89e0c.mongo.ondigitalocean.com"

    # URI put together
    uri = "{}://{}:{}@{}".format( connectionProtocol, urllib.quote_plus(userName) , urllib.quote_plus(userPass) , hostName )

    # Connecting
    dbClient = pymongo.MongoClient( uri, ssl_cert_reqs= ssl.CERT_NONE )

    print("I successfully connected!")

    # Inside
    mainDatabase = dbClient.client["admin"]
    mainCollection = mainDatabase["MyCollection"]

    # Insert example
    a = Message("Karen", "I like birds!", datetime.datetime.now())

    # Can be used once to try inserting something.
    if testItOut:

        mainCollection.insert_one( a.toDocument() )

# Whole thing was tested through a terminal with this query (also in query.txt):

# >>> import pymongo
# >>> import ssl
# >>> import urllib
# >>> connectionProtocol = "mongodb+srv"
# >>> userName = "doadmin"
# >>> userPass = "od3x8it52qQ047I9"
# >>> hostName = "db-mongodb-lon1-02074-eea89e0c.mongo.ondigitalocean.com"
# >>> uri = "{}://{}:{}@{}".format( connectionProtocol, urllib.quote_plus(userName) , urllib.quote_plus(userPass) , hostName )
# >>> dbClient = pymongo.MongoClient( uri, ssl_cert_reqs= ssl.CERT_NONE )
# >>> mainDatabase = dbClient.client["admin"]
# >>> mainCollection = mainDatabase["MyCollection"]
# >>> for result in mainCollection.find():
# ...     print(result)

# {u'_id': 0, u'string': u'one'}
# {u'_id': 1, u'string': u'two'}
# {u'_id': 2, u'string': u'three'}
# {u'_id': 3, u'string': u'four'}

label start:

    return