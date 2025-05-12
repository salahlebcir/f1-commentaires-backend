#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 12 15:08:54 2025

@author: slebcir
"""

from app import app, db
from models import Comment

with app.app_context():
    db.session.query(Comment).delete()
    db.session.commit()
    print("✅ Tous les commentaires ont été supprimés.")
