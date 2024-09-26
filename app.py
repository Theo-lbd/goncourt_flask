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


# Route pour le vote du jury (sélection des 8 livres)
@app.route('/jury', methods=['GET', 'POST'])
def jury():
    if 'jury_authenticated' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        selected_books = request.form.getlist('selected_books')
        if len(selected_books) == 8:
            session['selected_books'] = selected_books  # Stocker les 8 livres sélectionnés
            return redirect(url_for('second_vote'))

    books = get_all_books()
    return render_template('jury.html', books=books)


# Route pour la phase intermédiaire (vote pour réduire de 8 à 4 livres)
@app.route('/second_vote', methods=['GET', 'POST'])
def second_vote():
    selected_books = session.get('selected_books', [])

    if request.method == 'POST':
        selected_finalists = request.form.getlist('selected_finalists')
        if len(selected_finalists) == 4:
            session['finalists'] = selected_finalists  # Stocker les 4 livres finalistes
            return redirect(url_for('final_selection'))

    books = get_all_books()
    selected_books_data = [book for book in books if str(book.book_id) in selected_books]

    return render_template('second_vote.html', selected_books=selected_books_data)


# Route pour la phase finale du vote (sélection du gagnant)
@app.route('/final', methods=['GET', 'POST'])
def final_selection():
    finalists = session.get('finalists', [])

    if request.method == 'POST':
        selected_finalist = request.form.get('selected_finalist')
        session['final_winner'] = selected_finalist
        return redirect(url_for('winner'))

    books = get_all_books()
    finalists_books = [book for book in books if str(book.book_id) in finalists]

    return render_template('final.html', finalists_books=finalists_books)


# Route pour afficher le gagnant
@app.route('/winner')
def winner():
    final_winner_id = session.get('final_winner')

    if not final_winner_id:
        return redirect(url_for('home'))  # Redirige si aucun gagnant n'a été choisi

    books = get_all_books()
    winner_book = next((book for book in books if str(book.book_id) == final_winner_id), None)

    return render_template('winner.html', winner_book=winner_book)


# --- Routes pour le public pour afficher les sélections ---
# Route pour afficher les 8 livres sélectionnés
@app.route('/public/selected_books')
def public_selected_books():
    selected_books = session.get('selected_books', [])
    if not selected_books:
        return "Aucune sélection de livres pour le moment."

    books = get_all_books()
    selected_books_data = [book for book in books if str(book.book_id) in selected_books]

    return render_template('public_selected_books.html', selected_books=selected_books_data)


# Route pour afficher les 4 finalistes
@app.route('/public/finalists')
def public_finalists():
    finalists = session.get('finalists', [])
    if not finalists:
        return "Aucune sélection de finalistes pour le moment."

    books = get_all_books()
    finalists_books = [book for book in books if str(book.book_id) in finalists]

    return render_template('public_finalists.html', finalists_books=finalists_books)


# Route pour afficher le livre gagnant
@app.route('/public/winner')
def public_winner():
    final_winner_id = session.get('final_winner')

    if not final_winner_id:
        return "Aucun gagnant sélectionné pour le moment."

    books = get_all_books()
    winner_book = next((book for book in books if str(book.book_id) == final_winner_id), None)

    return render_template('public_winner.html', winner_book=winner_book)


# --- Fin des routes pour le public ---

# Route pour recommencer le vote
@app.route('/revote')
def revote():
    session.pop('selected_books', None)  # Supprimer la liste des 8 livres sélectionnés
    session.pop('finalists', None)  # Supprimer la liste des finalistes
    session.pop('final_winner', None)  # Supprimer le gagnant
    return redirect(url_for('jury'))  # Revenir à la sélection initiale


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
    session.pop('selected_books', None)
    session.pop('finalists', None)
    session.pop('final_winner', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
