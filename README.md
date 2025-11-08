# OpenBook--IntelligentNews-SmarterConversations
Django Based Web Platform

---

 <p align="center">
  <img src="images/home.png?raw=true" style="max-width:100%;height:auto;" alt="Image 1"/>
</p> 

---

OpenBook is an AI-integrated news and content platform built with **Django**, designed to deliver, analyze, and interact with news intelligently.  
It combines traditional article publishing with modern AI capabilities — including **automated Q&A generation**, **contextual chatbot interactions**, and **smart content management**.

---

## 🚀 Features

### 🧩 Core Modules
- **User Authentication & Profiles** — Secure login, registration, and user management.
- **Article Management** — Multi-role access for Admin, Editor, Moderator, and User.
- **Comments & Reactions** — Like, dislike, comment, and save articles for later.
- **Role-Based Access Control (RBAC)** — Workflow for reviewing, approving, or rejecting articles.
- **Community Mode** — User-submitted posts displayed as public content.

---

# Gallery

<div style="display: flex; gap: 10px;">
  <img src="images/api_news_page.png" alt="Image 1" style="width: 30%; max-width: 150px; height: auto;">
  <img src="images/article_det.png" alt="Image 2" style="width: 30%; max-width: 150px; height: auto;">
  <img src="images/opi_qa_generator.png" alt="Image 3" style="width: 30%; max-width: 150px; height: auto;">
</div>

<details>
  <summary>Show more images</summary>
  <div style="display: flex; gap: 10px; margin-top:10px;">
    <img src="images/editor_dash.png" alt="Image 4" style="width: 30%; max-width: 150px; height: auto;">
    <img src="images/moderator_dash.png" alt="Image 5" style="width: 30%; max-width: 150px; height: auto;">
    <img src="images/opi-chat-underdevelopment.png" alt="Image 6" style="width: 30%; max-width: 150px; height: auto;">
  </div>
</details>

---

### 🤖 AI Integrations
- **Smart Q&A Generator**  
  Automatically generates **5 high-quality question–answer pairs** per article using the Gemini API.  
  This allows readers to quickly understand article highlights or test their comprehension.

- **Opi — The Chatbot**  
  An AI chatbot built using the **Gemini API**, designed to engage users in intelligent conversations about news, context, or related topics.  
  *(Experimental feature: under development to enhance contextual accuracy.)*

---

### 📊 Analytics (Planned)
- Dashboard for tracking:
  - Top articles & trending categories
  - User engagement metrics
  - Reaction & comment analytics
  - Content growth over time

---

## 🏗️ Tech Stack

| Category | Technology |
|-----------|-------------|
| **Backend** | Django (Python) |
| **Frontend** | HTML, CSS, Bootstrap |
| **Database** | SQLite / PostgreSQL |
| **AI Integration** | Google Gemini API |
| **Environment Management** | Python Dotenv |
| **Version Control** | Git, GitHub |

---



## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/jibu-aji/OpenBook--IntelligentNews-SmarterConversations.git
cd openbook
