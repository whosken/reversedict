import flask

import os

import reversedict

app = flask.Flask(__name__)

@app.route('/lookup/', methods=['GET','POST'])
@app.route('/lookup/<description>/')
def reversedict_lookup(description=None):
    if not description:
        description = flask.request.form['description']
    pos = flask.request.args.get('pos')
    results = reversedict.lookup(description, 
                                 pos=pos,
                                 verbose=True)
    return flask.jsonify(suggestions=results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT') or 5000))
