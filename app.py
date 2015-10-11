import flask

import os

import reversedict

app = flask.Flask(__name__)

@app.route('/')
def instruction():
    return flask.jsonify(how_to='GET request to /lookup/{description}/ or POST to /lookup/ with parameter `description`.',
                         tip='You can laso use `pos` argument to define part-of-speech of the intended word.')

@app.route('/lookup/', methods=['GET','POST'])
@app.route('/lookup/<description>/')
def reversedict_lookup(description=None):
    description = description or flask.request.form.get('description')
    if not description:
        return flask.redirect(flask.url_for('instruction'))
    pos = flask.request.args.get('pos')
    results = reversedict.lookup(description, 
                                 pos=pos,
                                 verbose=True)
    return flask.jsonify(suggestions=results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', 
            debug=True,
            port=int(os.environ.get('PORT') or 5000))
    