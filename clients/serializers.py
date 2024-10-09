from rest_framework import serializers
from .models import Client, Deudas, Message
from datetime import datetime

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('text', 'role', 'sentAt')

    def validate_sentAt(self, value):
        if not isinstance(value, datetime):
            raise serializers.ValidationError("El valor debe ser un objeto datetime.")
        return value

    def validate_role(self, value):
        valid_roles = [choice[0] for choice in Message.ROLE_CHOICES]
        if value not in valid_roles:
            raise serializers.ValidationError(f'"{value}" no es una elección válida.')
        return value

class DeudasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deudas
        fields = ('institution', 'amount', 'dueDate')

    def validate_dueDate(self, value):
        if not isinstance(value, datetime):
            raise serializers.ValidationError("El valor debe ser un objeto datetime.")
        return value 

class ClientSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    debts = DeudasSerializer(many=True, read_only=True)
    class Meta:
        fields = ("uuid", "name", "rut", "messages", "debts")
        model = Client

class CreateClientSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, required=False)
    debts = DeudasSerializer(many=True, required=False)

    class Meta:
        model = Client
        fields = ('name', 'rut', 'messages', 'debts')

    def create(self, validated_data):
        messages_data = validated_data.pop('messages', [])
        debts_data = validated_data.pop('debts', [])
        client = Client.objects.create(**validated_data)

        for message_data in messages_data:
            Message.objects.create(client=client, **message_data)

        for debt_data in debts_data:
            Deudas.objects.create(client=client, **debt_data)

        return client
    