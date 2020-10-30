from flask import Flask, render_template, redirect, flash, url_for
from forms import PokemonSubmissionForm, LoginForm
app = Flask(__name__)
app.config['SECRET_KEY'] = 'tepiglover'

'''
TODO: 
This method is to use the Pokemon Prediction Model Brad or Jennifer used to predict
the winner of the pokemon battle

Their model may not rely on the actual names of the pokemon, so you will have to do some
manipulation on your end, shouldn't be too bad though.

The output should be the name of the winning pokemon, currently returning Pikachu as 
a dummy value
'''

def predict(pokemon1, pokemon2):
    return 'Pikachu'

@app.route("/", methods=["GET","POST"])
@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('home', username=form.username.data))
    return render_template('login.html', form=form)

@app.route("/home/<username>", methods=["GET", "POST"])
def home(username):
    winner = ''
    form = PokemonSubmissionForm()
    if form.validate_on_submit():
        winner = predict(form.pokemon1.data, form.pokemon2.data)
    return render_template("home.html", form=form, user=username, winner=winner)

if __name__ == "__main__":
    app.run(debug=True)