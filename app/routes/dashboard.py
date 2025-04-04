from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.models import Customer
from sqlalchemy import func
from app import db

bp = Blueprint('dashboard', __name__)

@bp.route('/')
@login_required
def index():
    # Get customer counts by status
    status_counts = db.session.query(
        Customer.status, 
        func.count(Customer.id)
    ).filter_by(
        user_id=current_user.id
    ).group_by(
        Customer.status
    ).all()
    
    # Get recent customers
    recent_customers = Customer.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Customer.created_at.desc()
    ).limit(5).all()
    
    return render_template('dashboard/index.html',
                         status_counts=dict(status_counts),
                         recent_customers=recent_customers) 