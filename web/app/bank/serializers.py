from rest_framework import serializers
from bank.models import Customer, Account, Action, Transaction


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


class ActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Action
        fields = ('id', 'account', 'amount', 'date')
        read_only_fields = ('id', 'date')

    def create(self, validated_data):
        # check if enough money to withdraw
        # mb it's better done by
        # https://medium.com/profil-software-blog/10-\
        # things-you-need-to-know-to-effectively-use-django-rest-framework-7db7728910e0
        if validated_data['account'].balance + validated_data['amount'] > 0:
            validated_data['account'].balance += validated_data['amount']
            validated_data['account'].save()
        else:
            raise serializers.ValidationError(
                ('Not enough money')
            )

        return super(ActionSerializer, self).create(validated_data)


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ('id', 'account', 'date', 'merchant', 'amount')
        read_only_fields = ('id', )
