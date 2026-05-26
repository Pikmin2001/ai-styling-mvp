# AI Styling MVP

A full-stack fashion recommendation web app that generates personalized outfits based on user preferences like gender, budget, and style tags.

---

## Features

* Outfit generation based on:

  * gender
  * budget
  * style preferences
* Dynamic outfit swapping
* Image-based outfit cards
* Save/share outfit functionality
* Smart style matching logic
* Responsive modern UI
* Full-stack architecture

---

## Tech Stack

### Frontend

* React
* TypeScript
* Vite
* TanStack Router

### Backend

* FastAPI
* Python
* Pydantic
* SQLModel

---

## 

<img width="795" height="945" alt="image" src="https://github.com/user-attachments/assets/98b7939c-c0cc-4449-9be1-8667bcea7b33" />


---

## Project Structure

```bash
ai-styling-mvp/
│
├── frontend/       # React frontend
├── backend/        # FastAPI backend
└── README.md
```

---

## Local Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd ai-styling-mvp
```

---

## Backend Setup

### 1. Navigate to backend

```bash
cd backend
```

### 2. Install dependencies

Using Poetry:

```bash
poetry install
```

### 3. Run backend server

```bash
poetry run uvicorn app.main:app --reload
```

Backend runs on:

```txt
http://localhost:8000
```

Swagger docs:

```txt
http://localhost:8000/docs
```

---

## Frontend Setup

### 1. Navigate to frontend

```bash
cd frontend
```

### 2. Install dependencies

```bash
npm install
```

### 3. Run frontend

```bash
npm run dev
```

Frontend runs on:

```txt
http://localhost:5173
```

---

## Environment Variables

Create a `.env` file inside `frontend/`:

```env
VITE_API_URL=http://localhost:8000
```

---

## Example Features

### Style Quiz

Users can select:

* Casual
* Streetwear
* Minimalist
* Formal

### Outfit Generation

The backend:

* filters inventory
* scores item compatibility
* builds cohesive outfits
* returns a styled recommendation

---

## Future Improvements

* AI/LLM-powered styling recommendations
* Real retailer inventory integration
* User authentication
* Saved wardrobes
* Occasion-based styling
* Vector/image similarity search
* Computer vision for clothing analysis
* Personalized recommendation engine

---

## Foci

I wanted to tinker with:

*FastAPI
* recommendation systems
* full-stack application architecture
* AI-powered personalization
* UI/UX product design
   

---

## Author

Josh 

GitHub: https://github.com/Pikmin2001

---

## License

MIT License
