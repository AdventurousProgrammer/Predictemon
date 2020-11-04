from flask import Flask, render_template, redirect, flash, url_for, request
from forms import PokemonSubmissionForm, LoginForm

import pandas as pd
import math
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import tensorflow
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.metrics import Accuracy
import pickle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tepiglover'

'''
TODO: 
This method is to use the Pokemon Prediction Model Brad or Julia used to predict
the winner of the pokemon battle

Their model may not rely on the actual names of the pokemon, so you will have to do some
manipulation on your end, shouldn't be too bad though.

The output should be the name of the winning pokemon, currently returning Pikachu as 
a dummy value
'''

def predict(pokemon1, pokemon2):
    return 'Pikachu'

def get_types(pkmn1, pkmn2):
    Types = ['Normal', 'Fight', 'Flying', 'Poison', 'Ground', 'Rock', 'Bug', 'Ghost', 'Steel', 'Fire', 'Water', 'Grass', 'Electric', 'Psychic', 'Ice', 'Dragon', 'Dark', 'Fairy', 'None']
    pkmn1_type = []
    pkmn2_type = []
    # Determine Type 1 of Pokemon 1
    for i in range (0, 19):
        answer = (pkmn1["Type 1"] == Types[i])
        if answer.bool():
            pkmn1_type.append(Types[i])
            
    # Determine Type 1 of Pokemon 2
    for i in range (0, 19):
        answer = (pkmn2["Type 1"] == Types[i])
        if answer.bool():
            pkmn2_type.append(Types[i])
    
    # Determine Type 2 of Pokemon 1
    for i in range (0, 19):
        answer = (pkmn1["Type 2"] == Types[i])
        if answer.bool():
            pkmn1_type.append(Types[i])
            break
        else :
            pkmn1_type.append("None")
    
    # Determine Type 2 of Pokemon 2
    for i in range (0, 19):
        answer = (pkmn2["Type 2"] == Types[i])
        if answer.bool():
            pkmn2_type.append(Types[i])
            break
        else :
            pkmn2_type.append("None")
        
    print("Pokemon 1 Type 1:", pkmn1_type[0], '\n')
    print("Pokemon 1 Type 2:", pkmn1_type[1], '\n')
    print("Pokemon 2 Type 1:", pkmn2_type[0], '\n')
    print("Pokemon 2 Type 2:", pkmn2_type[1], '\n')

    very_effective_dict = {'Normal': [],
                           'Fight': ['Normal', 'Rock', 'Steel', 'Ice', 'Dark'],
                           'Flying': ['Fight', 'Bug', 'Grass'],
                           'Poison': ['Grass', 'Fairy'],
                           'Ground': ['Poison', 'Rock', 'Steel', 'Fire', 'Electric'],
                           'Rock': ['Flying', 'Bug', 'Fire', 'Ice'],
                           'Bug': ['Grass', 'Psychic', 'Dark'],
                           'Ghost': ['Ghost', 'Psychic'],
                           'Steel': ['Rock', 'Ice', 'Fairy'],
                           'Fire': ['Bug', 'Steel', 'Grass', 'Ice'],
                           'Water': ['Ground', 'Rock', 'Fire'],
                           'Grass': ['Ground', 'Rock', 'Water'],
                           'Electric': ['Flying', 'Water'],
                           'Psychic': ['Fight', 'Poison'],
                           'Ice': ['Flying', 'Ground', 'Grass', 'Dragon'],
                           'Dragon': ['Dragon'],
                           'Dark': ['Ghost', 'Psychic'],
                           'Fairy': ['Fight', 'Dragon', 'Dark'],
                           'None': []}
    not_very_effective_dict = {'Normal': ['Rock', 'Steel'],
                               'Fight': ['Flying', 'Poison', 'Bug', 'Psychic', 'Fairy'],
                               'Flying': ['Rock', 'Steel', 'Electric'],
                               'Poison': ['Poison', 'Rock', 'Ground', 'Ghost'],
                               'Ground': ['Bug', 'Grass'],
                               'Rock': ['Fight', 'Ground', 'Steel'],
                               'Bug': ['Fight', 'Flying', 'Poison', 'Ghost', 'Steel', 'Fire', 'Fairy'],
                               'Ghost': ['Dark'],
                               'Steel': ['Steel', 'Fire', 'Water', 'Electric'],
                               'Fire': ['Rock', 'Fire', 'Water', 'Dragon'],
                               'Water': ['Water', 'Grass', 'Dragon'],
                               'Grass': ['Flying', 'Poison', 'Bug', 'Steel', 'Fire', 'Grass', 'Dragon'],
                               'Electric': ['Grass', 'Electric', 'Dragon'],
                               'Psychic': ['Steel', 'Psychic'],
                               'Ice': ['Steel', 'Fire', 'Water', 'Psychic'],
                               'Dragon': ['Steel'],
                               'Dark': ['Fight', 'Dark', 'Fairy'],
                               'Fairy': ['Posion', 'Steel', 'Fire'],
                               'None': []}  

    
    nested_type =[[1,1], [1,1]]
    for i in range (0,2):
        for j in range (0,2):
            if pkmn2_type[j] in very_effective_dict.get(pkmn1_type[i]):
                nested_type[0][i] *=2
            if pkmn2_type[j] in not_very_effective_dict.get(pkmn1_type[i]):
                nested_type[0][i] /=2

            if pkmn1_type[j] in very_effective_dict.get(pkmn2_type[i]):
                nested_type[1][i] *=2
            if pkmn1_type[j] in not_very_effective_dict.get(pkmn2_type[i]):
                nested_type[1][i] /=2

    p1_type1 = nested_type[0][0]
    p1_type2 = nested_type[0][1]
    p2_type1 = nested_type[1][0]
    p2_type2 = nested_type[1][1]
    
    return (p1_type1, p1_type2, p2_type1, p2_type2) 

@app.route("/", methods=["GET","POST"])
@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('home', username=form.username.data))
    return render_template('login.html', form=form)

@app.route("/home/<username>", methods=["GET", "POST"])
def home(username):
    if request.method == 'POST':
        pkmn_stats = pd.read_csv("C:/Users/Nicolas/Downloads/Pokemon_Data/pokemon.csv") #Change the file path to wherever your csv file is stored

        pokemon1=request.form['pokemon1']
        pokemon2=request.form['pokemon2']

        pkmn1 = pkmn_stats.loc[pkmn_stats['Name'] == pokemon1]
        pkmn2 = pkmn_stats.loc[pkmn_stats['Name'] == pokemon2]

        hp_diff = int(pkmn1["HP"]) - int(pkmn2["HP"])
        attack_diff = int(pkmn1["Attack"]) - int(pkmn2["Attack"])
        defense_diff = int(pkmn1["Defense"]) - int(pkmn2["Defense"])
        sp_attack_diff = int(pkmn1["Sp. Atk"]) - int(pkmn2["Sp. Atk"])
        sp_defense_diff = int(pkmn1["Sp. Def"]) - int(pkmn2["Sp. Def"])
        speed_diff = int(pkmn1["Speed"]) - int(pkmn2["Speed"])
        legendary_diff = int(pkmn1["Legendary"]) - int(pkmn2["Legendary"])
        p1_type1, p1_type2, p2_type1, p2_type2 = get_types(pkmn1, pkmn2)


        model = pickle.load(open(r"C:\AI\CSCE 5214\P3\Predictemon\random_forest.pkl", 'rb')) #Change the file path to wherever your pickle file is stored
        winner = model.predict([[hp_diff, attack_diff, defense_diff, sp_attack_diff, sp_defense_diff, speed_diff, legendary_diff, p1_type1, p1_type2, p2_type1, p2_type2]])
        if winner == 0:
            champion = pokemon1
        else:
            champion = pokemon2

        return render_template("home.html", user=username, champion=champion)
    if request.method == 'GET':
        return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)

#winner = model.predict([[50, -34, -47, -34, -57, -2, 0, 1.0, 1.0, 1.0, 1.0]])
