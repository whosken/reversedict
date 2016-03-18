import flask

import os

import reversedict

app = flask.Flask(__name__)

@app.route('/api/instructions')
def instruction():
    return flask.jsonify(how_to='GET request to /lookup/{description}/ or POST to /lookup/ with parameter `description`.',
                         tip='You can also use `synonyms` parameter or `synonym` arguments to filter the candidates.')

@app.route('/api/lookup/', methods=['GET','POST'])
@app.route('/api/lookup/<description>/')
def reversedict_lookup(description=None):
    description = description or flask.request.form.get('description')
    if not description:
        return flask.redirect(flask.url_for('instruction'))
    synonyms = flask.request.form.get('synonyms') or flask.request.args.getlist('synonym')
    results = reversedict.lookup(description, synonyms)
    return flask.jsonify(suggestions=results)


@app.route('/')
@app.route('/<description>')
def index(description=None):
    return flask.render_template('index.html', description=description)

@app.route('/js/<path:file_path>')
def send_js(file_path):
    return flask.send_from_directory('static/js', file_path)

@app.route('/css/<path:file_path>')
def send_css(file_path):
    return flask.send_from_directory('static/css', file_path)

@app.route('/img/<path:file_path>')
def send_img(file_path):
    return flask.send_from_directory('static/img', file_path)

@app.route('/font-awesome/<path:file_path>')
def send_font_awesome(file_path):
    return flask.send_from_directory('static/font-awesome', file_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', 
            debug=True,
            port=int(os.environ.get('PORT') or 5000))
    