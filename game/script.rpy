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

    # TODO: Inaccurate day display, because of only partial data.
    # Given time of:
    # 2022-05-10 00:15:32.957221
    # Running it through timeToStr and back through strToTime results in:
    # 1900-01-10 00:15:32

    # Uses strftime to convert datetime object into a string
    def timeToStr(timeGiven):
        return timeGiven.strftime("%A %d, %H:%M:%S")

    # Uses strptime to convert string into a datetime object 
    def strToTime(stringGiven):
        return datetime.datetime.strptime(stringGiven, "%A %d, %H:%M:%S")

# Chat and Message Class
init -15 python:

    # Core class.
    # channel - a string, name of a collection in the database
    class Chat():

        def __init__(self, channel):

            self.channel = channel
            self.messages = []

        def pullAllMessages(self):

            allDocs = [doc for doc in store.mainCollection.find()]

            messages = []

            for doc in allDocs:

                messages.append( MessageFromDocument(doc) )

            return messages

        def reloadMessages(self):

            self.messages = self.pullAllMessages()

        # Add a message to database and my own messages
        def sendMessage(self, content):

            # TODO: Currently static author.
            message = Message( "Static Author", content, datetime.datetime.now() )

            self.messages.append(message)

            mainCollection.insert_one( message.toDocument() )

        # Clear the database and all my own messages.
        def clear(self):

            self.messages = []

            mainCollection.drop()



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

        def __str__(self):
            return "{} - {}: {}".format( timeToStr(self.time), self.author, self.content )

    # Creates a Message object from a document from a collection.
    def MessageFromDocument(doc):

        return Message( doc["author"], doc["content"], strToTime(doc["time"]) )

# Same name as the collection chosen inside the database.
default mainChat = Chat("mainChannel")

# Test
init python:

    # Variable that runs the test.
    testItOut = True 

    # Connection info
    connectionProtocol = "mongodb+srv"
    userName = "ChatClient"
    userPass = open("pass.txt").read()
    hostName = "db-mongodb-lon1-02074-eea89e0c.mongo.ondigitalocean.com"

    # URI put together
    uri = "{}://{}:{}@{}".format( connectionProtocol, urllib.quote_plus(userName) , urllib.quote_plus(userPass) , hostName )

    # Connecting
    # TODO: This reeeallly might need to get defaulted.
    dbClient = pymongo.MongoClient( uri, ssl_cert_reqs= ssl.CERT_NONE )

    print("I successfully connected!")

    # Inside
    mainDatabase = dbClient.client["ChatDatabase"]
    mainCollection = mainDatabase["mainChannel"]

    # Insert example
    a = Message("Meep", "Gimme lettuce.", datetime.datetime.now())

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

screen chatScreen():

    # Chat frame
    frame:

        align (0.5, 0.5)
        xysize (1060, 500)
        yoffset -80

        vbox:

            xalign 0.5
            spacing 15

            for message in mainChat.messages:

                text str(message)

    default messageInput = "Default of the message."

    frame:

        align (0.5, 1.0)
        offset (-100, -90)
        xysize (860, 70)

        input:
            value ScreenVariableInputValue("messageInput")
            pixel_width 800

    textbutton "Send":

        background Solid("ddd")

        align (0.5, 1.0)
        offset (460, -90)
        xysize (140, 70)
        text_align (0.5, 0.5)

        action Function(mainChat.sendMessage, messageInput), SetScreenVariable("messageInput", "Default of the message.")

    # Buttons
    hbox:

        align (0.5, 0.9)
        yoffset 30
        spacing 50

        textbutton "Reload messages.":
            action Function(mainChat.reloadMessages)

        textbutton "Clear the chat.":
            action Function(mainChat.clear)

label start:

    call screen chatScreen

    return