from dateutil.relativedelta import relativedelta
from django.db.models import Sum, Max, Min
from rest_framework import serializers
from . models import *
import datetime

class housing_typeSerializer(serializers.ModelSerializer):
    class Meta:
        model = housing_type
        fields = ['id', 'housing_type']

class household_individualSerializer(serializers.ModelSerializer):
    class Meta:
        model = household_individual
        fields = ['name', 
                  'gender', 'marital_status',
                  'spouse', 'occupation_type',
                  'annual_income','DOB']

class household_individualSerializer2(serializers.ModelSerializer):
    # household_individualSerializer without the spouse field
    class Meta:
        model = household_individual
        fields = ['name', 'gender', 'marital_status',
                  'occupation_type','annual_income','DOB']

class empty_HouseholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Household
        fields = ['id', 'housing_type']

class simple_HouseholdSerializer(serializers.ModelSerializer):
    family_members = household_individualSerializer(many=True)

    class Meta:
        model = Household
        fields = ['id', 'housing_type', 'family_members']

    def create(self, validated_data):
        family_members = validated_data.pop('family_members')
        householdID = Household.objects.create(**validated_data)
        for family_member in family_members:
            household_individual.objects.create(householdID=householdID, **family_member)
        return householdID

class HouseholdSerializer(serializers.ModelSerializer):
    family_members = serializers.SerializerMethodField()
    household_detail = serializers.SerializerMethodField()

    def get_family_members(self, obj):
        family_members = household_individual.objects.filter(householdID = obj)
        return household_individualSerializer2(family_members, many=True, read_only=True).data

    def get_household_detail(self, obj):
        details = {}
        family_members = household_individual.objects.filter(householdID = obj)
        details['family_size'] = len(household_individual.objects.filter(householdID = obj))
        details['total_income'] = family_members.aggregate(Sum('annual_income'))['annual_income__sum'] or 0
        details['youngest_age'] = relativedelta(datetime.datetime.now(),
                                               family_members.aggregate(Max('DOB'))['DOB__max']).years
        details['oldest_age'] = relativedelta(datetime.datetime.now(),
                                              family_members.aggregate(Min('DOB'))['DOB__min']).years
        return details

    class Meta:
        model = Household
        fields = ['id', 'housing_type', 'family_members', 'household_detail']

class delete_HouseholdSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    family_members = household_individualSerializer(many=True)

    class Meta:
        model = Household
        fields = ['id','housing_type', 'family_members']
        read_only_fields = ['housing_type', 'family_members']

class household_add_memberSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = household_individual
        fields = ['id', 'householdID', 'name', 'gender', 'marital_status', 'spouse', 'occupation_type','annual_income','DOB']
        read_only_fields = ['name', 'gender', 'marital_status', 'spouse', 'occupation_type','annual_income','DOB']

class household_remove_memberSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = household_individual
        fields = ['id', 'householdID', 'name', 'gender', 'marital_status', 'spouse', 'occupation_type','annual_income','DOB']
        read_only_fields = ['name', 'householdID', 'gender', 'marital_status', 'spouse', 'occupation_type','annual_income','DOB']