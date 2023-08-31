from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.authentication.serializer import LoginSerializer, RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework import generics
# Verify if there's a better way to reference project auth user model
from api.users.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.authentication.serializer import LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


"""
We can hit this URL with POST request and pass the access token in authorization and refresh token in body.
"""

# @permission_classes([IsAuthenticated])
class LogoutView(APIView):

     def post(self, request):
        try:
            if request.data.get('all'):
                token: OutstandingToken
                for token in OutstandingToken.objects.filter(user=request.user):
                    _, _ = BlacklistedToken.objects.get_or_create(token=token)
                print("All refresh tokens blacklisted")
                return Response({"status": "All refresh tokens blacklisted"})
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print('%s' % type(e))
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        data = f"Congratulation {request.user}, your API just responded to GET request"
        return Response({'response': data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = request.POST.get('text')
        data = f'Congratulation your API just responded to POST request with text: {text}'
        return Response({'response': data}, status=status.HTTP_200_OK)
    return Response({}, status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/login/',
        '/api/register/',
        '/api/refresh-token/'
    ]
    return Response(routes)