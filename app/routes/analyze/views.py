from flask import (Blueprint, render_template, 
				   request, redirect, url_for, 
				   abort, flash, current_app)
from flask.views import MethodView

analyze_bp = Blueprint(
    'analyze_bp', __name__, template_folder='templates', url_prefix='/analyze')

    