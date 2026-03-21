from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, Literal
import math

from datetime import datetime
date: datetime

app = FastAPI()


# DATA (acts like database)

doctors = [
    {"id": 1, "name": "Dr. Ravi", "specialization": "Cardiologist", "fee": 500, "experience_years": 10, "is_available": True},
    {"id": 2, "name": "Dr. Meena", "specialization": "Dermatologist", "fee": 300, "experience_years": 7, "is_available": True},
    {"id": 3, "name": "Dr. Kumar", "specialization": "Pediatrician", "fee": 400, "experience_years": 12, "is_available": False},
    {"id": 4, "name": "Dr. Anil", "specialization": "General", "fee": 200, "experience_years": 5, "is_available": True},
    {"id": 5, "name": "Dr. Sneha", "specialization": "Cardiologist", "fee": 600, "experience_years": 15, "is_available": True},
    {"id": 6, "name": "Dr. John", "specialization": "Dermatologist", "fee": 350, "experience_years": 8, "is_available": False},
]

appointments = []
appt_counter = 1



# MODELS

class AppointmentRequest(BaseModel):
    patient_name: str = Field(..., min_length=2)
    doctor_id: int = Field(..., gt=0, alias="doctor id")
    date: str = Field(..., min_length=8)
    reason: str = Field(..., min_length=5)
    appointment_type: Literal["in-person", "video", "emergency"] = "in-person"
    senior_citizen: bool = False

    class Config:
        populate_by_name = True


class NewDoctor(BaseModel):
    name: str = Field(..., min_length=2)
    specialization: str = Field(..., min_length=2)
    fee: int = Field(..., gt=0)
    experience_years: int = Field(..., gt=0)
    is_available: bool = True



# HELPER FUNCTIONS

def find_doctor(doctor_id: int):
    for doc in doctors:
        if doc["id"] == doctor_id:
            return doc
    return None


def calculate_fee(base_fee, appointment_type, senior=False):
    fee = base_fee

    if appointment_type == "video":
        fee *= 0.8
    elif appointment_type == "emergency":
        fee *= 1.5

    original_fee = fee

    if senior:
        fee *= 0.85

    return int(original_fee), int(fee)


def filter_doctors_logic(doctors, specialization, max_fee, min_exp, is_available):
    result = doctors

    if specialization is not None:
        result = [d for d in result if d["specialization"].lower() == specialization.lower()]

    if max_fee is not None:
        result = [d for d in result if d["fee"] <= max_fee]

    if min_exp is not None:
        result = [d for d in result if d["experience_years"] >= min_exp]

    if is_available is not None:
        result = [d for d in result if d["is_available"] == is_available]

    return result


# Q1 - HOME

@app.get("/")
def home():
    return {"message": "Welcome to MediCare Clinic"}



# Q2 - GET ALL DOCTORS

@app.get("/doctors")
def get_doctors():
    return {
        "total": len(doctors),
        "available_count": sum(d["is_available"] for d in doctors),
        "data": doctors
    }



# Q5 - SUMMARY (IMPORTANT: ABOVE ID ROUTE)

@app.get("/doctors/summary")
def summary():
    most_exp = max(doctors, key=lambda x: x["experience_years"])
    cheapest = min(doctors, key=lambda x: x["fee"])

    spec_count = {}
    for d in doctors:
        spec_count[d["specialization"]] = spec_count.get(d["specialization"], 0) + 1

    return {
        "total": len(doctors),
        "available": sum(d["is_available"] for d in doctors),
        "most_experienced": most_exp["name"],
        "cheapest_fee": cheapest["fee"],
        "specialization_count": spec_count
    }




# Q20 - COMBINED (SEARCH + SORT + PAGINATION)

@app.get("/doctors/browse")
def browse(
    keyword: Optional[str] = Query(None),
    sort_by: str = Query("fee"),
    order: str = Query("asc"),
    page: int = Query(1, ge=1),
    limit: int = Query(4, ge=1)
):
    # Step 1: Filter by keyword
    result = doctors
    if keyword:
        result = [
            d for d in result
            if keyword.lower() in d["name"].lower()
            or keyword.lower() in d["specialization"].lower()
        ]

    # Step 2: Validate sort_by field
    if sort_by not in ["fee", "name", "experience_years"]:
        raise HTTPException(400, "Invalid sort field. Choose from: fee, name, experience_years")

    # Step 3: Validate order direction
    if order not in ["asc", "desc"]:
        raise HTTPException(400, "Invalid order. Choose from: asc, desc")

    # Step 4: Sort results
    reverse = True if order == "desc" else False
    result = sorted(result, key=lambda x: x[sort_by], reverse=reverse)

    # Step 5: Paginate
    total = len(result)
    start = (page - 1) * limit
    end = start + limit

    return {
        "total": total,
        "page": page,
        "total_pages": math.ceil(total / limit),
        "limit": limit,
        "data": result[start:end]
    }



# Q10 - FILTER DOCTORS

@app.get("/doctors/filter")
def filter_docs(
    specialization: Optional[str] = Query(None),
    max_fee: Optional[int] = Query(None),
    min_experience: Optional[int] = Query(None),
    is_available: Optional[str] = Query(None)
):
    # Convert string to boolean for is_available
    is_available_bool = None
    if is_available is not None:
        is_available_bool = is_available.lower() in ['true', '1', 'yes']
    
    result = filter_doctors_logic(doctors, specialization, max_fee, min_experience, is_available_bool)
    return {"total": len(result), "data": result}



# Q16 - SEARCH DOCTORS

@app.get("/doctors/search")
def search(keyword: str):
    res = [
        d for d in doctors
        if keyword.lower() in d["name"].lower()
        or keyword.lower() in d["specialization"].lower()
    ]
    if not res:
        return {"message": "No doctors found"}
    return {"total_found": len(res), "data": res}



# Q17 - SORT DOCTORS

@app.get("/doctors/sort")
def sort_docs(sort_by: str = "fee"):
    if sort_by not in ["fee", "name", "experience_years"]:
        raise HTTPException(400, "Invalid sort field")

    return sorted(doctors, key=lambda x: x[sort_by])



# Q18 - PAGINATION

@app.get("/doctors/page")
def paginate(page: int = 1, limit: int = 3):
    total = len(doctors)
    start = (page - 1) * limit
    end = start + limit

    return {
        "page": page,
        "total_pages": math.ceil(total / limit),
        "data": doctors[start:end]
    }



# Q3 - GET DOCTOR BY ID

@app.get("/doctors/{doctor_id}")
def get_doctor(doctor_id: int):
    doc = find_doctor(doctor_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doc



# Q4 - GET APPOINTMENTS

@app.get("/appointments")
def get_appointments():
    return {"total": len(appointments), "data": appointments}



# Q8 + Q9 - CREATE APPOINTMENT

@app.post("/appointments")
def create_appointment(req: AppointmentRequest):
    global appt_counter

    doc = find_doctor(req.doctor_id)
    if not doc:
        raise HTTPException(404, "Doctor not found")

    if not doc["is_available"]:
        raise HTTPException(400, "Doctor not available")

    original_fee, final_fee = calculate_fee(
        doc["fee"], req.appointment_type, req.senior_citizen
    )

    appt = {
        "appointment_id": appt_counter,
        "patient": req.patient_name,
        "doctor": doc["name"],
        "doctor_id": doc["id"],
        "date": req.date,
        "type": req.appointment_type,
        "original_fee": original_fee,
        "final_fee": final_fee,
        "status": "scheduled"
    }

    appointments.append(appt)
    appt_counter += 1
    doc["is_available"] = False

    return appt



# Q11 - ADD DOCTOR

@app.post("/doctors", status_code=201)
def add_doctor(new_doc: NewDoctor):
    for d in doctors:
        if d["name"].lower() == new_doc.name.lower():
            raise HTTPException(400, "Doctor already exists")

    new_id = max(d["id"] for d in doctors) + 1
    doc = new_doc.dict()
    doc["id"] = new_id

    doctors.append(doc)
    return doc



# Q12 - UPDATE DOCTOR

@app.put("/doctors/{doctor_id}")
def update_doc(
    doctor_id: int,
    fee: Optional[int] = None,
    is_available: Optional[bool] = None
):
    doc = find_doctor(doctor_id)
    if not doc:
        raise HTTPException(404, "Doctor not found")

    if fee is not None:
        doc["fee"] = fee
    if is_available is not None:
        doc["is_available"] = is_available

    return doc



# Q13 - DELETE DOCTOR

@app.delete("/doctors/{doctor_id}")
def delete_doc(doctor_id: int):
    doc = find_doctor(doctor_id)
    if not doc:
        raise HTTPException(404, "Doctor not found")

    for appt in appointments:
        if appt["doctor_id"] == doctor_id and appt["status"] == "scheduled":
            raise HTTPException(400, "Doctor has active appointments")

    doctors.remove(doc)
    return {"message": "Doctor deleted successfully"}



# Q14 & Q15 - STATUS MANAGEMENT


@app.post("/appointments/{appointment_id}/confirm")
def confirm(appointment_id: int):
    for a in appointments:
        if a["appointment_id"] == appointment_id:
            a["status"] = "confirmed"
            return a
    raise HTTPException(404, "Appointment not found")


@app.post("/appointments/{appointment_id}/cancel")
def cancel(appointment_id: int):
    for a in appointments:
        if a["appointment_id"] == appointment_id:
            a["status"] = "cancelled"
            doc = find_doctor(a["doctor_id"])
            doc["is_available"] = True
            return a
    raise HTTPException(404, "Appointment not found")


@app.post("/appointments/{appointment_id}/complete")
def complete(appointment_id: int):
    for a in appointments:
        if a["appointment_id"] == appointment_id:
            a["status"] = "completed"
            return a
    raise HTTPException(404, "Appointment not found")


@app.get("/appointments/active")
def active():
    return [a for a in appointments if a["status"] in ["scheduled", "confirmed"]]


@app.get("/appointments/by-doctor/{doctor_id}")
def by_doc(doctor_id: int):
    return [a for a in appointments if a["doctor_id"] == doctor_id]
