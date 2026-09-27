print("CourseHub - Buoi 1")

students = [
    {"id": "22000001", "name": "Nguyen Minh Anh", "major": "KHDL"},
    {"id": "22000002", "name": "Tran Duc Long", "major": "KHDL"},
]
courses = [
    {
    "code": "INT2204",
    "name": "Co so du lieu Web va he thong thong tin",
    "capacity": 3,
    "enrolled": 2,
    },
    {
    "code": "INT2205",
    "name": "Khai pha du lieu",
    "capacity": 2,
    "enrolled": 2,
    },
]
enrollments = [
    {"student_id": "22000001", "course_code": "INT2204"}
]

for course in courses:
    remaining = course["capacity"] - course["enrolled"]
    print(course["code"], "- con", remaining, "cho")

def find_course(course_code):
    for course in courses:
        if course["code"] == course_code:
            return course
    return None

print(find_course("INT2204"))

def can_enroll(student_id, course_code):
    course = find_course(course_code)
    if course is None:
        return False, "Hoc phan khong ton tai"
    if not any(student["id"] == student_id for student in students):
        return False, "Sinh vien khong ton tai"
    
    duplicated = any(
        item["student_id"] == student_id and item["course_code"] == course_code
        for item in enrollments
    )
    if duplicated:
        return False, "Sinh vien da dang ky hoc phan nay"
    if course["enrolled"] >= course["capacity"]:
            return False, "Lop da du so luong"
    return True, "Co the dang ky"

print(can_enroll("22000001", "INT2204"))

try: 
    limit = int(input("Nhap so luong hoc phan muon hien thi:"))
    print(courses[:limit])
except ValueError:
    print("So luong phai la so nguyen")

def search_courses(keyword):
    normalized = keyword.strip().lower()
    results = []
    for course in courses:
        code = course["code"].lower()
        name = course["name"].lower()
        if normalized in code or normalized in name:
            results.append(course)
    return results

print(search_courses("web"))
#1. Hoàn thành hàm đăng ký học phần 
def enroll_student(student_id, course_code):
    can_enroll_result, message = can_enroll(student_id, course_code)
    if not can_enroll_result:
        return False, message
    enrollments.append({"student_id": student_id, "course_code": course_code})
    course = find_course(course_code)
    course["enrolled"] += 1
    return True, "Dang ky thanh cong"
#Kiểm tra chương trình
#TH1: Đăng ký thành công
result, message = enroll_student("22000002", "INT2204")
print(result, message)
#TH2: Đăng ký trùng
result, message = enroll_student("22000001", "INT2204")
print(result, message)
#TH3: Lớp đầy   
result, message = enroll_student("22000002", "INT2205")
print(result, message)
#TH4: Mã học phần không tồn tại
result, message = enroll_student("22000002", "INT2206")
print(result, message)  
#TH5: Mã sinh viên không tồn tại
result, message = enroll_student("22000003", "INT2204") 
print(result, message)
#3.

