#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 12 13:52:42 2025

@author: slebcir
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pseudo = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auteur = db.Column(db.String(100), nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.String(100), nullable=False)
    type_graphique = db.Column(db.String(50), nullable=False)
    grand_prix = db.Column(db.String(100), nullable=False)
    cible = db.Column(db.String(100))
