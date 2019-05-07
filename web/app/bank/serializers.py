from rest_framework import serializers
from bank.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Customer
        fields = ('id', 'fname', 'lname', 'city', 'house', 'image')
        read_only_fields = ('id',)
