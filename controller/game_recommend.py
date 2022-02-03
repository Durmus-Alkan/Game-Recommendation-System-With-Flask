#oyun önerisi yapılan yer controller
from flask import Flask, render_template,request
import sqlite3
app = Flask(__name__, template_folder='../view/')
@app.route("/")
def home():
    return render_template("home.html")


# Form Verileri Alma
@app.route("/oneriler", methods=['POST', 'GET'])
def verilerial():
   if request.method == 'POST':
       with sqlite3.connect("../model/content-base-code/gamedatabase.db") as database:
           database.row_factory = sqlite3.Row
           game1 = request.form.get('game1')
           game2 =request.form.get('game2')
           game3 =request.form.get('game3')
           cur = database.cursor()
           cur.execute("SELECT r.game1, r.game2,r.game3, r.game4,r.game5, r.game6,r.game7, r.game8, r.game9, r.game10 "
                       "FROM games INNER JOIN recommend as r on games.appid = r.appid "
                       "WHERE games.name = '"+ game1 +"'"
                                                      "OR games.name = '" + game2 + "'"
                                                                                    "OR games.name = '" + game3 + "'")

           rows = cur.fetchall()

           return render_template("oneriler.html", rows=rows)

   else:
      return render_template("oneriler.html", hata="Formdan veri gelmedi!")


if __name__ == "__main__":
    app.run(debug = True)
