from flask import Flask, render_template,redirect,request	
import pandas as pd
import json
import os

app = Flask(__name__, )
app._static_folder = os.path.abspath("static/")
translations = pd.read_excel('pinyin_correction_table.xlsx').set_index('english')
json_data=open('mots_json.json')
data = json.load(json_data)

l  =list(data.values())
flatten = [item for sublist in l for item in sublist]
word_list = pd.Series(flatten)

df =translations.loc[data['Verbs']]
true_words =df['french']
english_words =list(df.index)
lang_country = 'french'
def check_answer(answer,true_word):

   return render_template('hello.html', answer = answer,true_word=true_word)


def choose_category(category,language):
    global df
    global true_words
    global english_words
    global lang_country 
    lang_country = language
    df =translations.loc[data[category]]
    true_words = df[language]
    english_words = list(df.index)
    

i=0
score=0
@app.route('/',methods=['GET', 'POST']) 
def send_form():
        global i
        global score
        i = 0
        score=0
        print('pass')
        return render_template('choose_cat.html')

@app.route('/score',methods=['GET', 'POST']) 
def send_form2():
        category = request.form['category'] 
        language = request.form['language'] 
        choose_category(category,language)
        return redirect('/get_answer/non>', code=302)

@app.route('/hello/<answer>/<true_word>',methods=['GET', 'POST']) 
def hello_name_score(answer,true_word):

        return check_answer(answer,true_word)

    
@app.route('/get_answer/<verite>',methods=['GET', 'POST']) 
def get_answer(verite):
    global true_words
    global english_words
    global i
    global score
    print(i)
    print(len(true_words))
    if i==len(true_words)-1:
        #return('END. Your score is : '+str(score)+' out of '+str(len(df)))
        print('inside')
        return(render_template('score.html',score = score))
    english = english_words[i]
    correction = true_words[i]
    
    if verite=='oui':
        reponse = request.form['translation_result']
        i+=1
        if reponse==correction:
            score+=1
        print(score)
        return check_answer(reponse,correction)
    else:
        print("non")
        print(verite)
    global lang_country
    print(lang_country)
    return render_template('original_form.html',language = lang_country,word=english)

if __name__ == '__main__':
   app.run(debug = True)
