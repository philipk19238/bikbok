from flask import (Blueprint, render_template, 
				   request, redirect, url_for, 
				   abort, flash, current_app)
from flask.views import MethodView

landing_bp = Blueprint(
    'landing_bp', __name__, template_folder='templates')

class LandingView(MethodView):

    template = 'landing.html'

    def get(self):
        return render_template(self.template)

landing_bp.add_url_rule('/', view_func=LandingView.as_view('landing'))