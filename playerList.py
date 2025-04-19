# -*- coding: utf-8 -*-
"""
Created on Sat Apr 19 12:53:22 2025

@author: Rushi
"""

from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, auth, firestore

# Initialize Firebase Admin SDK
import os, json
firebase_key_json = os.getenv("FIREBASE_KEY")
cred = credentials.Certificate(json.loads(firebase_key_json))

firebase_admin.initialize_app(cred)
db = firestore.client()

app = FastAPI()

db = firestore.client()

# List all root-level collections
collections = db.collections()

@app.get("/all-players")
def get_all_players():
    docs = db.collection("user").where("userType", "==", "Player").stream()

    player_names = []
    for doc in docs:
        data = doc.to_dict()
        name = data.get("display_name")
        if name:
            player_names.append(name.strip())

    return {"players": sorted(player_names)}
