# Django Todo App

A modern, responsive todo application built with Django and styled with Tailwind CSS. This application allows users to manage their tasks efficiently with a clean, dark-themed interface.

## 📋 Project Description

This is a full-featured todo application that provides user authentication, task management, and progress tracking. Users can create accounts, manage their personal todo lists, and track their productivity with visual progress indicators.

## 🛠️ Tech Stack

### Backend
- **Python 3.14** - Programming language
- **Django 5.2.8** - Python web framework
- **PostgreSQL** - Database
- **Docker** - PostgreSQL containerization

### Frontend
- **Tailwind CSS** - Utility-first CSS framework
- **HTML5** - Markup language
- **JavaScript** - Client-side functionality
- **SVG Icons** - Vector graphics for UI elements

### Development Tools
- **python-dotenv** - Environment variable management
- **psycopg** - PostgreSQL adapter for Python

## ✨ Features

### Authentication System
- ✅ User registration with custom user model
- ✅ Secure login/logout functionality
- ✅ Password visibility toggle
- ✅ Form validation and error handling
- ✅ Persistent sessions (users stay logged in after server restart)

### Todo Management
- ✅ Create, read, update, and delete todos
- ✅ Three-status system (TODO, IN_PROGRESS, DONE)
- ✅ User-specific todo lists with privacy controls
- ✅ Todo creation and modification timestamps
- ✅ Real-time search and filtering
- ✅ Advanced sorting options (newest, oldest, A-Z, Z-A)
- ✅ Pagination for large todo lists

### Collaboration & Sharing
- ✅ Share todos with other registered users
- ✅ Real-time username validation during sharing
- ✅ **Strict permission-based access controls**:
  - **Owners**: Full access (edit, delete, share)
  - **Shared users**: Status updates only (no editing/sharing)
- ✅ Visual indicators for shared todos
- ✅ Share during todo creation or after
- ✅ **Security**: Only owners can share todos

### Dashboard & Analytics
- ✅ Comprehensive 3-tier dashboard:
  - **Overall Statistics** (owned + shared todos)
  - **Your Own Tasks** (personal todos only)
  - **Shared Tasks** (collaborative todos only)
- ✅ Visual progress tracking with completion rates
- ✅ Status-based categorization with icons
- ✅ Motivational messages based on progress
- ✅ Real-time statistics updates

### User Interface
- ✅ Responsive table view with mobile card fallback
- ✅ Dark theme with brand colors (#020013 primary, #F59E0B secondary)
- ✅ Sidebar navigation with mobile hamburger menu
- ✅ Live search without page refresh
- ✅ Modal-based sharing interface
- ✅ Smooth animations and hover effects
- ✅ Form styling with icons and real-time validation
- ✅ Sequential numbering instead of database IDs

### Advanced Features
- ✅ Real-time user existence validation
- ✅ AJAX-powered sharing system
- ✅ Filter by ownership type (all, owned, shared)
- ✅ Status-based filtering and sorting
- ✅ Pagination with search preservation
- ✅ **Role-based UI restrictions** (shared users see limited interface)
- ✅ **Multi-level security enforcement** (template, view, backend)
- ✅ Admin panel integration
- ✅ CSRF protection and security measures

## 🚀 Installation & Setup

### Prerequisites
- Python 3.14+
- Docker (for PostgreSQL)
- pip (Python package manager)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd django-todo
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install django psycopg python-dotenv
```

### 4. Database Setup (PostgreSQL with Docker)
```bash
# Run PostgreSQL container
docker run -d --name postgresql \
  -e POSTGRES_USER=your_username \
  -e POSTGRES_PASSWORD='your_password' \
  -e POSTGRES_DB=tododb \
  -v ~/docker/postgres-data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --restart unless-stopped \
  postgres:16
```

### 5. Environment Configuration
After running the container, create a `.env` file in the project root:
```env
DB_NAME=tododb
DB_USER=your_username
DB_PASS=your_password
DB_HOST=127.0.0.1
DB_PORT=5432
```

### 6. Run Migrations
```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the application.
Visit `http://127.0.0.1:8000/admin/` to access the admin site.

## 📁 Project Structure

```
django-todo/
├── config/                 # Project configuration
│   ├── settings.py        # Django settings
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py           # WSGI configuration
├── todo/                  # Main application
│   ├── migrations/       # Database migrations
│   ├── templates/todo/   # HTML templates
│   │   ├── base.html    # Base template with navigation
│   │   ├── dashboard.html # Dashboard with statistics
│   │   ├── todos.html   # Todo list view
│   │   ├── todo_form.html # Create/edit todo form
│   │   ├── login.html   # Login form
│   │   └── register.html # Registration form
│   ├── models.py        # Database models (User, Todo)
│   ├── views.py         # View functions
│   ├── forms.py         # Django forms
│   ├── urls.py          # App URL patterns
│   └── admin.py         # Admin configuration
├── static/              # Static files (CSS, JS, images)
├── .env                 # Environment variables
├── manage.py           # Django management script
└── README.md           # Project documentation
```

## 🎨 Design Features

### Color Scheme
- **Primary Color:** #020013 (Deep dark blue/black)
- **Secondary Color:** #F59E0B (Warm amber/gold)
- **Background:** Dark theme throughout the application
- **Status Colors:** 
  - Green for completed tasks
  - Blue for in-progress tasks
  - Yellow for pending tasks
  - Gray for shared content

### Responsive Design
- Mobile-first approach with adaptive layouts
- Desktop: Responsive table view
- Mobile/Tablet: Card-based layout
- Collapsible sidebar navigation
- Touch-friendly interface elements
- Responsive dashboard grids (1-2-4 columns)

## 🔗 URL Routes

| URL | View | Description |
|-----|------|-------------|
| `/` | login_user | User login page |
| `/register/` | register_user | User registration |
| `/logout/` | logout_user | User logout |
| `/dashboard/` | dashboard | Enhanced dashboard with 3-tier statistics |
| `/todos/` | todos | Advanced todo list with search, filter, sort |
| `/dashboard/new/` | new_todo | Create new todo with sharing option |
| `/dashboard/todo/update/<id>/` | update_todo | Edit todo (permission-based) |
| `/dashboard/todo/delete/<id>/` | delete_todo | Delete todo (owners only) |
| `/todos/share/<id>/` | share_todo | Share todo with other users |
| `/check-user/` | check_user | Real-time username validation |
| `/admin-login-now/` | admin | Django admin panel |


**Happy Task Managing! 📝✨**