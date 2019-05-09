from rest_framework import serializers
from bank.models import Customer, Account


class CustomerSerializer(serializers.ModelSerializer):

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


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('id', 'balance')
        # balance is read only, because i don't want someone create account
        # with money
        read_only_fields = ('id', 'balance')
