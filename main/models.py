from django.db import models
from django.db.models import Count
from django.utils.timezone import now


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.name


class Student(models.Model):
    full_name = models.CharField(max_length=200)
    user_id = models.CharField(max_length=6)
    photo = models.FileField(upload_to='profile_photos/', blank=True, null=True)
    cats = models.ManyToManyField(Category, related_name='students')
    first_p = models.IntegerField(blank=True, null=True, default=0)
    second_p = models.IntegerField(blank=True, null=True, default=0)
    third_p = models.IntegerField(blank=True, null=True, default=0)
    total_p = models.IntegerField(blank=True, null=True, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.full_name} - {self.user_id}"

    def save(self, *args, **kwargs):
        print('getting into students save function.')
        f = Result.objects.filter(first_place__id=self.id).count()
        print('f count is:', f)
        s = Result.objects.filter(second_place__id=self.id).count()
        t = Result.objects.filter(third_place__id=self.id).count()
        self.first_p = f
        self.second_p = s
        self.third_p = t
        self.total_p = self.first_p + self.second_p + self.third_p
        return super(Student, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total_p = self.first_p + self.second_p + self.third_p
        return super(Student, self).update(*args, **kwargs)
    
    class Meta:
        ordering = ['-total_p', '-first_p', '-second_p', '-third_p']


class Result(models.Model):
    title = models.CharField(max_length=200)
    first_place = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results_first_place')
    second_place = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True, related_name='results_second_place')
    third_place = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True, related_name='results_third_place')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='results')
    date = models.DateField(default=now, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.date} - {self.category} - {self.title}"

    def clean(self):
        if self.first_place == self.second_place or self.first_place == self.third_place or self.second_place == self.third_place:
            raise ValueError('Students have same names!')

    def save(self, *args, **kwargs):
        if self.first_place == self.second_place or self.first_place == self.third_place or self.second_place == self.third_place:
            raise ValueError('Students have same names!')
        if self.category not in self.first_place.cats.all():
            self.first_place.cats.add(self.category)  # Add the category to the first placed student's cats
        if self.category not in self.second_place.cats.all():
            self.second_place.cats.add(self.category)  # Add the category to the second placed student's cats
        if self.category not in self.third_place.cats.all():
            self.third_place.cats.add(self.category)  # Add the category to the third placed student's cats
        if self.id:
            old_result = Result.objects.get(pk=self.id)  # getting old result

        super(Result, self).save(*args, **kwargs) 
        # old results students saving
        try:
            old_result.first_place.save()
            old_result.second_place.save()
            old_result.third_place.save()
        except:
            print('no old result!')
        # new results students saving
        self.first_place.save()
        self.second_place.save()
        self.third_place.save()
    
    def delete(self, *args, **kwargs):
        r = Result.objects.get(id=self.id)
        super(Result, self).delete(*args, **kwargs)
        print(r, 'object is after deleting')
        r.first_place.save()
        r.second_place.save()
        r.third_place.save()

    class Meta:
        ordering = ['-date']
