from flask import render_template, request, flash, redirect


from .app import app, login
from .modeles.donnees import Comment
from .modeles.utilisateurs import User
#from .constantes import LIEUX_PAR_PAGE
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
def accueil():
    """ Route permettant l'affichage d'une page accueil
    """
    # On a bien sûr aussi modifié le template pour refléter le changement
    commentaires = Comment.query.order_by(Comment.comment_id.desc()).limit(5).all()
    return render_template("pages/accueil.html", nom="Imaginatiiif", commentaires=commentaires)


@app.route("/comment/<int:comment_id>")

def commentaire(comment_id):
    import requests

    # On a bien sûr aussi modifié le template pour refléter le changement
    unique_commentaire = Comment.query.get(comment_id)
    utilisateur=User.query.get(unique_commentaire.comment_user_id)
    r = requests.get(unique_commentaire.comment_lien)
    data = r.json()
    simplified = []
    for item in data["metadata"]:
        try:
            identifier = item["label"]

            simplified.append(identifier)

        except:
            error = 'Pas pu récupérer les données'
            data = {}
    return render_template('pages/comment.html', nom='Imaginatiiif',
                           commentaire=unique_commentaire,
                           user=utilisateur,
                           data=data.get('metadata'))
    #return render_template("pages/comment.html",
                           #nom="Imaginatiiif",
                           #commentaire=unique_commentaire,
                           #user=utilisateur)




@app.route("/register", methods=["GET", "POST"])
def inscription():
    """ Route gérant les inscriptions
    """
    # Si on est en POST, cela veut dire que le formulaire a été envoyé
    if request.method == "POST":
        statut, donnees = User.creer(
            login=request.form.get("login", None),
            email=request.form.get("email", None),
            nom=request.form.get("nom", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if statut is True:
            flash("Enregistrement effectué. Identifiez-vous maintenant", "success")
            return redirect("/")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/inscription.html")
    else:
        return render_template("pages/inscription.html")

@app.route("/nomcommentaire", methods=["GET", "POST"])
@login_required
def nomcommentaire():
    """ Route gérant les inscriptions
    """
    # Si on est en POST, cela veut dire que le formulaire a été envoyé
    if request.method == "POST":
        statut, donnees = Comment.creercomment(
            nom=request.form.get("nom", None),
            commentaire=request.form.get("commentaire", None),
            lien=request.form.get("lien", None),
            user_id=current_user.get_id()

        )
        if statut is True:
            flash("Enregistrement effectué", "success")
            return redirect("/")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/nomcommentaire.html")
    else:
        return render_template("pages/nomcommentaire.html")

@app.route("/connexion", methods=["POST", "GET"])
def connexion():
    """ Route gérant les connexions
    """
    if current_user.is_authenticated is True:
        flash("Vous êtes déjà connecté-e", "info")
        return redirect("/")
    # Si on est en POST, cela veut dire que le formulaire a été envoyé
    if request.method == "POST":
        utilisateur = User.identification(
            login=request.form.get("login", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if utilisateur:
            flash("Connexion effectuée", "success")
            login_user(utilisateur)
            return redirect("/")
        else:
            flash("Les identifiants n'ont pas été reconnus", "error")

    return render_template("pages/connexion.html")
login.login_view = 'connexion'


@app.route("/deconnexion", methods=["POST", "GET"])
def deconnexion():
    if current_user.is_authenticated is True:
        logout_user()
    flash("Vous êtes déconnecté-e", "info")
    return redirect("/")
