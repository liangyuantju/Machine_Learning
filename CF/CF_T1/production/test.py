#-*-coding:utf8-*-
import math
import operator

def test_sqrt(a):
    print("sqrt(a)=%s"%math.sqrt(a))

def test_travers_dict(d):
    for item in d:
        print(item)

def test_sort_func(d):
    d_sorted = {}
    for itemid in d:
        d_sorted[itemid] = sorted(d[itemid].items(), key=operator.itemgetter(1), reverse=True)
    print(d_sorted)

class Students:
    def __init__(self, name, grade, age):
        self.name = name
        self.grade = grade
        self.age = age
    # def __repr__(self):
    #     return repr(self.name, self.grade, self.age)

student_objects = [
    Students('john', 'A', 15),
    Students('jane', 'C', 12),
    Students('dave', 'B', 13)
]

def test_sorted_func():
    students = [('john', 'A', 15), ('jane', 'C', 12), ('dave', 'B', 10)]
    b = sorted(students, key=operator.itemgetter(1))
    
    c = sorted(student_objects, key=operator.attrgetter('age'))
    for stu in c:
        print(stu.name, stu.grade, stu.age)

def test_items_module():
    d = {"1":["liang_1", "liang_2"], "2":["yuan_1", "yuan_2"]}
    for [num, namelist] in d.items():
        print("num:%s name:%s"%(num, namelist))
        print("type(num):%s type(namelist):%s"%(type(num), type(namelist)))

if __name__ == "__main__":
    list1 = [1,2,3,4,5,6,7,8,9]
    list2 = list1[:5]
    print(list2)



