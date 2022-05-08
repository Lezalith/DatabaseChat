# Imports
init -1 python:

    # Database Interaction
    import pymongo

    # pymongo dependency for mongodb+srv protocol
    # import dnspython 

    # Connection stuff
    import ssl
    import urllib

    def getPassword():
        return open("pass.txt").read()

# Test
init python:

    # Variable that runs the test.
    testItOut = False 

    # Connection info
    connectionProtocol = "mongodb+srv"
    userName = "doadmin"
    userPass = getPassword()
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
    toBeInserted = []
    
    for i, x in enumerate(["one", "two", "three", "four"]):

        toBeInserted.append( {"_id" : i, "string" : x} )

    # Can be used once to try inserting something.
    if testItOut:

        mainCollection.insert_many(toBeInserted)

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