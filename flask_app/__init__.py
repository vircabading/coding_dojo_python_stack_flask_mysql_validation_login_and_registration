# ///////////////////////////////////////////////////////////////////
# __init__
# ///////////////////////////////////////////////////////////////////

from flask import Flask, session


app = Flask(__name__)
app.secret_key = "TiYSKDNRitA!"                                         # This is Your Secret Key Do Not Reveal it to Anyone!