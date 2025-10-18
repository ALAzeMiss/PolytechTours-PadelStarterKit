# 📋 Instructions de finalisation

## ⚠️ IMPORTANT

Ce script a créé la STRUCTURE du projet, mais les fichiers de code source
sont des PLACEHOLDERS. Vous devez les remplir avec le contenu des artifacts.

## 🔧 Étapes suivantes

### 1. Copier les fichiers backend

Copiez le contenu de l'artifact "Backend - Code principal" dans :
- `backend/app/main.py`
- `backend/app/core/config.py`
- `backend/app/core/security.py`
- `backend/app/database.py`
- `backend/app/models/models.py`
- `backend/app/schemas/auth.py`
- `backend/app/api/auth.py`
- `backend/app/api/deps.py`

### 2. Copier les fichiers frontend

Copiez le contenu de l'artifact "Frontend - Code principal" dans :
- `frontend/src/main.js`
- `frontend/src/App.vue`
- `frontend/src/router/index.js`
- `frontend/src/services/api.js`
- `frontend/src/stores/auth.js`
- `frontend/src/components/NavBar.vue`
- `frontend/src/views/HomePage.vue`
- `frontend/src/views/LoginPage.vue`
- `frontend/src/assets/main.css`

### 3. Copier les tests

Copiez le contenu de l'artifact "Tests - Exemples" dans :
- `backend/tests/conftest.py`
- `backend/tests/test_auth.py`
- `backend/tests/test_security.py`
- `backend/tests/test_validation.py`
- `frontend/cypress/e2e/auth.cy.js`
- `frontend/cypress/e2e/navigation.cy.js`
- `frontend/cypress/support/commands.js`

### 4. Tester l'installation

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Éditer .env pour ajouter une vraie SECRET_KEY
python -c "from app.database import init_db; init_db()"
uvicorn app.main:app --reload

# Frontend (nouveau terminal)
cd frontend
npm install
cp .env.example .env
npm run dev
```

### 5. Vérification

- Backend : http://localhost:8000/docs
- Frontend : http://localhost:5173
- Login : admin@padel.com / Admin@2025!

### 6. Créer l'archive finale

```bash
cd ..
zip -r corpo-padel-starter-kit.zip corpo-padel-starter-kit/
```

## 📚 Documentation

- Cahier des charges : Exportez l'artifact HTML en PDF
- README : Déjà créés dans backend/ et frontend/
- Guide d'utilisation : Consultez l'artifact correspondant

## ✅ Checklist finale

- [ ] Tous les fichiers de code sont copiés
- [ ] Le backend démarre sans erreur
- [ ] Le frontend démarre sans erreur
- [ ] La connexion fonctionne
- [ ] Les tests passent
- [ ] Le cahier des charges est en PDF
- [ ] L'archive ZIP est créée

Bon projet ! 🎾
