# Movie-Recommendation-System-using-Data-Engineering-and-Content-Based-Filtering

A content-based Movie Recommender System built using Machine Learning techniques.
This project suggests similar movies based on user input using cosine similarity.

---

## 📌 Project Overview

This system recommends movies by analyzing features like:

* Genres
* Keywords
* Cast
* Crew

It uses **Natural Language Processing (NLP)** and **vectorization techniques** to compute similarity between movies.

---

## ⚙️ Tech Stack

* Python 🐍
* Pandas & NumPy
* Scikit-learn
* Streamlit (for UI, if used)
* Jupyter Notebook

---

## 📁 Project Structure

```
movie-recommender-system/
│
├── app.py                          # Main application file
├── movie_dict.pkl                  # Movie metadata dictionary
├── movies.pkl                      # Processed movie dataset
├── similarity.pkl ❌ (not included)
├── movie-recommender-system.ipynb  # Model building notebook
├── README.md
```

---

## ⚠️ Important Note

The file **`similarity.pkl`** is not included in this repository due to GitHub file size limits.

---

## 🚀 How to Run the Project

### Step 1: Clone the repository

```
git clone https://github.com/your-username/movie-recommender-system.git
cd movie-recommender-system
```

### Step 2: Install dependencies

```
pip install -r requirements.txt
```

*(If requirements.txt is not present, install manually: pandas, numpy, sklearn, streamlit)*

---

### Step 3: Generate similarity matrix

1. Open:

```
movie-recommender-system.ipynb
```

2. Run all cells
3. This will generate:

```
similarity.pkl
```

---

### Step 4: Run the application

```
python app.py
```

*(or if using Streamlit)*

```
streamlit run app.py
```

---

## 📥 Alternative (Download Precomputed File)

You can directly download the similarity matrix from here:

👉 https://drive.google.com/file/d/1xZ5l1TEd6Tn51tEO0L7w1H_J1OkSct01/view?usp=sharing

Place it in the project folder before running the app.

---

## 🧠 How It Works

1. Data preprocessing is done on movie datasets
2. Important features are combined into a single text column
3. Text is converted into vectors using **CountVectorizer**
4. **Cosine similarity** is calculated between all movies
5. Based on user input, top similar movies are recommended

---

## 📊 Example

Input:

```
Avatar
```

Output:

```
1. Guardians of the Galaxy
2. John Carter
3. Star Trek
4. Avengers
5. Interstellar
```

---

## 💡 Future Improvements

* Add collaborative filtering
* Improve UI design
* Deploy on cloud (AWS / Streamlit Cloud)
* Add user login & ratings system

---

## 🙋‍♀️ Author

RIYA KALOKHE

---

## ⭐ Acknowledgment

Dataset used: TMDB 5000 Movie Dataset

---

## 📌 Note for Evaluators

Due to file size constraints, large model files are excluded.
Kindly follow the steps above to regenerate them or download from the provided link.
