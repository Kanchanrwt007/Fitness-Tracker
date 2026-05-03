# ⚡ FitTrack — Personal Fitness & Health Tracker

A full-stack fitness and health tracking web app built with **Python (Flask)**, **HTML**, and **CSS**.  
Log your workouts, track food intake, monitor water consumption, set fitness goals, and visualize your health progress — all in one place.

---

## 🚀 Features

- 🏋️ **Workout logging** — log exercise name, duration, and calories burned with quick preset buttons
- 🥗 **Food intake tracking** — log meals by type (Breakfast, Lunch, Dinner, Snack) with calorie counts
- 💧 **Water intake tracker** — one-click glass buttons with animated bottle fill visualization
- 📊 **Animated dashboard** — live progress rings for calories, burn, water, and workout time
- 🎯 **Daily goals system** — set targets and see a real-time checklist of what you've completed
- 📈 **Analytics page** — 7-day calorie trend chart, weekly summary, and calorie split chart
- ⚖️ **Body stats** — log daily weight and steps walked
- 🧮 **BMI calculator** — instant BMI result with category (Underweight, Normal, Overweight, Obese)
- 👟 **Step tracker** — log daily steps and track against your goal
- 🌙 **Dark / Light mode** toggle with preference saved automatically
- 💾 **Persistent data** stored locally using SQLite — no internet required
- 📅 **Date picker** on every page — view and log data for any past date

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask |
| Database | SQLite (via Python's built-in `sqlite3`) |
| Frontend | HTML5, CSS3|
| Fonts | Google Fonts — Plus Jakarta Sans |

---

## 📁 Project Structure
---

## ⚙️ Getting Started

### Prerequisites

- Python 3.7 or above
- pip (comes with Python)

### Step 1 — Download the project

```bash
git clone https://github.com/kanchanrwt007/fitness-tracker.git
cd fitness-tracker
```

Or simply download the ZIP and extract it.

### Step 2 — Install Flask

Open your terminal or VS Code terminal and run:

```bash
pip install flask
```

### Step 3 — Run the app

```bash
python app.py
```

### Step 4 — Open in your browser
The SQLite database (`fitness.db`) is created automatically on the very first run. No extra configuration needed.

---

## 🧭 How to Use

| Step | What to do |
|---|---|
| 1 | Go to **Goals** and set your daily calorie, burn, water, workout, and steps targets |
| 2 | Go to **Workout** and log your exercise — use quick preset buttons like Run, Yoga, Swim |
| 3 | Go to **Nutrition** and log every meal with calorie count and meal type |
| 4 | Go to **Water** and tap the glass buttons to quickly add water intake |
| 5 | Go to **Body Stats** to log your weight and steps for the day |
| 6 | Visit the **Dashboard** to see your animated rings and daily goals checklist |
| 7 | Check **Analytics** for your 7-day calorie trend and weekly summary |

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/workouts` | Get workouts for a specific date |
| POST | `/api/workouts` | Log a new workout |
| DELETE | `/api/workouts/<id>` | Delete a workout by ID |
| GET | `/api/food` | Get food entries for a specific date |
| POST | `/api/food` | Log a new food item |
| DELETE | `/api/food/<id>` | Delete a food entry by ID |
| GET | `/api/water` | Get total water intake for a date |
| POST | `/api/water` | Add water intake |
| GET | `/api/summary` | Full daily summary — calories, water, workout, steps, weight |
| GET | `/api/goals` | Get current fitness goals |
| POST | `/api/goals` | Save or update fitness goals |
| GET | `/api/trend` | 7-day calorie consumed vs burned data for chart |
| GET | `/api/daily_log` | Get weight and steps for a specific date |
| POST | `/api/daily_log` | Save or update weight and steps |

---

## 📸 Screenshots

> Add your own screenshots once the app is running. Take a screenshot of each page and save them inside a `screenshots/` folder.

| Dashboard | Workout | Nutrition |
|---|---|---|
| ![dashboard](screenshots/dashboard.png) | ![workout](screenshots/workout.png) | ![nutrition](screenshots/nutrition.png) |

| Water | Analytics | Goals |
|---|---|---|
| ![water](screenshots/water.png) | ![analytics](screenshots/analytics.png) | ![goals](screenshots/goals.png) |

---

## 🗄️ Database Tables

| Table | What it stores |
|---|---|
| `workouts` | Exercise name, duration, calories burned, date |
| `food` | Food item, calories, meal type, date |
| `water` | Water amount in liters, date |
| `goals` | All daily fitness targets |
| `daily_log` | Weight and steps per day |

---

## 🔮 Future Plans

- [ ] Export health data to CSV or PDF
- [ ] Weekly progress report by email
- [ ] Calorie lookup — search food and get calories automatically
- [ ] Workout history with personal records (PR tracking)
- [ ] Weight trend graph over weeks and months
- [ ] Mobile-friendly PWA version
- [ ] Meal planning feature for the week ahead

---

## 🙋‍♂️ About This Project

This is a personal project built entirely from scratch as part of learning full-stack web development with Python.

No frameworks like React or Django were used — just pure Flask on the backend, plain HTML and CSS on the frontend, and python as database. Every feature including the animated rings, water bottle visualization, BMI calculator, graphs was planned, designed, and coded manually.

**Built by:** Kanchan Rawat
**Location:** India  
**Stack:** Python · Flask  · HTML · CSS 

---

## 📄 License

This project is free and open source under the [MIT License](LICENSE).  
Feel free to fork it, improve it, and make it your own.

---

> *"Take care of your body. It's the only place you have to live."*
