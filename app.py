"""Servidor local CSV/XLSX. SPDX-License-Identifier: AGPL-3.0-only."""
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory
from planner import parse_file, plan
ROOT=Path(__file__).resolve().parent
def create_app():
    app=Flask(__name__,static_folder=None)
    app.config.update(MAX_CONTENT_LENGTH=2_100_000,TRUSTED_HOSTS=['localhost','127.0.0.1'])
    @app.get('/')
    def home():return send_from_directory(ROOT/'public','index.html')
    @app.get('/<path:name>')
    def asset(name):return send_from_directory(ROOT/'public',name)
    @app.get('/health')
    def health():return jsonify(status='ok',version='2.0.0')
    @app.post('/api/plan')
    def calculate():
        origin=request.headers.get('Origin')
        if origin and origin!=request.host_url.rstrip('/'):return jsonify(error='Origen no permitido.'),403
        upload=request.files.get('file')
        if not upload or not upload.filename:return jsonify(error='Adjunta un CSV o XLSX.'),400
        try:
            count=int(request.form.get('routes','1'))
            points=parse_file(upload.read(),upload.filename)
            routes=plan(points,count)
        except (ValueError,KeyError,IndexError) as error:return jsonify(error=str(error)),400
        return jsonify(routes=routes,distance='km geodésicos, sin carreteras ni tráfico')
    @app.errorhandler(413)
    def too_large(error):return jsonify(error='Límite de archivo: 2 MB.'),413
    @app.after_request
    def headers(response):
        response.headers['X-Content-Type-Options']='nosniff'
        response.headers['Cache-Control']='no-store'
        response.headers['Content-Security-Policy']="default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; object-src 'none'; base-uri 'none'; frame-ancestors 'none'"
        return response
    return app
app=create_app()
if __name__=='__main__':app.run(host='127.0.0.1',debug=False)
