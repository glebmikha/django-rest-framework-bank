from rest_framework import serializers
from bank.models import Customer, Account, Action, Transaction, Transfer


class AccountSerializer(serializers.ModelSerializer):
    # in order to work you should add related_name in Action model
    actions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Account
        fields = ('id', 'balance', 'actions')
        # balance is read only, because i don't want someone create account
        # with money
        read_only_fields = ('id', 'balance', 'actions')


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ('id', 'fname', 'lname',
                  'city', 'house', 'image')
        read_only_fields = ('id', )

    def create(self, validated_data):
        # override standard method to create cumster without pk in url
        # https://stackoverflow.com/questions/38745280/\
        # in-drfdjango-rest-framework-null-value-in-column-author-id-violates-not-nul
        validated_data['user_id'] = self.context['request'].user.id
        return super(CustomerSerializer, self).create(validated_data)


class ActionSerializer(serializers.ModelSerializer):

    # customer init to limit choises in browesble api
    # https://stackoverflow.com/questions/15328632/dynamically-limiting-queryset-of-related-field/20679785
    # if not, all account will be visible in browesble api. that's a leak. bad.

    def __init__(self, *args, **kwargs):
        super(ActionSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            self.fields['account'].queryset = self.fields['account']\
                .queryset.filter(user=self.context['view'].request.user)

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

    def __init__(self, *args, **kwargs):
        super(TransactionSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            self.fields['account'].queryset = self.fields['account']\
                .queryset.filter(user=self.context['view'].request.user)

    class Meta:
        model = Transaction
        fields = ('id', 'account', 'date', 'merchant', 'amount')
        read_only_fields = ('id', )


class TransferSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(TransferSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            self.fields['from_account'].queryset = self.fields['from_account']\
                .queryset.filter(user=self.context['view'].request.user)

    to_account = serializers.CharField()

    def validate(self, data):
        try:
            data['to_account'] = Account.objects.get(pk=data['to_account'])
        except Exception as e:
            print(e)
            raise serializers.ValidationError(
                "No such account from serializer")
        return data

    class Meta:
        model = Transfer
        fields = ('id', 'from_account', 'to_account', 'amount')
        read_only_fields = ('id', )
