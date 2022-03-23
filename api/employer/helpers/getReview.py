import environ
import regex as re
import jwt as jwtLib
from employer.models import Vacancy 
from employee.models import Application, Profile
from employer.serializers import VacancySerializer
from employee.serializers import ApplicationSerializer, ProfileSerializer, SummaryProfileSerializer


env = environ.Env()


def extractJwt(request):
    # get jwt from request

    authToken = request.META.get('HTTP_AUTHORIZATION')
    authTokenRegex = re.compile(r'^Bearer: (.+\..+\..+)')

    jwtRegex = authTokenRegex.match(authToken)
    jwt = jwtRegex.group(1)

    jwt = jwtLib.decode(jwt, env('JWT_SECRET'), algorithms=['HS256'])

    return jwt



def checkUserOwnsVacancy(vacancyId, jwt):
    # check the user that made the request owns the vacancy that they are requesting the data for

    userId = jwt['id']

    vacancySet = Vacancy.objects.get(pk = vacancyId, UserId__exact = userId)
    vacancySerializer = VacancySerializer(vacancySet)
    vacancy = vacancySerializer.data

    if not vacancy:
        return False
    return vacancy



def getApplications(vacancyId):
    # get the matches and pending applications for review page

    matchesSet = Application.objects.filter(
        VacancyId__exact = vacancyId,
        ApplicationStatus__exact = 'MATCHED'
    )

    matchesSerializer = ApplicationSerializer(matchesSet, many = True)
    matches = matchesSerializer.data
    
    # pair matches with user profile
    richMatches = populateApplications(matches, SummaryProfileSerializer)


    newSet = Application.objects.filter(
        VacancyId__exact = vacancyId,
        ApplicationStatus__exact = 'PENDING'
    )

    newSerializer = ApplicationSerializer(newSet, many = True)
    new = newSerializer.data

    # pair new applications with user profile
    richNew = populateApplications(new, ProfileSerializer)

    return { 'matches': richMatches, 'new': richNew }



def populateApplications(matches, serializer):
    # pair matches with user profile

    pairedMatches = []

    for match in matches:
        profileSet = Profile.objects.get(UserId__exact = match['UserId'])
        profile = serializer(profileSet).data

        pairedMatches.append({
            'application': match,
            'profile': profile
        })
    
    return pairedMatches