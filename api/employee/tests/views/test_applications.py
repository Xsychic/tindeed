from math import ceil
from django.test import TestCase
from employer.models import Vacancy, EmployerDetails
from employee.models import Application
from employee.serializers import ApplicationSerializer
from authentication.tests.jwtFuncs import createAccessToken


class getApplicationTests(TestCase):

    maxDiff = None
    userId = 2 # Adam
    jwt = createAccessToken(userId)
    fixtures = ['authentication/fixtures/testseed.json']


    def test_validRequestSortDateAscFilterAll(self):
        response = self.client.get('/v1/applications/', { 'sort': 'dateAsc', 'count': 5, 'pageNum': 1, 'filter': 'all' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        applicationSet = Application.objects.filter(UserId__exact = self.userId, ApplicationStatus__in = ['MATCHED','PENDING','REJECTED']).order_by('LastUpdated')[0:5]
        numApps = Application.objects.filter(UserId__exact = self.userId).count()
        applications = ApplicationSerializer(applicationSet, many=True).data

        pairedApplications = []

        for app in applications:
            vacancy = Vacancy.objects.get(pk = app['VacancyId'])
            employerDetails = EmployerDetails.objects.get(UserId__exact = vacancy.UserId)

            pair = { **app, 'VacancyId': vacancy.VacancyId, 'VacancyName': vacancy.VacancyName, 'CompanyName': employerDetails.CompanyName }
            pairedApplications.append(pair)

        expectedData = {
            'applications': pairedApplications,
            'numPages': ceil(numApps / 5),
            'pageNum': 1,
            'numApps': numApps
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(expectedData, response.data)



    # Sort: dateDesc, Filter: matched
    def test_validRequestSortDateDescFilterMatched(self):
        response = self.client.get('/v1/applications/', { 'sort': 'dateDesc', 'count': 5, 'pageNum': 1, 'filter': 'matched' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        applicationSet = Application.objects.filter(UserId__exact = self.userId, ApplicationStatus__in = ['MATCHED']).order_by('-LastUpdated')[0:5]
        numApps = Application.objects.filter(UserId__exact = self.userId, ApplicationStatus__in = ['MATCHED']).count()
        applications = ApplicationSerializer(applicationSet, many=True).data

        pairedApplications = []

        for app in applications:
            vacancy = Vacancy.objects.get(pk = app['VacancyId'])
            employerDetails = EmployerDetails.objects.get(UserId__exact = vacancy.UserId)

            pair = { **app, 'VacancyId': vacancy.VacancyId, 'VacancyName': vacancy.VacancyName, 'CompanyName': employerDetails.CompanyName }
            pairedApplications.append(pair)

        expectedData = {
            'applications': pairedApplications,
            'numPages': ceil(numApps / 5),
            'pageNum': 1,
            'numApps': numApps
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(expectedData, response.data)



    # Filter: pending, Incorrect Large Page Num
    def test_incorrectlyLargePageNumFilterPending(self):
        response = self.client.get('/v1/applications/', { 'sort': 'dateAsc', 'count': 5, 'pageNum': 3, 'filter': 'pending' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        numApps = Application.objects.filter(UserId__exact = self.userId, ApplicationStatus__in = ['PENDING']).count()

        skip = (numApps // 5) * 5

        applicationSet = Application.objects.filter(UserId__exact = self.userId, ApplicationStatus__in = ['PENDING']).order_by('LastUpdated')[skip:skip+5]
        applications = ApplicationSerializer(applicationSet, many=True).data

        pairedApplications = []

        for app in applications:
            vacancy = Vacancy.objects.get(pk = app['VacancyId'])
            employerDetails = EmployerDetails.objects.get(UserId__exact = vacancy.UserId)

            pair = { **app, 'VacancyId': vacancy.VacancyId, 'VacancyName': vacancy.VacancyName, 'CompanyName': employerDetails.CompanyName }
            pairedApplications.append(pair)

        expectedData = {
            'applications': pairedApplications,
            'numPages': ceil(numApps / 5),
            'pageNum': 1,
            'numApps': numApps
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(expectedData, response.data)



    # Filter: rejected
    def test_validRequestFilterRejected(self):
        response = self.client.get('/v1/applications/', { 'sort': 'dateAsc', 'count': 5, 'pageNum': 1, 'filter': 'rejected' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        applicationSet = Application.objects.filter(UserId__exact = self.userId, ApplicationStatus__in = ['REJECTED'])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['applications']), len(applicationSet))



    def test_missingParameters(self):
        response = self.client.get('/v1/applications/', { }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 400)



    def test_expiredJWT(self):
        jwt = createAccessToken(self.userId, 'now')

        response = self.client.get('/v1/applications/', { 'sort': 'titleAsc', 'count': 5, 'pageNum': 1, 'filter': 'all' }, **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Expired auth token')



    def test_invalidJWT(self):
        jwt = self.jwt[:-1]

        response = self.client.get('/v1/applications/', { 'sort': 'titleAsc', 'count': 5, 'pageNum': 1, 'filter': 'all' }, **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Invalid auth token')



class getApplicationStatsTests(TestCase):

    userId = 2 # Adam
    jwt = createAccessToken(userId)

    fixtures = ['authentication/fixtures/testseed.json']
    
    def test_getApplicationsStats(self):
        response = self.client.get('/v1/applications/stats/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        numApps = Application.objects.filter(
            UserId__exact = self.userId
        ).count()

        self.assertEquals(response.status_code, 200)
        self.assertEqual(response.data['total'], numApps)



    def test_expiredJWT(self):
        jwt = createAccessToken(self.userId, 'now')

        response = self.client.get('/v1/applications/stats/', **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Expired auth token')



    def test_invalidJWT(self):
        jwt = self.jwt[:-1]

        response = self.client.get('/v1/applications/stats/', **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Invalid auth token')



class getApplicationDetailsTests(TestCase):

    userId = 1 # Tom
    vacancyId = 1
    jwt = createAccessToken(userId)
    applicationId = 1034

    fixtures = ['authentication/fixtures/testseed.json']
    

    def test_validRequest(self):
        response = self.client.get(f'/v1/applications/{ self.applicationId }/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 200)



    def test_unmatchedApplication(self):
        response = self.client.get(f'/v1/applications/{ 1003 }/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.data['status'], 400)
        self.assertEqual(response.data['message'], 'You have not matched with that vacancy.')



    def test_noApplicationExists(self):
        response = self.client.get(f'/v1/applications/{ 9999 }/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'You do not have access to that application')



    def test_expiredJWT(self):
        jwt = createAccessToken(self.userId, 'now')

        response = self.client.get(f'/v1/applications/{ self.applicationId }/', **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Expired auth token')



    def test_invalidJWT(self):
        jwt = self.jwt[:-1]

        response = self.client.get(f'/v1/applications/{ self.applicationId }/', **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Invalid auth token')



class postApplicationTests(TestCase):

    userId = 2 # Adam
    vacancyId = 1
    jwt = createAccessToken(userId)

    fixtures = ['authentication/fixtures/testseed.json']


    # Valid Request
    def test_validRequest(self):
        response = self.client.post(f'/v1/vacancies/{ self.vacancyId }/apply/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 201)


    # think this test is a repetition of the one below
    # def test_invalidVacancy(self):
    #     response = self.client.post(f'/v1/vacancies/{ 2 }/apply/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

    #     self.assertEqual(response.status_code, 400)



    def test_closedVacancy(self):
        response = self.client.post(f'/v1/vacancies/{ 2 }/apply/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 400)



    def test_duplicateRequest(self):
        firstResponse = self.client.post(f'/v1/vacancies/{ 1004 }/apply/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(firstResponse.status_code, 400)



    def test_expiredJWT(self):
        jwt = createAccessToken(self.userId, 'now')

        response = self.client.post(f'/v1/vacancies/{ self.vacancyId }/apply/', **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['message'], 'Expired auth token')



    def test_invalidJWT(self):
        jwt = self.jwt[:-1]

        response = self.client.post(f'/v1/vacancies/{ self.vacancyId }/apply/', **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['message'], 'Invalid auth token')



class deleteApplicationTests(TestCase):
    
    userId = 2 # Adam
    vacancyId = 1004
    jwt = createAccessToken(userId)
    applicationId = 1028

    fixtures = ['authentication/fixtures/testseed.json']


    def test_validRequest(self):
        originalSet = Application.objects.filter(
            VacancyId__exact = self.vacancyId
        ).count()

        response = self.client.delete(f'/v1/applications/{ self.applicationId }/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        newSet = Application.objects.filter(
            VacancyId__exact = self.vacancyId
        ).count()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(originalSet - 1, newSet)



    def test_invalidRequest(self):
        applicationId = 1032
        response = self.client.delete(f'/v1/applications/{ applicationId }/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 401)


    
    def test_rejectedApplication(self):
        applicationId = 1052

        response = self.client.delete(f'/v1/applications/{ applicationId }/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 403)



    def test_expiredJWT(self):
        jwt = createAccessToken(self.userId, 'now')

        response = self.client.delete(f'/v1/applications/{ self.applicationId }/', **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Expired auth token')



    def test_invalidJWT(self):
        jwt = self.jwt[:-1]

        response = self.client.delete(f'/v1/applications/{ self.applicationId }/', **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Invalid auth token')