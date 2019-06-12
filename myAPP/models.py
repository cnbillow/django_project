from django.db import models

# Create your models here.

class arrangements(models.Model):
    day=models.CharField(max_length=255,default="-")
    employee_id = models.IntegerField(default=0)
    start_time_am = models.CharField(max_length=255,default='-')
    end_time_am = models.CharField(max_length=255,default='-')
    start_time_pm = models.CharField(max_length=255,default='-')
    end_time_pm = models.CharField(max_length=255,default='-')

class attendances(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=11,default="user")
    employee_id = models.IntegerField()
    arrive_at = models.CharField(max_length=255)
    leave_at = models.CharField(max_length=255)
    is_overtime = models.SmallIntegerField(max_length=4)
    reason = models.CharField(max_length=255)

class departments(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    employee_id = models.IntegerField(default=0)

class employees(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=11)
    birthday = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    department_id = models.ForeignKey(departments,on_delete = models.PROTECT)
    #arrange_id = models.ForeignKey(arrangements,on_delete = models.PROTECT)

#测试时使用的表，不要轻易删除
class empyt(models.Model):
    test = models.IntegerField(primary_key=True)

class leaves(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.SmallIntegerField(max_length=4)
    status = models.SmallIntegerField(max_length=4)
    start_time = models.CharField(max_length=255)
    end_time = models.CharField(max_length=255)
    reason = models.CharField(max_length=255)
    employee_id = models.ForeignKey(employees,on_delete = models.CASCADE)

class managers(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthday = models.CharField(max_length=255,default='')

class overtimes(models.Model):
    id = models.IntegerField(primary_key=True)
    start_time = models.CharField(max_length=255)
    end_time = models.CharField(max_length=255)
    reason = models.CharField(max_length=255,default='')
    status = models.SmallIntegerField(max_length=4,default=0)
    employee_id = models.ForeignKey(employees, on_delete=models.CASCADE,default=0)

class temp_arrangements(models.Model):
    id = models.IntegerField(primary_key=True)
    start_time = models.CharField(max_length=255)
    end_time = models.CharField(max_length=255)
    start_date = models.CharField(max_length=255)
    end_date = models.CharField(max_length=255)
    employee_id = models.ForeignKey(employees,on_delete = models.CASCADE)

departments.employee_id = models.ForeignKey(employees,on_delete = models.SET_NULL)
