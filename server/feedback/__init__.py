from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
feedback_bp = Blueprint("feedback", __name__)

from . import routes  
