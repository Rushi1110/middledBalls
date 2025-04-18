# -*- coding: utf-8 -*-
"""
Created on Sat Apr 19 01:50:57 2025

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

@app.get("/middled-stats/{batter_name}")
def get_middled_stats(batter_name: str):
    docs = db.collection("ball_ID").where("batterName", "==", batter_name).stream()

    total = 0
    middled = 0

    for doc in docs:
        data = doc.to_dict()
        total += 1
        if data.get("batLength", "").strip().lower() == "middle":
            middled += 1

    return {
        "batter": batter_name,
        "total_balls": total,
        "middled_balls": middled
    }
