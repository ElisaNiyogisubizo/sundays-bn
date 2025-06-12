from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from sqlalchemy.orm import sessionmaker
from .db import get_sqlalchemy_engine
from .models import Owner, ArtPiece
from .serializers import OwnerSerializer, ArtPieceSerializer
from .authentication import authenticate_owner
import cloudinary.uploader
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class OwnerRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'email', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Owner username'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description='Owner email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, description='Owner password'),
            },
        ),
        responses={201: openapi.Schema(type=openapi.TYPE_OBJECT, properties={'token': openapi.Schema(type=openapi.TYPE_STRING)})}
    )
    def post(self, request):
        serializer = OwnerSerializer(data=request.data)
        if serializer.is_valid():
            owner = serializer.save()
            token, created = Token.objects.get_or_create(user_id=owner.id)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OwnerLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Owner username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, description='Owner password'),
            },
        ),
        responses={200: openapi.Schema(type=openapi.TYPE_OBJECT, properties={'token': openapi.Schema(type=openapi.TYPE_STRING)})}
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        owner = authenticate_owner(username, password)
        if owner:
            token, created = Token.objects.get_or_create(user_id=owner.id)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class ArtPieceListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Token <your-token>",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={200: ArtPieceSerializer(many=True)}
    )
    def get(self, request):
        engine = get_sqlalchemy_engine()
        Session = sessionmaker(bind=engine)
        session = Session()
        art_pieces = session.query(ArtPiece).filter_by(owner_id=request.user.id).all()
        serializer = ArtPieceSerializer(art_pieces, many=True)
        session.close()
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['title', 'price', 'image'],
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Art piece title'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Art piece description', default=''),
                'price': openapi.Schema(type=openapi.TYPE_NUMBER, description='Art piece price'),
                'image': openapi.Schema(type=openapi.TYPE_FILE, description='Art piece image file'),
            },
        ),
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Token <your-token>",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={201: ArtPieceSerializer}
    )
    def post(self, request):
        if 'image' in request.FILES:
            upload_result = cloudinary.uploader.upload(request.FILES['image'])
            request.data['image_url'] = upload_result['secure_url']
        request.data['owner_id'] = request.user.id
        serializer = ArtPieceSerializer(data=request.data)
        if serializer.is_valid():
            art_piece = serializer.save()
            return Response(ArtPieceSerializer(art_piece).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ArtPieceDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, owner_id):
        engine = get_sqlalchemy_engine()
        Session = sessionmaker(bind=engine)
        session = Session()
        art_piece = session.query(ArtPiece).filter_by(id=pk, owner_id=owner_id).first()
        session.close()
        return art_piece

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Token <your-token>",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={200: ArtPieceSerializer}
    )
    def get(self, request, pk):
        art_piece = self.get_object(pk, request.user.id)
        if not art_piece:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ArtPieceSerializer(art_piece)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Art piece title'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Art piece description'),
                'price': openapi.Schema(type=openapi.TYPE_NUMBER, description='Art piece price'),
                'image': openapi.Schema(type=openapi.TYPE_FILE, description='Art piece image file'),
            },
        ),
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Token <your-token>",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={200: ArtPieceSerializer}
    )
    def put(self, request, pk):
        art_piece = self.get_object(pk, request.user.id)
        if not art_piece:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if 'image' in request.FILES:
            upload_result = cloudinary.uploader.upload(request.FILES['image'])
            request.data['image_url'] = upload_result['secure_url']
        serializer = ArtPieceSerializer(art_piece, data=request.data, partial=True)
        if serializer.is_valid():
            art_piece = serializer.save()
            return Response(ArtPieceSerializer(art_piece).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Token <your-token>",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={204: 'No Content'}
    )
    def delete(self, request, pk):
        art_piece = self.get_object(pk, request.user.id)
        if not art_piece:
            return Response(status=status.HTTP_404_NOT_FOUND)
        engine = get_sqlalchemy_engine()
        Session = sessionmaker(bind=engine)
        session = Session()
        session.delete(art_piece)
        session.commit()
        session.close()
        return Response(status=status.HTTP_204_NO_CONTENT)