import pickle
import numpy as np
from django.shortcuts import render

model = pickle.load(open("stress_models_final.pkl", "rb"))

def yn(val):
    """Yes = 8, No = 2  (model ke 1-10 scale ke mutabiq)"""
    return 8.0 if val == "yes" else 2.0

def home(request):
    result = description = score = tips = None

    if request.method == "POST":
        financial_stress = yn(request.POST.get("financial_stress"))
        peer_pressure    = yn(request.POST.get("peer_pressure"))
        cognitive_dist   = yn(request.POST.get("cognitive_dist"))
        relationship_str = yn(request.POST.get("relationship_str"))
        gpa              = float(request.POST.get("gpa", 0))
        sleep_hours      = float(request.POST.get("sleep_hours", 0))
        study_hours      = float(request.POST.get("study_hours", 0))
        social_media     = float(request.POST.get("social_media", 0))
        exercise_hours   = float(request.POST.get("exercise_hours", 0))
        financial_sq     = financial_stress ** 2

        data = np.array([[
            financial_stress, peer_pressure, cognitive_dist,
            relationship_str, gpa, sleep_hours, study_hours,
            social_media, exercise_hours, financial_sq
        ]])

        pred = int(model.predict(data)[0])

        if pred == 0:
            result      = "Low"
            score       = 2
            description = "You are mentally stable and handling daily tasks well. No major pressure detected."
            tips        = ["Maintain your regular sleep schedule", "Keep up your exercise routine", "Celebrate your consistency"]
        elif pred == 1:
            result      = "Medium"
            score       = 5
            description = "You are experiencing moderate stress. Some pressure is present but manageable with the right habits."
            tips        = ["Take a 30-minute walk daily", "Reduce social media screen time", "Talk to a trusted friend or mentor"]
        else:
            result      = "High"
            score       = 9
            description = "You are under significant mental pressure. This may affect your health and academic performance."
            tips        = ["Consider speaking with a counselor", "Prioritize 7–8 hours of sleep each night", "Take regular breaks during study sessions"]

    return render(request, "index.html", {
        "result": result, "score": score,
        "description": description, "tips": tips
    })