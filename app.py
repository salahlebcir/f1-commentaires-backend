#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 12 13:52:13 2025

@author: slebcir
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, User, Comment
import hashlib
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/")
def hello():
    return "Serveur commentaires actif ✅"

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    pseudo = data.get("pseudo")
    password = data.get("password")

    if not pseudo or not password:
        return jsonify({"error": "Champs requis"}), 400

    existing_user = User.query.filter_by(pseudo=pseudo).first()
    if existing_user:
        return jsonify({"error": "Pseudo déjà pris"}), 409

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    new_user = User(pseudo=pseudo, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Compte créé avec succès"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    pseudo = data.get("pseudo")
    password = data.get("password")

    if not pseudo or not password:
        return jsonify({"error": "Champs requis"}), 400

    user = User.query.filter_by(pseudo=pseudo).first()
    if not user:
        return jsonify({"error": "Pseudo inconnu"}), 404

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if user.password_hash != hashed_password:
        return jsonify({"error": "Mot de passe incorrect"}), 401

    return jsonify({"message": "Connexion réussie", "pseudo": pseudo}), 200

@app.route("/comments", methods=["POST"])
def add_comment():
    data = request.get_json()
    auteur = data.get("auteur")
    contenu = data.get("contenu")
    type_graphique = data.get("type_graphique")
    grand_prix = data.get("grand_prix")
    cible = data.get("cible")

    if not all([auteur, contenu, type_graphique, grand_prix]):
        return jsonify({"error": "Champs manquants"}), 400

    timestamp = datetime.utcnow().isoformat()
    new_comment = Comment(
        auteur=auteur,
        contenu=contenu,
        timestamp=timestamp,
        type_graphique=type_graphique,
        grand_prix=grand_prix,
        cible=cible
    )
    db.session.add(new_comment)
    db.session.commit()

    return jsonify({"message": "Commentaire ajouté"}), 201

@app.route("/comments", methods=["GET"])
def get_comments():
    type_graphique = request.args.get("type")
    grand_prix = request.args.get("gp")
    cible = request.args.get("cible")

    if not type_graphique or not grand_prix:
        return jsonify({"error": "Paramètres requis"}), 400

    query = Comment.query.filter_by(
        type_graphique=type_graphique,
        grand_prix=grand_prix
    )
    if cible:
        query = query.filter_by(cible=cible)

    comments = query.order_by(Comment.timestamp.desc()).all()
    result = []
    for c in comments:
        result.append({
            "auteur": c.auteur,
            "contenu": c.contenu,
            "timestamp": c.timestamp
        })

    return jsonify(result), 200

def create_app():
    with app.app_context():
        db.create_all()
    return app

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()   # ⚠️ À retirer une fois tout fonctionne
        db.create_all()
        
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

