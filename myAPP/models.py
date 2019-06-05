from django.db import models

# Create your models here.

class arrangements(models.Model):
    id = models.IntegerField(primary_key=True)
    start_time = models.CharField(max_length=255)
    end_time = models.CharField(max_length=255)
    period = models.CharField(max_length=255)
    start_date = models.CharField(max_length=255)

class attendances(models.Model):
    id = models.IntegerField(primary_key=True)
    employee_id = models.IntegerField()
    arrive_at = models.CharField(max_length=255)
    leave_at = models.CharField(max_length=255)
    is_overtime = models.SmallIntegerField(max_length=4)
    reason = models.CharField(max_length=255)


# class auth_group(models.Model):
#     id = models.IntegerField(primary_key=True)
#     name = models.CharField(max_length=80)
#
# class auth_group_premissions(models.Model):
#     id = models.IntegerField(primary_key=True)
#     group_id = models.IntegerField(max_length=11)
#     permission_id = models.IntegerField(max_length=11)
#
# class auth_permission(models.Model):
#     id = models.IntegerField(primary_key=True)
#     name = models.CharField(max_length=255)
#     content_type_id = models.ForeignKey(a,on_delete = models.PROTECT)
#     condename = models.CharField(max_length=100)
#
# class auth_user(models.Model):
#     id = models.IntegerField(primary_key=True)
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(max_length=6)
#     is_superuser = models.SmallIntegerField(max_length=1)
#     username = models.CharField(max_length=150)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=150)
#     email = models.CharField(max_length=254)
#     is_staff = models.SmallIntegerField(max_length=1)
#     is_active = models.SmallIntegerField(max_length=1)
#     date_joined = models.DateTimeField(max_length=6)
#
# class auth_user_groups(models.Model):
#     id = models.IntegerField(primary_key=True)
#     user_id = models.ForeignKey(auth_user,on_delete = models.PROTECT)
#     group_id = models.ForeignKey(auth_group,on_delete = models.PROTECT)
#
# class auth_user_permissions(models.Model):
#     id = models.IntegerField(primary_key=True)
#     user_id = models.ForeignKey(auth_user,on_delete = models.PROTECT)
#     permission_id = models.ForeignKey(auth_permission,on_delete = models.PROTECT)

class departments(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    director_id = models.IntegerField()

class employees(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=11)
    birthday = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    department_id = models.ForeignKey(departments,on_delete = models.PROTECT)
    arrange_id = models.ForeignKey(arrangements,on_delete = models.PROTECT)

#测试时使用的表，不要轻易删除
class empyt(models.Model):
    test = models.IntegerField(primary_key=True)

class leaves(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.SmallIntegerField(max_length=4)
    status = models.SmallIntegerField(max_length=4)
    start_date = models.CharField(max_length=255)
    end_date = models.CharField(max_length=255)
    reason = models.CharField(max_length=255)
    employee_id = models.ForeignKey(employees,on_delete = models.CASCADE)

class managers(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

class overtimes(models.Model):
    id = models.IntegerField(primary_key=True)
    start_time = models.CharField(max_length=255)
    end_time = models.CharField(max_length=255)
    date = models.CharField(max_length=255)

class temp_arrangements(models.Model):
    id = models.IntegerField(primary_key=True)
    start_time = models.CharField(max_length=255)
    end_time = models.CharField(max_length=255)
    start_date = models.CharField(max_length=255)
    end_date = models.CharField(max_length=255)
    employee_id = models.ForeignKey(employees,on_delete = models.CASCADE)

#departments.id = models.ForeignKey(employees,on_delete = models.SET_NULL)
