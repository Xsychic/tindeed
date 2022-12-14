from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..helpers import reset as resetHelper
from authentication.models import User
from django.contrib.auth.hashers import make_password 

@api_view(['POST'])
def postEmail(request):
    # grab email from body
    body = request.data

    if(not body or not body['email']):
        return Response(data={'status': 400, 'message': 'incomplete form data'}, status=status.HTTP_400_BAD_REQUEST)

    # check email is in db and associated with an account
    try:
        userObj = User.objects.get(Email__exact=body['email'])
    except User.DoesNotExist:
        # if email is unverified, then return 401
        # set as 200 so the user cannot tell if the email belongs to a user account for security
        return Response(data={ 'status': 200 }, status=status.HTTP_200_OK)
    except Exception as err:
        return Response(data={'status': 500, 'message': 'Server error.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # if email is verified, then create reset token and send email, return 200
    plainToken = resetHelper.createResetPlainToken()
    hashedToken = resetHelper.createResetHashedToken(plainToken)
    resetHelper.saveResetToken(hashedToken, userObj)

    if(resetHelper.sendEmail(plainToken, body['email'])):
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
def getReset(request, token):

    # on vue mount, send get request to auto auth DONE
    # check /reset/token matches token
    try:
        hashedToken = resetHelper.createResetHashedToken(token)
        validatedUser = User.objects.get(PasswordResetToken__exact = hashedToken)

        if (not resetHelper.checkExpiration(validatedUser)):
            return Response(data={'status': 401, 'message': 'Expired reset token.'}, status=status.HTTP_401_UNAUTHORIZED)

    except User.DoesNotExist:
        return Response(data={'status': 401, 'message': 'Unauthorised request.'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as err:
        return Response(data={'status': 500, 'message': 'Server error.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status=status.HTTP_200_OK)



@api_view(['POST'])
def postReset(request):
    
    # destructure
    try:
        password = request.data['password']
        token = request.data['token']
    except:
        return Response(data={'status': 400, 'message': 'incomplete request data'}, status=status.HTTP_400_BAD_REQUEST)

    # verify token matches db again
    try:
        hashedToken = resetHelper.createResetHashedToken(token)
        validatedUser = User.objects.get(PasswordResetToken__exact = hashedToken)

        if (not resetHelper.checkExpiration(validatedUser)):
            return Response(data={'status': 401, 'message': 'Expired reset token.'}, status=status.HTTP_401_UNAUTHORIZED)

    except User.DoesNotExist:
        ## return 401 if not
        return Response(data={'status': 401, 'message': 'Unauthorised request.'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as err:
        return Response(data={'status': 500, 'message': 'Server error.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # update password in db
    validatedUser.Password = make_password(password)
    validatedUser.PasswordResetToken = None
    validatedUser.PasswordResetExpiration = None
    validatedUser.save(update_fields=['Password','PasswordResetToken','PasswordResetExpiration'])
    # return 200
    return Response(data={'status': 200, 'message': 'Update successful.'}, status=status.HTTP_200_OK)