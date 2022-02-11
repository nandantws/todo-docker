from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import status

from todo.models import Todo, TodoCollection
from todo.serializers import ToDoSerializer, TodoCollectionSerializer, UserSerializer
from todo.utils import get_tokens_for_user


# Create your views here.
class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "message": "User Created Successfully.",
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": get_tokens_for_user(user)
        },status=status.HTTP_201_CREATED)


class LoginView(APIView):
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            return Response(get_tokens_for_user(user), status=status.HTTP_200_OK)
        return Response({'message': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)



class TodoCollectionViewSet(ModelViewSet):
    serializer_class = TodoCollectionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return TodoCollection.objects.prefetch_related('todo').filter(created_by=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)

        

class TodoViewSet(ModelViewSet):
    serializer_class = ToDoSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Todo.objects.all()

    def perform_create(self, serializer):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        return super().perform_create(serializer)



