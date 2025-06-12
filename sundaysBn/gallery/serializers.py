from rest_framework import serializers
from sqlalchemy.orm import sessionmaker
from .db import get_sqlalchemy_engine
from .models import Owner, ArtPiece
from datetime import datetime

class OwnerSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)

    def create(self, validated_data):
        engine = get_sqlalchemy_engine()
        Session = sessionmaker(bind=engine)
        session = Session()
        owner = Owner(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']  # In production, hash the password
        )
        session.add(owner)
        session.commit()
        owner_id = owner.id
        session.close()
        return owner

class ArtPieceSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(allow_blank=True)
    price = serializers.FloatField()
    image_url = serializers.CharField(max_length=255)
    created_at = serializers.DateTimeField(read_only=True)
    owner_id = serializers.IntegerField()

    def create(self, validated_data):
        engine = get_sqlalchemy_engine()
        Session = sessionmaker(bind=engine)
        session = Session()
        art_piece = ArtPiece(
            title=validated_data['title'],
            description=validated_data.get('description', ''),
            price=validated_data['price'],
            image_url=validated_data['image_url'],
            created_at=datetime.now(),
            owner_id=validated_data['owner_id']
        )
        session.add(art_piece)
        session.commit()
        session.close()
        return art_piece

    def update(self, instance, validated_data):
        engine = get_sqlalchemy_engine()
        Session = sessionmaker(bind=engine)
        session = Session()
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.image_url = validated_data.get('image_url', instance.image_url)
        session.merge(instance)
        session.commit()
        session.close()
        return instance