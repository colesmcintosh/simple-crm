from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.models import Customer, Interaction, StatusChange
from app import db

bp = Blueprint('customers', __name__, url_prefix='/customers')

@bp.route('/')
@login_required
def index():
    customers = Customer.query.filter_by(user_id=current_user.id).all()
    return render_template('customers/index.html', customers=customers)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        customer = Customer(
            name=request.form.get('name'),
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            company=request.form.get('company'),
            status='lead',
            notes=request.form.get('notes'),
            user_id=current_user.id
        )
        # Record initial status
        status_change = StatusChange(
            customer=customer,
            old_status=None,
            new_status='lead'
        )
        db.session.add(customer)
        db.session.add(status_change)
        db.session.commit()
        flash('Customer added successfully')
        return redirect(url_for('customers.index'))
    return render_template('customers/add.html')

@bp.route('/<int:id>')
@login_required
def view(id):
    customer = Customer.query.get_or_404(id)
    if customer.user_id != current_user.id:
        flash('Access denied')
        return redirect(url_for('customers.index'))
    
    # Combine interactions and status changes for timeline
    timeline_items = []
    
    # Add status changes
    for change in customer.status_changes:
        timeline_items.append({
            'type': 'status_change',
            'date': change.created_at,
            'old_status': change.old_status,
            'new_status': change.new_status
        })
    
    # Add interactions
    for interaction in customer.interactions:
        timeline_items.append({
            'type': 'interaction',
            'date': interaction.created_at,
            'interaction_type': interaction.type,
            'notes': interaction.notes
        })
    
    # Sort timeline by date
    timeline_items.sort(key=lambda x: x['date'], reverse=True)
    
    return render_template('customers/view.html', 
                         customer=customer,
                         timeline_items=timeline_items)

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    customer = Customer.query.get_or_404(id)
    if customer.user_id != current_user.id:
        flash('Access denied')
        return redirect(url_for('customers.index'))
    
    if request.method == 'POST':
        customer.name = request.form.get('name')
        customer.email = request.form.get('email')
        customer.phone = request.form.get('phone')
        customer.company = request.form.get('company')
        new_status = request.form.get('status')
        
        # Check if status has changed
        if new_status != customer.status:
            status_change = customer.update_status(new_status)
            if status_change:
                db.session.add(status_change)
        
        customer.notes = request.form.get('notes')
        db.session.commit()
        flash('Customer updated successfully')
        return redirect(url_for('customers.view', id=customer.id))
    return render_template('customers/edit.html', customer=customer)

@bp.route('/<int:id>/interaction', methods=['POST'])
@login_required
def add_interaction(id):
    customer = Customer.query.get_or_404(id)
    if customer.user_id != current_user.id:
        flash('Access denied')
        return redirect(url_for('customers.index'))
    
    interaction = Interaction(
        type=request.form.get('type'),
        notes=request.form.get('notes'),
        customer_id=customer.id
    )
    db.session.add(interaction)
    db.session.commit()
    flash('Interaction added successfully')
    return redirect(url_for('customers.view', id=customer.id)) 