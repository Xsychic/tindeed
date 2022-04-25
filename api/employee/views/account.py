from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from authentication.helpers import jwt as jwtHelper
from employer.helpers import getAccount as accountHelper

@api_view(['GET'])
def getAccount(request):
    # get jwt
    jwt = jwtHelper.extractJwt(request)

    if type(jwt) is not dict:
        return jwt

    # get email
    try:
        email = accountHelper.getEmail(jwt['id'])

    except Exception as err:
        print(f'uh oh: { err }')
        return Response(data={ 'status': 500, 'message': 'Error acquiring email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    returnData = {
        'email': email['Email']
    }

    return Response(returnData, status=status.HTTP_200_OK)


@api_view(['PUT'])
def putAccount(request):
    # get jwt
    
    jwt = jwtHelper.extractJwt(request)

    if type(jwt) is not dict:
        return jwt

    # destructure
    try:
        newEmail = request.data['setEmail']
    except:
        return Response(data={'status': 400, 'message': 'incomplete request data'}, status=status.HTTP_400_BAD_REQUEST)

    # update Email/User['Email']
    try:
        accountHelper.updateEmail(jwt['id'], newEmail)
    except Exception as err:
        print(f'uh oh: { err }')
        return Response(data={'status': 500, 'message': 'server error updating email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({ 'status': 200, 'message': 'Account updated.'}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def deleteAccount(request):
    jwt = jwtHelper.extractJwt(request)

    if type(jwt) is not dict:
        return jwt

    try:
        accountHelper.deleteUser(jwt['id'])
        return Response(status=status.HTTP_200_OK)

    except Exception as err:
        print(f'uh oh: { err }')
        return Response(data={'status':500, 'message':'Server error while finding and deleting account'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)