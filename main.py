from datetime import datetime

class HospitalError(Exception):
    pass

class PatientNotFound(HospitalError):
    def __init__(self, patient_id):
        self.message = f"Пацієнт з ID {patient_id} не знайдений."
        super().__init__(self.message)

class Patient:
    def __init__(self, patient_id, name, age, ailment):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.ailment = ailment

    def display_info(self):
        return f"ID: {self.patient_id}, Ім'я: {self.name}, Вік: {self.age}, Діагноз: {self.ailment}"

class Staff:
    def __init__(self, staff_id, name, position):
        self.staff_id = staff_id
        self.name = name
        self.position = position

    def perform_duties(self):
        raise NotImplementedError("Цей метод повинен бути перевизначений у підкласах.")

class Doctor(Staff):
    def __init__(self, staff_id, name, specialization):
        super().__init__(staff_id, name, "Лікар")
        self.specialization = specialization

    def perform_duties(self):
        return f"{self.name} проводить огляд пацієнтів. Спеціалізація: {self.specialization}"

class Nurse(Staff):
    def __init__(self, staff_id, name):
        super().__init__(staff_id, name, "Медсестра")

    def perform_duties(self):
        return f"{self.name} надає базовий догляд за пацієнтами."

class Hospital:
    def __init__(self, name):
        self.name = name
        self.patients = {}
        self.staff = []

    def add_patient(self, patient):
        self.patients[patient.patient_id] = patient
        print(f"Пацієнт {patient.name} успішно доданий.")

    def find_patient(self, patient_id):
        if patient_id not in self.patients:
            raise PatientNotFound(patient_id)
        return self.patients[patient_id]

    def add_staff(self, staff_member):
        self.staff.append(staff_member)
        print(f"Співробітник {staff_member.name} успішно доданий.")

    def list_patients(self):
        print("Список пацієнтів:")
        for patient in self.patients.values():
            print(patient.display_info())

    def list_staff(self):
        print("Список співробітників:")
        for staff_member in self.staff:
            print(f"ID: {staff_member.staff_id}, Ім'я: {staff_member.name}, Посада: {staff_member.position}")

    def save_patients_to_file(self, filename):
        try:
            with open(filename, "w") as file:
                for patient in self.patients.values():
                    file.write(f"{patient.patient_id},{patient.name},{patient.age},{patient.ailment}\n")
            print("Дані пацієнтів збережено до файлу.")
        except Exception as e:
            print(f"Помилка запису до файлу: {e}")

    def load_patients_from_file(self, filename):
        try:
            with open(filename, "r") as file:
                for line in file:
                    patient_id, name, age, ailment = line.strip().split(",")
                    self.add_patient(Patient(int(patient_id), name, int(age), ailment))
            print("Дані пацієнтів завантажено з файлу.")
        except Exception as e:
            print(f"Помилка читання з файлу: {e}")

if __name__ == "__main__":
    hospital = Hospital("Центральна лікарня")

    doctor = Doctor(1, "Вадим", "Кардіолог")
    nurse = Nurse(2, "Ігор")
    hospital.add_staff(doctor)
    hospital.add_staff(nurse)

    dog1 = Patient(101, "Юля", 39, "Грип")
    dog2 = Patient(102, "Даня", 55, "Мігрень")
    hospital.add_patient(dog1)
    hospital.add_patient(dog2)

    hospital.list_patients()
    hospital.list_staff()

    for staff_member in hospital.staff:
        print(staff_member.perform_duties())

    hospital.save_patients_to_file("patients.txt")

    new_hospital = Hospital("Нова лікарня")
    new_hospital.load_patients_from_file("patients.txt")
    new_hospital.list_patients()

    try:
        hospital.find_patient(999)
    except PatientNotFound as e:
        print(e)
