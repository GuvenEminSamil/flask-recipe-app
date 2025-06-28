from flask import render_template, redirect, url_for, session, flash, request, abort
from flask.views import MethodView
from app import db
from app.models.comment import Comment
from app.forms.comment_form import CommentForm

class CommentCreateView(MethodView):
    def post(self, recipe_id):
        if "user_id" not in session:
            flash("You must be logged in to comment.", "danger")
            return redirect(url_for("login"))

        form = CommentForm()
        if form.validate_on_submit():
            comment = Comment(
                content=form.content.data,
                user_id=session["user_id"],
                recipe_id=recipe_id,
            )
            db.session.add(comment)
            db.session.commit()
            flash("Comment Added.", "success")

        return redirect(url_for("meal_detail", meal_id=recipe_id))


class CommentEditView(MethodView):
    def get(self, comment_id):
        comment = Comment.query.get_or_404(comment_id)
        if comment.user_id != session.get("user_id"):
            abort(403)

        form = CommentForm(obj=comment)
        return render_template("comments/edit.html", form=form, comment=comment)

    def post(self, comment_id):
        comment = Comment.query.get_or_404(comment_id)
        if comment.user_id != session.get("user_id"):
            abort(403)

        form = CommentForm()
        if form.validate_on_submit():
            comment.content = form.content.data
            db.session.commit()
            flash("Comment updated.", "success")
            return redirect(url_for("meal_detail", meal_id=comment.recipe_id))

        return render_template("comments/edit.html", form=form, comment=comment)

class CommentDeleteView(MethodView):
    def post(self, comment_id):
        comment = Comment.query.get_or_404(comment_id)
        if comment.user_id != session.get("user_id"):
            abort(403)

        db.session.delete(comment)
        db.session.commit()
        flash("Comment deleted.", "info")
        return redirect(url_for("meal_detail", meal_id=comment.recipe_id))