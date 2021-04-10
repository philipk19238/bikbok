from flask import (Blueprint, render_template, 
				   request, redirect, url_for, 
				   abort, flash, current_app)
from flask.views import MethodView
from ...pipelines import *

analyze_bp = Blueprint(
    'analyze_bp', __name__, template_folder='templates', url_prefix='/analyze')

top_song_ids = get_top_songs()
genre_vectors = generate_genre_vectors(top_song_ids)

class AnalyzeView(MethodView):

    template = 'analyze.html'

    def post(self):
        song_id = request.form['song_id']
        song = generate_vector(song_id)
        similarity = genre_similarity(song, top_song_ids)
        return render_template(self.template, song=song_id, similarity=similarity)

analyze_bp.add_url_rule('/', view_func=AnalyzeView.as_view('analyze'))