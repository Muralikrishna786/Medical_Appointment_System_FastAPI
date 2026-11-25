# 🏥 MediCare Clinic – Medical Appointment System (FastAPI)

A RESTful backend API built with **FastAPI** and **Python** for managing clinic doctors, dynamic consultation fee calculations, advanced search/filter/pagination workflows, and patient appointment bookings.

---

## 📁 Repository Structure

```text
Medical_Appointment_System_FastAPI/
├── Medical_Appointment_Output/   # Swagger UI screenshots & API test outputs
├── main.py                       # FastAPI app, Pydantic schemas, fee logic & routes
└── README.md                     # Project documentation
```

---

## ✨ Key Features

- **Doctor Directory & Analytics (`/doctors`):** View all doctors, track real-time availability, inspect clinic-wide summary statistics (`most_experienced`, `cheapest_fee`, specialization breakdown), add new doctors with duplicate checks, and update fees or availability.
- **Advanced Querying (`/doctors/browse`, `/filter`, `/search`, `/sort`, `/page`):** Filter doctors by specialization, maximum fee, minimum experience, and availability; search by keyword; sort by `fee`, `name`, or `experience_years`; and paginate results.
- **Dynamic Appointment Booking & Fee Engine (`/appointments`):**
  - Validates doctor existence and real-time availability before booking, automatically marking the doctor as unavailable once scheduled.
  - Calculates dynamic consultation fees based on appointment type (`video`: **20% discount**, `emergency`: **50% surcharge**, `in-person`: standard rate) plus an additional **15% senior citizen discount**.
- **Strict Pydantic Validation:** Enforces field lengths, positive numeric constraints, and literal appointment types (`in-person`, `video`, `emergency`) with alias support (`doctor_id` / `doctor id`).
- **Interactive API Docs:** Built-in Swagger UI (`/docs`) and ReDoc (`/redoc`) for live endpoint testing.

---

## 🛠️ Tech Stack

- **Framework:** FastAPI
- **Language:** Python 3.9+
- **Data Validation:** Pydantic (`BaseModel`, `Field`, `Literal`)
- **Server:** Uvicorn

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com
cd Medical_Appointment_System_FastAPI
```

### 2. Set Up Virtual Environment & Install Dependencies
```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install fastapi uvicorn pydantic
```

### 3. Start the Server
```bash
uvicorn main:app --reload
```
Open your browser and visit:
- **API Base URL:** `http://127.0.0.1:8000`
- **Swagger UI Docs:** `http://127.0.0`
- **ReDoc:** `http://127.0.0`

---

## 📌 API Endpoints Reference

### General & Doctors

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Clinic welcome & health check (`Welcome to MediCare Clinic`) |
| `GET` | `/doctors` | Get all doctors along with total and available counts |
| `GET` | `/doctors/summary` | Clinic analytics: available count, most experienced doctor, cheapest fee, and specialization counts |
| `GET` | `/doctors/browse` | Combined search (`keyword`), sorting (`sort_by`, `order`), and pagination (`page`, `limit`) |
| `GET` | `/doctors/filter` | Multi-criteria filter (`specialization`, `max_fee`, `min_experience`, `is_available`) |
| `GET` | `/doctors/search` | Case-insensitive keyword search across doctor names and specializations |
| `GET` | `/doctors/sort` | Sort doctors by `fee`, `name`, or `experience_years` |
| `GET` | `/doctors/page` | Paginated list of doctors (`page`, `limit`) |
| `GET` | `/doctors/{doctor_id}` | Fetch a single doctor's profile by ID |
| `POST` | `/doctors` | Register a new doctor (prevents duplicate names) |
| `PUT` | `/doctors/{doctor_id}` | Update a doctor's `fee` and/or `is_available` status |

### Appointments

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/appointments` | List all scheduled appointments |
| `POST` | `/appointments` | Book an appointment, apply dynamic pricing/discounts, and update doctor availability |

---

## 🧪 Example API Usage

### Book an Appointment (`POST /appointments`)

**Request Body:**
```json
{
  "patient_name": "Arjun Reddy",
  "doctor_id": 1,
  "date": "2026-11-28",
  "reason": "Routine cardiac checkup",
  "appointment_type": "video",
  "senior_citizen": true
}
```

**Sample Response (`200 OK`):**
```json
{
  "appointment_id": 1,
  "patient": "Arjun Reddy",
  "doctor": "Dr. Ravi",
  "doctor_id": 1,
  "date": "2026-11-28",
  "type": "video",
  "original_fee": 400,
  "final_fee": 340,
  "status": "scheduled"
}
```
*(Calculation: Base ₹500 → 20% video discount = ₹400 `original_fee` → 15% senior discount = ₹340 `final_fee`)*

---

## 📸 Output Screenshots

All Swagger UI execution screenshots and verified API responses are stored in the [`Medical_Appointment_Output`](./Medical_Appointment_Output) folder.

---

## 👤 Author

**Murali Krishna Ullikallu**  
- GitHub: [@Muralikrishna786](https://github.com)  
- Email: muralikrishnaullikallu@gmail.com
