# SkillSwap

SkillSwap is a full-stack web application that enables users to exchange skills within a community. Users can create profiles, list skills they can offer, select skills they want to learn, and connect with others for skill swaps. The platform features a modern React frontend (with Tailwind CSS) and a Django REST backend.

---

## Features

- **User Authentication:** Register, login, and manage your account securely.
- **Profile Management:** Edit your profile, upload a photo, set your location and availability.
- **Skills Library:** Browse a library of predefined skills, add custom skills, and see who offers or wants each skill.
- **Skill Selection:** Select multiple skills you can offer and want to learn, with a modern chip-based UI.
- **Skill Swap Requests:** Request skill swaps with other users.
- **Feedback System:** Leave feedback and ratings after a skill swap.
- **Responsive UI:** Beautiful, modern, and mobile-friendly design using Tailwind CSS.
- **Admin Panel:** Manage users and skills via Django admin.

---

## Project Structure

```
odoo_shreyansh/
├── skillswap-frontend/   # React + Tailwind CSS frontend
├── skillswap_backend/    # Django backend (API, models, admin, etc.)
```

---

## Getting Started

### Prerequisites

- **Node.js** (v16+ recommended)
- **npm** (v8+ recommended)
- **Python** (v3.9+ recommended)
- **pip** (v21+ recommended)
- **virtualenv** (recommended for backend)

---

### Backend Setup (Django)

1. **Navigate to the backend directory:**
   ```sh
   cd skillswap_backend
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Apply migrations:**
   ```sh
   python manage.py migrate
   ```

5. **Create a superuser (admin):**
   ```sh
   python manage.py createsuperuser
   ```

6. **Run the backend server:**
   ```sh
   python manage.py runserver
   ```
   The API will be available at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

### Frontend Setup (React + Tailwind CSS)

1. **Navigate to the frontend directory:**
   ```sh
   cd skillswap-frontend
   ```

2. **Install dependencies:**
   ```sh
   npm install
   ```

3. **Start the frontend server:**
   ```sh
   npm start
   ```
   The app will be available at [http://localhost:3000/](http://localhost:3000/)

---

## Usage

- Register a new account or log in.
- Complete your profile and select skills you can offer and want to learn.
- Browse the Skills Library and see who offers or wants each skill.
- Send and receive skill swap requests.
- Leave feedback after a swap.

---

## Customization

- **Add Predefined Skills:** Use the Django management command to add a set of predefined skills:
  ```sh
  python manage.py add_predefined_skills
  ```
- **Admin Panel:** Access Django admin at `/admin` to manage users and skills.

---

## Tech Stack

- **Frontend:** React, TypeScript, Tailwind CSS, Axios
- **Backend:** Django, Django REST Framework, SimpleJWT, SQLite (default)
- **Other:** PostCSS, Django CORS Headers, Django Filter

---

## License

This project is for educational and demonstration purposes.

---

If you need further customization or want to add deployment instructions, let me know! 