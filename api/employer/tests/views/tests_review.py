from authentication.models import User
from employee.models import Application, Profile
from employer.models import EmployerDetails, Vacancy
from django.test import TestCase, TransactionTestCase
from authentication.tests.jwtFuncs import createAccessToken
from employee.serializers import ApplicationSerializer, ProfileSerializer, SummaryProfileSerializer


class getReviewTests(TestCase):
    
    fixtures = ['authentication/fixtures/testseed.json']

    # user: Sabah
    userId = 4
    # vacancy: Surveyor, rural practice (Facebook)
    vacancyId = 1001
    jwt = createAccessToken(userId)

    # GET TESTS

    def test_validRequestFullData(self):
        # make request
        response = self.client.get(f'/v1/e/vacancies/{ self.vacancyId }/review/', { 'searchValue':'' } , **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})
        data = response.data

        # check matches are correct
        matchesSet = Application.objects.filter(VacancyId__exact = self.vacancyId, ApplicationStatus__exact = 'MATCHED')
        matches = ApplicationSerializer(matchesSet, many=True).data

        expectedMatches = []

        for match in matches:
            profileSet = Profile.objects.get(UserId__exact = match['UserId'])
            profile = SummaryProfileSerializer(profileSet).data

            user = User.objects.get(pk = match['UserId'])
            profile['Email'] = user.Email

            expectedMatches.append({ 'application': match, 'profile': profile })


        self.assertListEqual(data['matches'], expectedMatches)

        # check new is correct
        newSet = Application.objects.filter(VacancyId__exact = self.vacancyId, ApplicationStatus__exact = 'PENDING').order_by('LastUpdated')[:1]

        new = ApplicationSerializer(newSet[0]).data

        profileSet = Profile.objects.get(UserId__exact = new['UserId'])
        profile = ProfileSerializer(profileSet).data

        expectedNew = { 'application': new, 'profile': profile }

        self.assertDictEqual(data['new'], expectedNew)

        # check vacancy is correct
        vacancy = Vacancy.objects.get(pk = self.vacancyId)
        employerDetails = EmployerDetails.objects.get(UserId__exact = self.userId)
        expectedVacancy = { 'VacancyId': vacancy.VacancyId, 'VacancyName': vacancy.VacancyName, 'CompanyName': employerDetails.CompanyName }
        self.assertEqual(data['vacancy'], expectedVacancy)
        
        numKeys = 4

        self.assertTrue(len(data.keys()) == numKeys)



    def test_validRequestFullDataSearchValue(self):
        # make request
        response = self.client.get(f'/v1/e/vacancies/{ self.vacancyId }/review/', { 'searchValue':'e' } , **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})
        data = response.data

        userIdList = []

        userSet = Profile.objects.filter(LastName__contains = 'e')

        for user in userSet:
            userIdList.append(user.UserId)

        # check matches are correct
        matchesSet = Application.objects.filter(VacancyId__exact = self.vacancyId, ApplicationStatus__exact = 'MATCHED', UserId__in = userIdList)
        matches = ApplicationSerializer(matchesSet, many=True).data

        expectedMatches = []

        for match in matches:
            profileSet = Profile.objects.get(UserId__exact = match['UserId'])
            profile = SummaryProfileSerializer(profileSet).data

            user = User.objects.get(pk = match['UserId'])
            profile['Email'] = user.Email

            expectedMatches.append({ 'application': match, 'profile': profile })


        self.assertListEqual(data['matches'], expectedMatches)

        # check new is correct
        newSet = Application.objects.filter(VacancyId__exact = self.vacancyId, ApplicationStatus__exact = 'PENDING').order_by('LastUpdated')[:1]

        new = ApplicationSerializer(newSet[0]).data

        profileSet = Profile.objects.get(UserId__exact = new['UserId'])
        profile = ProfileSerializer(profileSet).data

        expectedNew = { 'application': new, 'profile': profile }

        self.assertDictEqual(data['new'], expectedNew)

        
        # check vacancy is correct
        vacancy = Vacancy.objects.get(pk = self.vacancyId)
        employerDetails = EmployerDetails.objects.get(UserId__exact = self.userId)
        expectedVacancy = { 'VacancyId': vacancy.VacancyId, 'VacancyName': vacancy.VacancyName, 'CompanyName': employerDetails.CompanyName }
        self.assertEqual(data['vacancy'], expectedVacancy)
        
        numKeys = 4

        self.assertTrue(len(data.keys()) == numKeys)
    


    def test_otherUsersVacancy(self):
        vacancyId = 1010

        response = self.client.get(f'/v1/e/vacancies/{ vacancyId }/review/', { 'searchValue':'' } , **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})
        
        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'You do not have access to that vacancy')



    def test_invalidVacancy(self):
        vacancyId = 1030

        response = self.client.get(f'/v1/e/vacancies/{ vacancyId }/review/', { 'searchValue':'' } , **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})
        
        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'You do not have access to that vacancy')



    def test_expiredJwt(self):
        jwt = createAccessToken(self.userId, 'now')
        response = self.client.get(f'/v1/e/vacancies/{ self.vacancyId }/review/', { 'searchValue':'' } , **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})
        
        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'Expired auth token')



    def test_invalidJwt(self):
        jwt = self.jwt[:-1]
        response = self.client.get(f'/v1/e/vacancies/{ self.vacancyId }/review/', { 'searchValue':'' } , **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'Invalid auth token')




class putReviewValidTests(TransactionTestCase):
    
    userId = 4 # Sabah
    vacancyId = 1001 # Surveyor, rural practice (Facebook)
    applicationId = 1018 # Carlos to Surveyor, rural practice
    jwt = createAccessToken(userId)
    reset_sequences = True

    fixtures = ['authentication/fixtures/testseed.json']


    def test_validAccept(self):
        getPreResponse = self.client.get(f'/v1/e/vacancies/{ self.vacancyId }/review/', { 'searchValue':'' } , **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})
        putResponse = self.client.put(
            f'/v1/e/vacancies/{ self.vacancyId }/review/{ self.applicationId }/',
            data={ 'setStatus': 'accept' },
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'}
        )
        getPostResponse = self.client.get(f'/v1/e/vacancies/{ self.vacancyId }/review/', { 'searchValue':'' } , **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEquals(putResponse.status_code, 200)
        self.assertGreater(len(getPostResponse.data['matches']), len(getPreResponse.data['matches']))
    


    def test_validDefer(self):
        getPreResponse = self.client.get(f'/v1/e/vacancies/{ self.vacancyId }/review/', { 'searchValue':'' } , **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})
        putResponse = self.client.put(
            f'/v1/e/vacancies/{ self.vacancyId }/review/{ self.applicationId }/',
            data={ 'setStatus': 'defer' },
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'}
        )
        getPostResponse = self.client.get(f'/v1/e/vacancies/{ self.vacancyId }/review/', { 'searchValue':'' } , **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})
        
        self.assertEquals(putResponse.status_code, 200)
        self.assertFalse(getPreResponse.data['new'] == getPostResponse.data['new'])



    def test_validReject(self):
        preAppCount = Application.objects.filter(VacancyId__exact = self.vacancyId, ApplicationStatus__exact = 'PENDING').count()
        putResponse = self.client.put(
            f'/v1/e/vacancies/{ self.vacancyId }/review/{ self.applicationId }/',
            data={ 'setStatus': 'reject', 'searchValue': '' },
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'}
        )
        postAppCount = Application.objects.filter(VacancyId__exact = self.vacancyId, ApplicationStatus__exact = 'PENDING').count()
    
        self.assertEquals(putResponse.status_code, 200)
        self.assertLess(postAppCount, preAppCount)




class putReviewInvalidTests(TestCase):
    
    userId = 4 # Sabah
    vacancyId = 1001 # Surveyor, rural practice (Facebook)
    applicationId = 1018 # Carlos to Surveyor, rural practice
    jwt = createAccessToken(userId)

    fixtures = ['authentication/fixtures/testseed.json']


    def test_missingParameter(self):
        response = self.client.put(
            f'/v1/e/vacancies/{ self.vacancyId }/review/{ self.applicationId }/',
            data={  },
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'}
        )

        self.assertEquals(response.data['status'], 400)
        self.assertEquals(response.data['message'], 'incomplete request data')



    def test_invalidParameter(self):
        response = self.client.put(
            f'/v1/e/vacancies/{ self.vacancyId }/review/{ self.applicationId }/',
            data={ 'setStatus': 'potato' },
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'}
        )

        self.assertEquals(response.data['status'], 400)
        self.assertEquals(response.data['message'], 'invalid setStatus, must be one of "defer", "accept" or "reject"')



    def test_invalidApplication(self):
        applicationId = 10000

        response = self.client.put(
            f'/v1/e/vacancies/{ self.vacancyId }/review/{ applicationId }/',
            data={ 'setStatus': 'reject' },
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'}
        )
        
        self.assertEquals(response.data['status'], 404)
        self.assertEquals(response.data['message'], 'invalid application id')

    
    
    def test_otherUsersVacancy(self):
        vacancyId = 1010

        response = self.client.put(
            f'/v1/e/vacancies/{ vacancyId }/review/{ self.applicationId }/',
            data={ 'setStatus': 'reject' },
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'}
        )
        
        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'You do not have access to that vacancy')



    def test_invalidVacancy(self):
        vacancyId = 1030

        response = self.client.get(f'/v1/e/vacancies/{ vacancyId }/review/', { 'searchValue':'' } , **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})
        
        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'You do not have access to that vacancy')



    def test_expiredJwt(self):
        jwt = createAccessToken(self.userId, 'now')
        response = self.client.put(
            f'/v1/e/vacancies/{ self.vacancyId }/review/{ self.applicationId }/',
            data={ 'setStatus': 'reject' },
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'}
        )
        
        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'Expired auth token')



    def test_invalidJwt(self):
        jwt = self.jwt[:-1]
        response = self.client.put(
            f'/v1/e/vacancies/{ self.vacancyId }/review/{ self.applicationId }/',
            data={ 'setStatus': 'reject' },
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'}
        )

        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'Invalid auth token')

        

        





        