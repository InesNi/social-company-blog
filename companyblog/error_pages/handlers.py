from flask import Blueprint, render_template
from companyblog import db

error_pages = Blueprint('error_pages', __name__)

@error_pages.app_errorhandler(404)
def error_404(error):
    return render_template('error_pages/404.html') , 404

@error_pages.app_errorhandler(403)
def error_403(error):
    return render_template('error_pages/403.html') , 403

@error_pages.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error_pages/500.html'), 500