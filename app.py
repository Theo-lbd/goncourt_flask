from flask import Flask, render_template, request, redirect, url_for, session
from business.book import get_all_books

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Pour sécuriser les sessions


# Page d'accueil
@app.route('/')
def home():
    return render_template('index.html')


# Route pour afficher tous les livres
@app.route('/books')
def display_books():
    books = get_all_books()
    return render_template('books.html', books=books)


# Route pour le vote du jury
@app.route('/jury', methods=['GET', 'POST'])
def jury():
    if 'jury_authenticated' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        selected_books = request.form.getlist('selected_books')
        return redirect(url_for('final_selection'))

    books = get_all_books()
    return render_template('jury.html', books=books)


# Route pour la phase finale du vote
@app.route('/final')
def final_selection():
    return render_template('final.html')


# Route pour se connecter comme jury
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == '123456789':  # Le mot de passe du jury
            session['jury_authenticated'] = True
            return redirect(url_for('jury'))
        else:
            return "Mot de passe incorrect."
    return render_template('login.html')


# Route pour se déconnecter
@app.route('/logout')
def logout():
    session.pop('jury_authenticated', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
