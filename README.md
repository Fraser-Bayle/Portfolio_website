```markdown
# 8-Bit-Dev Portfolio

A retro-themed developer portfolio built with Django and styled with a Matrix-inspired design theme.

## Features

- Responsive navigation with Matrix-inspired green (#00ff00) styling
- Retro 8-bit aesthetics using "Press Start 2P" font
- Project showcase functionality
- Contact and About pages
- Mobile-friendly design

## Tech Stack

- Python 3.10.7
- Django
- Bootstrap 4.5.2
- Custom CSS

## Project Structure
```
8-bit-dev/
├── manage.py
├── static/
│   └── css/
│       └── style.css
├── templates/
│   └── base.html
├── pages/
│   └── views.py
└── projects/
    ├── models.py
    └── views.py
```
## Models

### Project
- Displays portfolio projects
- Related through tags

### Tag
- Categorizes projects
- Many-to-many relationship with Project model

## Setup

1. Clone the repository:
```bash
git clone [repository-url]
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Styling

The site features a custom Matrix-inspired theme:
- Black (#000) backgrounds
- Matrix green (#00ff00) accents
- White (#fff) hover effects with green glow
- Retro 8-bit font styling

## License

© 2025 Fraser W Bayle. All rights reserved.
```
