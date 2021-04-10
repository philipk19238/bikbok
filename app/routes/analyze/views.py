from flask import (Blueprint, render_template, 
				   request, redirect, url_for, 
				   abort, flash, current_app)
from flask.views import MethodView
from ...pipelines import *

analyze_bp = Blueprint(
    'analyze_bp', __name__, template_folder='templates', url_prefix='/analyze')

top_songs = get_top_songs()
genre_vectors = generate_genre_vectors()

class AnalyzeView(MethodView):

    template = 'analyze.html'

    def post(self):
        song_id = request.form['song_id']
        song = generate_vector()
        similarity = genre_similarity(song, top_songs)
        return render_template(self.template, song=song_id)

analyze_bp.add_url_rule('/', view_func=AnalyzeView.as_view('analyze'))