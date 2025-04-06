# Simple CRM

A lightweight, easy-to-use CRM system built with Flask and SQLite. Perfect for small organizations that need a simple way to manage customer relationships without the complexity of enterprise solutions. This is a completely self-hosted, free solution that puts you in control of your data.

## Why Self-Hosted?

- **Free Forever**: No monthly subscriptions or hidden costs
- **Data Privacy**: Keep your customer data entirely under your control
- **Customizable**: Modify the code to fit your specific needs
- **No Internet Required**: Works offline since it's running on your own infrastructure
- **No Vendor Lock-in**: Own your data and export it anytime

## Features

- User authentication and management
- Customer lifecycle management (Lead → Prospect → Qualified → Customer → Churned)
- Customer interaction tracking
- Dashboard with customer statistics
- Timeline view of customer interactions
- Clean, responsive interface

## Setup

1. Create a virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Visit http://localhost:5000 in your browser

## Usage

1. Register a new user account
2. Log in to access the dashboard
3. Add customers and track their status
4. Record interactions with customers (calls, emails, meetings)
5. View customer history and progress through the sales pipeline

## Project Structure

```
.
├── app/
│   ├── models/
│   │   └── models.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── customers.py
│   │   └── dashboard.py
│   ├── templates/
│   │   ├── auth/
│   │   ├── customers/
│   │   └── dashboard/
│   └── __init__.py
├── app.py
├── requirements.txt
└── README.md
```

## Database

The application uses SQLite as its database, which is perfect for small to medium-sized organizations. The database file (`crm.db`) will be created automatically when you first run the application.

## Security

- Passwords are hashed using Werkzeug's security functions
- User sessions are managed securely
- CSRF protection is enabled by default
- SQLAlchemy ORM prevents SQL injection

## Contributing

Feel free to submit issues and enhancement requests!