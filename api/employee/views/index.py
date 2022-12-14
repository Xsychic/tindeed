from math import ceil
from rest_framework import status
from django.db.models import Count, Q
from ..serializers import RejectSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from authentication.helpers import jwt as jwtHelper
from employer.models import EmployerDetails, Vacancy, Tag
from employee.models import Application, Favourite, Reject
from employer.serializers import VacancySerializer, TagSerializer



@api_view(['GET'])
def getIndex(request):

    params = request.query_params

    jwt = jwtHelper.extractJwt(request)

    if type(jwt) is not dict:
        try:
            noAuth = params['noAuth']

            if not noAuth or noAuth.lower() != 'true':
                return jwt
            else:
                return getIndexNoAuth(request)
        except:
            return jwt


    # get query params: sort, count, filter, pageNum, tags, searchValue

    # destructure params and typecast
    try:
        sort = params['sort']
        filter = params['filter']
        count = int(params['count'])
        pageNum = int(params['pageNum'])
        tags = params['tagsFilter']
        searchValue = params['searchValue']
    except:
        return Response(data={'status': 400, 'message': 'incomplete request data'}, status=status.HTTP_400_BAD_REQUEST)

    tagListInt = []

    if len(tags) < 1:
        tags = 'null'

    if tags != 'null':
        tagList = tags.split(',')

        for tag in tagList:
            tagListInt.append(int(tag))


    # parse sort parameter into django sort parameter
    if sort == 'dateDesc':
        sortParam = '-Created'
    elif sort == 'dateAsc':
        sortParam = 'Created'
    elif sort == 'titleAsc':
        sortParam = 'VacancyName'
    else:
        # 'titleDesc'
        sortParam = '-VacancyName'

    # parse filter parameter into django filter parameter
    if filter == 'closed':
        filterParam = [False]
    elif filter == 'active':
        filterParam = [True]
    else:
        # 'all'
        filterParam = [True, False]


    usingTags = False
    triedTags = False

    try:
        # get number of pages

        vacancyList = []

        favouriteSet = Favourite.objects.filter(
            UserId__exact = jwt['id']
        )

        rejectSet = Reject.objects.filter(
            UserId__exact = jwt['id']
        )

        applicationSet = Application.objects.filter(
            UserId__exact = jwt['id']
        )

        for fav in favouriteSet:
            vacancyList.append(fav.VacancyId.VacancyId)

        for rej in rejectSet:
            vacancyList.append(rej.VacancyId.VacancyId)

        for app in applicationSet:
            vacancyList.append(app.VacancyId.VacancyId)

        if tags != 'null':
            dbSet = Vacancy.objects.filter(
                IsOpen__in = filterParam,
                Tags__contains = tagListInt,
                VacancyName__contains = searchValue
            ).exclude(
                VacancyId__in = vacancyList
            )

            numVacancies = dbSet.count()

            if numVacancies > 0:
                usingTags = True
            else:
                triedTags = True

        if tags == 'null' or usingTags == False:
            dbSet = Vacancy.objects.filter(
                IsOpen__in = filterParam,
                VacancyName__contains = searchValue
            ).exclude(
                VacancyId__in = vacancyList
            )

            numVacancies = dbSet.count()

        pages = int(ceil(numVacancies / int(params['count'])))
        
        # deals with a lower number of pages than the current page
        while (pageNum - 1) * count >= numVacancies and pageNum > 1:
            pageNum -= 1

    except Exception as err:
        print(f'uh oh: { err }')
        return Response(data={'status': 500, 'message': 'Server error counting vacancies'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    skip = max(count * (pageNum - 1), 0)
    limit = count * pageNum

    try:
        # order vacancies
        vacanciesSet = dbSet.order_by(sortParam)[skip:limit]

        vacancySerializer = VacancySerializer(vacanciesSet, many=True)
        vacancies = vacancySerializer.data

    except Exception as err:
        print(f'uh oh: { err }')
        return Response(data={'status': 500, 'message': 'Server error fetching vacancies'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    try:
        # get company name
        for vacancy in vacancies:
            employerDetails = EmployerDetails.objects.get(UserId__exact = vacancy['UserId'])
            vacancy['CompanyName'] = employerDetails.CompanyName

    except EmployerDetails.DoesNotExist:
        return Response(data={'code': 500, 'message': 'error getting company name for vacancy'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as err:
        print(f'uh oh: { err }')
        return Response(data={'code': 500, 'message': 'Server error getting company name and stats'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # compile return data and send response
    returnData = {
        'numPages': pages,
        'vacancies': vacancies,
        'numVacancies': numVacancies,
        'triedTags': triedTags
    }

    return Response(returnData, status=status.HTTP_200_OK)



def getIndexNoAuth(request):
    # get requested number of the most popular vacancies without auth

    # destructure params and typecast
    try:
        count = int(request.query_params['count'])
    except:
        return Response(data={'status': 400, 'message': 'request params missing valid count value'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # sort by the number of applications referencing vacancy
        vacanciesSet = Vacancy.objects.filter(
            IsOpen__exact = True
        ).annotate(
            applicationCount = Count('application', filter=Q(application__ApplicationStatus__exact='PENDING'))
        ).order_by(
            '-applicationCount'
        )[:count]

        vacancySerializer = VacancySerializer(vacanciesSet, many=True)
        vacancies = vacancySerializer.data

    except Exception as err:
        print(f'uh oh: { err }')
        return Response(data={'status': 500, 'message': 'Server error fetching vacancies'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    try:
        # get company name
        for vacancy in vacancies:
            employerDetails = EmployerDetails.objects.get(UserId__exact = vacancy['UserId'])
            vacancy['CompanyName'] = employerDetails.CompanyName

    except EmployerDetails.DoesNotExist:
        return Response(data={'code': 500, 'message': 'error getting company name for vacancy'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as err:
        print(f'uh oh: { err }')
        return Response(data={'code': 500, 'message': 'Server error getting company name and stats'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    returnData = {
        'vacancies': vacancies
    }

    if len(vacancies) < count:
        returnData['message'] = 'There are not the requested number of vacancies open for applications.'

    return Response(returnData, status=status.HTTP_200_OK)





@api_view(['POST'])
def postReject(request, vacancyId):
    jwt = jwtHelper.extractJwt(request)
    
    if type(jwt) is not dict:
        return jwt

    try:
        vacancy = Vacancy.objects.get(pk = vacancyId, IsOpen__exact = True)

    except Vacancy.DoesNotExist:
        return Response(data={ 'status': 400, 'message': 'That vacancy is not open for applications' }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as err:
        print(f'uh oh: { err }')
        return Response(data={ 'status': 500, 'message': 'Error getting vacancy details' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        existingRejection = Reject.objects.filter(UserId__exact = jwt['id'], VacancyId__exact = vacancyId).count()

        if existingRejection > 0:
            return Response({ 'status': 400, 'message': 'User has already rejected that vacancy' }, status=status.HTTP_400_BAD_REQUEST)

        existingApplications = Application.objects.filter(UserId__exact = jwt['id'], VacancyId__exact = vacancyId).count()

        if existingApplications > 0:
            return Response({ 'status': 400, 'message': 'Cannot reject a vacancy that you have already applied to' }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as err:
        print(f'uh oh: { err }')
        return Response({ 'status': 500, 'message': 'Server error checking request validity' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    try:
        newReject = {
            'VacancyId': vacancy.VacancyId,
            'UserId': jwt['id']
        }

        serializer = RejectSerializer(data = newReject)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()       

        Favourite.objects.filter(UserId__exact = jwt['id'], VacancyId__exact = vacancy.VacancyId).delete() 
    
    except Exception as err:
        print(f'uh oh: { err }')
        return Response(data={ 'status': 500, 'message': 'Error while saving favourite' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    return Response(status=status.HTTP_201_CREATED)



@api_view(['GET'])
def getTags(request):
    jwt = jwtHelper.extractJwt(request)

    if type(jwt) is not dict:
        return jwt

    try:
        tagSet = Tag.objects.all().order_by('TagId')
        tagSerializer = TagSerializer(tagSet, many=True)
        tags = tagSerializer.data

        tagDictList = []

        for tag in tags:
            tagDictList.append({ 'id': tag['TagId'], 'text': tag['TagName'], 'icon': tag['TagStyle'] })

    except Exception as err:
        print(f'uh oh: { err }')
        return Response(data={'status': 500, 'message': 'Server error fetching vacancies'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(tagDictList, status=status.HTTP_200_OK)
