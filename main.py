from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from . import db
from .models import Todo

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template("index.html")

@main.route("/profile")
@login_required
def profile():
    todo = Todo.query.all()
    return render_template("profile.html",todos=todo)

@main.route("/todo_post", methods=["POST"])
@login_required
def save_todo():
    todo = request.form.get("todo")
    new_todo = Todo(text=todo,user_id=current_user.id)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('main.profile'))

@main.route("/update_todo/<int:id>", methods=["GET", "POST"])
@login_required
def update_todo(id):
    todo = Todo.query.get_or_404(id)
    if current_user.id != id:
        flash('You dont have permission to update another user Todo')
        return redirect(url_for('main.profile'))
    if request.method=="POST":
        todo.text = request.form.get("todo")
        db.session.commit()
        flash(f"{todo.text} Updated")
        return redirect(url_for('main.profile'))
    return render_template("update_todo.html", todo=todo)


@main.route("/delete_todo/<int:id>")
@login_required
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    if current_user.id != id:
        flash('You dont have permission to Delete another user Todo')
        return redirect(url_for('main.profile'))
    db.session.delete(todo)
    db.session.commit()
    flash(f"{todo.text} Deleted")
    return redirect(url_for('main.profile'))
