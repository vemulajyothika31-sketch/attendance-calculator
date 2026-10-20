import streamlit as st


def calculate_percentage(a, t):
    return a / t * 100


def validate(a, t, target):
    if t <= 0:
        return "Total classes must be more than 0"
    elif a < 0:
        return "Attended classes can't be negative"
    elif a > t:
        return "Attended classes can't be more than total classes"
    return None


def classes_can_skip(a, t, target):
    n = 0
    A = calculate_percentage(a, t)
    while A >= target:
        t = t + 1
        n = n + 1
        A = calculate_percentage(a, t)
    return n - 1


def classes_to_attend(a, t, target):
    if target >= 100:
        return None
    n = 0
    A = calculate_percentage(a, t)
    while A < target:
        t = t + 1
        a = a + 1
        n = n + 1
        A = calculate_percentage(a, t)
    return n


def check_attendance(a, t, target=75):
    error = validate(a, t, target)
    if error:
        return error
    A = calculate_percentage(a, t)
    if A >= target:
        return f"You can skip {classes_can_skip(a, t, target)} classes"
    else:
        n = classes_to_attend(a, t, target)
        if n is None:
            return "This target can't be reached"
        return f"You need to attend {n} more classes"


# ---------- multi-subject part (Streamlit version) ----------

st.title("Wanna know which classes u wanna bunk?, without dropping ur attendance below 75%?")

subject_names = ["Maths", "Mechanics", "IBD", "FIH", "MOM",
                 "Computational Thinking", "EEE", "Tech Com", "EOC"]

subjects = []

for name in subject_names:
    st.subheader(name)
    col1, col2 = st.columns(2)
    a = col1.number_input("Classes attended", min_value=0, step=1, key="a_" + name)
    t = col2.number_input("Total classes", min_value=0, step=1, key="t_" + name)
    subjects.append({"name": name, "attended": a, "total": t})

st.divider()
st.header("Your attendance")

for s in subjects:
    result = check_attendance(s["attended"], s["total"])
    if validate(s["attended"], s["total"], 75) is None:
        percent = calculate_percentage(s["attended"], s["total"])
        st.write(f"**{s['name']}** : {percent:.2f}% - {result}")
    else:
        st.write(f"**{s['name']}** : {result}")