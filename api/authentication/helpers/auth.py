from employee.models import Profile
from employer.models import EmployerDetails


def getEmployeeDetails(userId):
    return {}


def getEmployerDetails(userId):
    details = EmployerDetails.objects.get(UserId__exact = userId)

    return {
        'CompanyName': details.CompanyName
    }

