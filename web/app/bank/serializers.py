from rest_framework import serializers
from bank.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Customer
        fields = ('id', 'fname', 'lname', 'city', 'house', 'image',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        # override standard method to create cumster without pk in url
        # https://stackoverflow.com/questions/38745280/\
        # in-drfdjango-rest-framework-null-value-in-column-author-id-violates-not-nul
        validated_data['user_id'] = self.context['request'].user.id
        return super(CustomerSerializer, self).create(validated_data)
