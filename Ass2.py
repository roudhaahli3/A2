from collections import deque

class Doctor:
    '''class to represent a doctor'''
    def __init__(self, doctor_id, name, specialization):
        # Initializing the constructor (attributes of a real doctor)
        self.doctor_id = doctor_id
        self.name = name
        self.specialization = specialization

# Example of doctors
doctors = {
    "D001": Doctor("D001", "Dr. Smith", "General"),
    "D002": Doctor("D002", "Dr. Johnson", "Cardiologist"),
    "D003": Doctor("D003", "Dr. Lee", "Dermatologist")
}
class Patient:
    '''class to represent a patient'''
    # Add a new patient record, including personal details, medical history, and current condition.
    def __init__(self, patient_id, name, age, medical_history=None, current_condition=None): # none so that the user can enter it
        # Initializing the constructor (attributes of a real patient)
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.medical_history = medical_history if medical_history else [] #if provided set to its value, if not empty list
        self.current_condition = current_condition

    #Update an existing patient record with new information or medical updates
    def update_medical_history(self, new_entry):
        # Update patient's medical history with a new entry
        self.medical_history.append(new_entry)

    def update_condition(self, new_condition):
        # Update patient's current medical condition
        self.current_condition = new_condition

# Example of patients
patients = {
    "P001": Patient("P001", "Fatma Baharoon", 18),
    "P002": Patient("P002", "Hind Ahli", 19, ["Allergy to penicillin"], "Fever"),
    "P003": Patient("P003", "Roudha Ahli", 19)
}

class PatientRecordSystem:
    '''class to represent the patient record system that can be modified'''
    def __init__(self):
        # Initializing the constructor (patient record system attributes)
        self.patients = {} # Dictionary to store patient records
        self.appointment_schedule = {} # Dictionary to store appointments
        self.consultation_queue = deque()  # Queue to manage patients waiting for consultation (FIFO)
        self.prescription_stack = []  # Stack to manage issued prescriptions

    # Add a new patient record
    def add_patient_record(self, patient_id, name, age, medical_history=None, current_condition=None):
        new_patient = Patient(patient_id, name, age, medical_history, current_condition)
        self.patients[patient_id] = new_patient # adding it to the dictionary
        return new_patient

    # Update an existing patient record with new information or medical updates in the class of record system
    def update_patient_record(self, patient_id, **kwargs):# **kwargs = additional keyword arguments
        if patient_id in self.patients: # if the patient id is in the patient dictionary
            patient = self.patients[patient_id] # retrieves it
            # Iterate over each key-value pair in kwargs
            for key, value in kwargs.items():
                setattr(patient, key, value)

    # Remove a patient record from the queue upon discharge or transfer to another facility
    def remove_patient_from_queue(self, patient_id):
        if patient_id in self.consultation_queue: # if the patient id is in consultation queue
            self.consultation_queue.remove(patient_id) # remove the patient record

    # Schedule an appointment for a patient with a specific doctor
    def schedule_appointment(self, patient_id, doctor_id):
        # Assign the doctor_id to the patient_id in the appointment_schedule dictionary
        self.appointment_schedule[patient_id] = doctor_id
        self.consultation_queue.append(patient_id)

    # Issue medical prescriptions to patients during consultation and manage the stack of prescriptions.
    def issue_prescription(self, patient_id, medication):
        # Check if the patient_id exists in the patients dictionary
        if patient_id in self.patients:
            # Create a prescription tuple containing the patient_id and the medication
            prescription = (patient_id, medication)
            # Add the prescription to the prescription_stack
            self.prescription_stack.append(prescription)
            return True # successful prescription issuance
        return False # patient_id is not found in the patients dictionary

    # Search for a patient and display a summary including their personal details, the doctor who will attend to them, their appointment details, and their medications.
    def search_patient_summary(self, patient_id):
        if patient_id in self.patients: # if the patient_id exists in the patients dictionary
            patient = self.patients[patient_id] # Retrieve the patient object associated with the patient_id
            doctor_id = self.appointment_schedule.get(patient_id)  # Get the doctor ID from the appointment_schedule dictionary
            # Retrieve medications prescribed to the patient by filtering the prescription_stack
            medications = [prescription[1] for prescription in self.prescription_stack if prescription[0] == patient_id]
            summary = {
                'Personal Details': {
                    'Name': patient.name,
                    'Age': patient.age
                },
                'Doctor': doctor_id,
                'Appointment Details': self.appointment_schedule.get(patient_id, "Not scheduled"),
                'Medications': medications
            }
            return summary
        else:
            return None

    # Menu-based interface demonstrating how the system works
    def menu_interface(self):
        while True:
            # Display menu options
            print("Patient Record System Menu:")
            print("1. Add Patient Record")
            print("2. Update Patient Record")
            print("3. Remove Patient from Queue")
            print("4. Schedule Appointment")
            print("5. Issue Prescription")
            print("6. Search Patient Summary")
            print("7. Exit")

            # Get user input
            choice = input("Enter your choice (1-7): ")

            # Process user choice
            if choice == "1":
                # Add Patient Record
                patient_id = input("Enter patient ID: ")
                name = input("Enter patient name: ")
                age = input("Enter patient age: ")
                self.add_patient_record(patient_id, name, age)
                print("Patient record added successfully.")
            elif choice == "2":
                # Update Patient Record
                patient_id = input("Enter patient ID to update: ")
                medical_history = input("Enter new medical history (leave blank to keep current): ")
                current_condition = input("Enter new current condition (leave blank to keep current): ")
                if medical_history or current_condition:
                    kwargs = {}
                    if medical_history:
                        kwargs['medical_history'] = medical_history
                    if current_condition:
                        kwargs['current_condition'] = current_condition
                        self.update_patient_record(patient_id, **kwargs)
                        print("Patient record updated successfully.")
                else:
                    print("No changes made.")
            elif choice == "3":
                # Remove Patient from Queue
                patient_id = input("Enter patient ID to remove from queue: ")
                self.remove_patient_from_queue(patient_id)
                print("Patient removed from queue successfully.")
            elif choice == "4":
                # Schedule Appointment
                patient_id = input("Enter patient ID to schedule appointment: ")
                doctor_id = input("Enter doctor ID: ")
                self.schedule_appointment(patient_id, doctor_id)
                print("Appointment scheduled successfully.")
            elif choice == "5":
                # Issue Prescription
                patient_id = input("Enter patient ID to issue prescription: ")
                medication = input("Enter medication: ")
                success = self.issue_prescription(patient_id, medication)
                if success:
                    print("Prescription issued successfully.")
                else:
                    print("Failed to issue prescription. Patient ID not found.")
            elif choice == "6":
                # Search Patient Summary
                patient_id = input("Enter patient ID to search summary: ")
                summary = self.search_patient_summary(patient_id)
                if summary:
                    print("Patient Summary:")
                    for key, value in summary.items():
                        print(f"{key}: {value}")
                else:
                    print("Patient not found.")
            elif choice == "7":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 7.")

# Instantiate PatientRecordSystem object
patient_system = PatientRecordSystem()

# Run the menu interface
patient_system.menu_interface()

