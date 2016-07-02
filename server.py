import json
import os

from flask import Flask, render_template, request, make_response
from sys import argv

from app import build_app
from models import db, connect_to_db, Invite, Guest

app = build_app(__name__)
DEBUG = 'PROD' not in os.environ
PORT = os.environ.get('PORT', 5000)


@app.route("/")
def home():
    invite_code = request.cookies.get("conWedInvCode", "")
    return render_template("main.html", invite_code=invite_code)

@app.route("/invite-code/", methods=["POST"])
def invite_code():
    code = request.form["code"]
    matching_invite = Invite.validate(code)

    if matching_invite:
        resp = {"ok": True}
    else:
        resp = {"error": "Invalid Code"}

    return json.dumps(resp)

@app.route("/rsvp/", methods=["POST"])
def rsvp():
    code = request.form["inviteCode"]
    invite = Invite.validate(code)
    if not invite:
        return false

    attending = request.form["attending"]
    guest = Guest(invite_id=invite.id)
    return attending

if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=DEBUG, host='0.0.0.0', port=PORT)
