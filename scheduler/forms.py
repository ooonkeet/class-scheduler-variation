from django import forms

# Single Subject form
class SubjectForm(forms.Form):
    name = forms.CharField(max_length=100, label="Subject Name")
    theory = forms.IntegerField(min_value=0, label="Theory Hours/Week")
    practical = forms.IntegerField(min_value=0, label="Practical Hours/Week")

# Single Faculty form
class FacultyForm(forms.Form):
    name = forms.CharField(max_length=100, label="Faculty Name")
    subjects = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Comma-separated subjects"}),
        label="Subjects"
    )

# Global scheduler config
class ConfigForm(forms.Form):
    sections = forms.IntegerField(min_value=1, label="Number of Sections")
    periods_per_day = forms.IntegerField(min_value=1, label="Periods per Day")
    classrooms = forms.IntegerField(min_value=1, label="Number of Classrooms")
