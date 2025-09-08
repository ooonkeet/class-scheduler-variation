from django.shortcuts import render
from django.contrib import messages
from django.forms import formset_factory
from .forms import ConfigForm, SubjectForm, FacultyForm
from .scheduler_engine import build_schedule, format_schedule, DAYS

def index(request):
    SubjectFormSet = formset_factory(SubjectForm, extra=2)
    FacultyFormSet = formset_factory(FacultyForm, extra=2)

    if request.method == "POST":
        config_form = ConfigForm(request.POST)
        subject_formset = SubjectFormSet(request.POST, prefix="subjects")
        faculty_formset = FacultyFormSet(request.POST, prefix="faculty")

        if config_form.is_valid() and subject_formset.is_valid() and faculty_formset.is_valid():
            try:
                # Config values
                sections = config_form.cleaned_data["sections"]
                periods = config_form.cleaned_data["periods_per_day"]
                num_classrooms = config_form.cleaned_data["classrooms"]

                section_list = [chr(65 + i) for i in range(sections)]
                classrooms = [f"CR{i+1}" for i in range(num_classrooms)]

                # Subjects + weekly quota
                subjects = []
                weekly_quota = {}
                for form in subject_formset:
                    name = form.cleaned_data.get("name")
                    theory = form.cleaned_data.get("theory", 0)
                    practical = form.cleaned_data.get("practical", 0)
                    if name:
                        subjects.append(name)
                        weekly_quota[name] = {"T": theory, "P": practical}

                # Faculty mapping
                faculty = {}
                subject_to_fac = {}
                for form in faculty_formset:
                    fname = form.cleaned_data.get("name")
                    subj_list = form.cleaned_data.get("subjects")
                    if fname and subj_list:
                        fac_subjects = [s.strip() for s in subj_list.split(",") if s.strip()]
                        faculty[fname] = fac_subjects
                        for s in fac_subjects:
                            subject_to_fac[s] = fname

                # Build schedule
                schedules = build_schedule(
                    section_list, subjects, faculty, subject_to_fac,
                    weekly_quota, periods, classrooms
                )

                formatted = {sec: format_schedule(schedules[sec], periods) for sec in section_list}
                return render(request, "timetable.html", {
                    "schedules": formatted,
                    "days": DAYS,
                    "periods": range(periods)
                })

            except Exception as e:
                messages.error(request, f"Error: {e}")
    else:
        config_form = ConfigForm()
        subject_formset = SubjectFormSet(prefix="subjects")
        faculty_formset = FacultyFormSet(prefix="faculty")

    return render(request, "index.html", {
        "config_form": config_form,
        "subject_formset": subject_formset,
        "faculty_formset": faculty_formset
    })
