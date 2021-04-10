from flask import (Blueprint, render_template, 
				   request, redirect, url_for, 
				   abort, flash, current_app)
from flask.views import MethodView
from ...pipelines import *

analyze_bp = Blueprint(
    'analyze_bp', __name__, template_folder='templates', url_prefix='/analyze')

class AnalyzeView(MethodView):

    template = 'analyze.html'

    def post(self):
        song_name = request.form['song_name']
        return render_template(self.template, song=song_name)

analyze_bp.add_url_rule('/', view_func=AnalyzeView.as_view('analyze'))