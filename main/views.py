from django.shortcuts import render, get_object_or_404
from . import models

import datetime
import math


def result_list(request):
    results = models.Result.objects.all()
    categories = models.Category.objects.all()
    return render(request, 'html/list_results.html', {'results': results, 'categories': categories})


def student_list(request):
    students = models.Student.objects.all()
    categories = models.Category.objects.all()
    return render(request, 'html/list_students.html', {'students': students, 'categories': categories})



def home(request):
    students_list = models.Student.objects.all()[:10]
    resutls = models.Result.objects.all()[:9]
    categories = models.Category.objects.all()
    return render(request, 'html/index.html', {'students': students_list, 'results': resutls, 'categories': categories})


def account(request, id=None):
    faculties = {'1': "Hukuk Fakulteti", "2": "Maglumat Howpsuzlygy Fakulteti"}
    student = get_object_or_404(models.Student, pk=id)
    categories = student.cats.all()
    faculty = faculties[student.user_id[2]]
    inner_date = datetime.datetime(2000 + int(student.user_id[:2]), 8, 25)
    year = datetime.datetime.now() - inner_date
    yearth = math.ceil(year.days/365)
    content = {}
    content['f_ps'] = models.Result.objects.filter(first_place=student)
    content['s_ps'] = models.Result.objects.filter(second_place=student)
    content['t_ps'] = models.Result.objects.filter(third_place=student)
    return render(request, 'html/account.html', {
        'student': student, 'faculty': faculty, 
        "year": yearth, "content": content,
        "categories": categories,
        })


def by_category(request, cat_id):
    categories = models.Category.objects.all()
    current = categories.get(pk=cat_id)
    students = current.students.all()
    results = current.results.all()
    for st in students:
        st.first_p = st.results_first_place.filter(category=current.id).count()
        st.second_p = st.results_second_place.filter(category=current.id).count()
        st.third_p = st.results_third_place.filter(category=current.id).count()
        st.total_p = st.first_p + st.second_p + st.third_p
        st = st

    return render(request, 'html/index.html', {
        'students': students,
        'results': results,
        'categories': categories,
        'current': current
    })

