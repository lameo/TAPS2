from dateutil.relativedelta import relativedelta
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.db.models import Sum, Min
from . serializers import *
from . models import *
import datetime


# Create your views here.
class houseing_typeView(viewsets.ModelViewSet):
    """
    Get:
    Lists all the housing types in the database

    Post:
    Creates and adds a housing types in the database

    Example parameter:
    {"housing_type": "executiveApartment"}
    """
    queryset = housing_type.objects.all()
    serializer_class = housing_typeSerializer
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'Status': "True",
            'Message': 'Household type created'
            }, status=status.HTTP_201_CREATED, headers=headers)

class household_individualView(viewsets.ModelViewSet):
    """
    Get:
    Lists all the individuals in the database

    Post:
    Creates and adds a individuals without any household assignments

    Example parameter:
    {"name": "Yi Ling", 
    "gender": 2, 
    "marital_status": 2, 
    "spouse": "Zhi Hao", 
    "occupation_type": 3, 
    "annual_income": "50000.00", 
    "DOB": "1971-12-10"}
    """
    queryset = household_individual.objects.all()
    serializer_class = household_individualSerializer
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'Status': "True",
            'Message': 'Individual created'
            }, status=status.HTTP_201_CREATED, headers=headers)

class empty_Household_View(viewsets.ModelViewSet):
    """
    Get:
    Lists all the households id and housingType in the database

    Post:
    Creates and adds a household without any family members

    Example parameter
    {"housing_type": 2}
    """
    queryset = Household.objects.all()
    serializer_class = empty_HouseholdSerializer
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'Status': "True",
            'Message': 'Household created'
            }, status=status.HTTP_201_CREATED, headers=headers)

class simple_Household_View(viewsets.ModelViewSet):
    """
    Get:
    Lists all the households in the database

    Post:
    Creates and adds a household with its corresponding family members

    Example parameter:
    {"housing_type": "3","family_members": [
    {"name": "Yi Ling", "gender": 2, "marital_status": 2, "spouse": "Zhi Hao", "occupation_type": 3, "annual_income": "50000.00", "DOB": "1971-12-10" },
    {"name": "Zhi Hao", "gender": 1, "marital_status": 2, "spouse": "Yi Ling", "occupation_type": 3, "annual_income": "45000.00", "DOB": "1965-07-14" },
    {"name": "Jia Hui", "gender": 1, "marital_status": 1, "spouse": "", "occupation_type": 2, "annual_income": "5.00", "DOB": "2010-02-02" }]}
    """
    queryset = Household.objects.all()
    serializer_class = simple_HouseholdSerializer
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'Status': "True",
            'Message': 'Household created'
            }, status=status.HTTP_201_CREATED, headers=headers)

class Household_View(viewsets.ModelViewSet):
    """
    A household viewset with more parameters given

    get:
    Return a list of all households

    Filter parameters:
    ● `household_ID`
    ↳ number ('28') or list of number ('28,29,32')
    ↳ Filter for specific household id

    ● below_min_annual_income
    ↳ number ('150000')
    ↳ Filter for specific household with combined annual income less (non-inclusive) than the given value

    ● containYoungerThanYears
    ↳ number ('10')
    ↳ Filter for specific household with at least one member younger (non-inclusive) than the given value

    ● containOlderThanYears
    ↳ number ('60')
    ↳ Filter for specific household with at least one member older (non-inclusive) than the given value

    ● housingTypeFilter
    ↳ string ('HDB')
    ↳ Filter for specific householdtype (Non-case-sensitive)


    Example link with all arguments: http://127.0.0.1:8000/household/show/?household_ID=28,29&below_min_annual_income=150000&containYoungerThanYears=10&containOlderThanYears=60&housingTypeFilter=HDB
    """
    queryset = Household.objects.all()
    serializer_class = HouseholdSerializer
    http_method_names = ['get']

    def get_queryset(self):
    
        # Filtering parameters
        queryset = Household.objects.all()

        household_ID = self.request.query_params.get('household_ID')
        below_min_annual_income = self.request.query_params.get('below_min_annual_income')
        containYoungerThanYears = self.request.query_params.get('containYoungerThanYears')
        containOlderThanYears = self.request.query_params.get('containOlderThanYears')
        housingTypeFilter = self.request.query_params.get('housingTypeFilter')

        # Filter by household_ID
        if household_ID != None:
            household_ID = [int(s) for s in household_ID.split(',')]
            queryset = queryset.filter(id__in=household_ID)


        # Filter household earning below $x (Non-inclusive)    
        if below_min_annual_income != None:
            # Getting list of household with at least one individual inside
            nonEmptyHouseholdList = household_individual.objects.values('householdID').order_by('householdID').distinct().values_list('householdID', flat=True)
            nonEmptyHousehold = household_individual.objects.filter(householdID__in = nonEmptyHouseholdList)

            filtered_Income_List = nonEmptyHousehold.values('householdID').annotate(total_income = Sum('annual_income')).order_by('householdID').filter(total_income__lt = below_min_annual_income).values_list('householdID', flat=True)
            # 1. Group household_individual by householdID, 
            # 2. then sum annual_income as total_income, 
            # 3. then select householdID where total_income > minHouseholdIncome
            queryset = queryset.filter(id__in=filtered_Income_List)


        # Filter household than contains people below X years of age (Non-inclusive)        
        if containYoungerThanYears != None:
            containYoungerThanYears = int(containYoungerThanYears)
            dateToCompare = datetime.datetime.now() + relativedelta(years=-containYoungerThanYears)

            # Getting list of household with at least one individual inside
            nonEmptyHouseholdList = household_individual.objects.values('householdID').order_by('householdID').distinct().values_list('householdID', flat=True)
            nonEmptyHousehold = household_individual.objects.filter(householdID__in = nonEmptyHouseholdList)

            filtered_Young_List = nonEmptyHousehold.values('householdID').annotate(youngest = Max('DOB')).order_by('householdID')
            filtered_Young_List = filtered_Young_List.filter(youngest__gt = dateToCompare).values_list('householdID', flat=True)
            # 1. Generate date parameter to compare by deducing x years from today's date
            # 2. Group household_individual by householdID, 
            # 3. then find largest DOB (youngest) in each household as youngest
            # 4. then select householdID where youngest > dateToCompare
            queryset = queryset.filter(id__in=filtered_Young_List)


        # Filter household than contains people below X years of age (Non-inclusive)        
        if containOlderThanYears != None:
            containOlderThanYears = int(containOlderThanYears)
            dateToCompare = datetime.datetime.now() + relativedelta(years=-containOlderThanYears)

            # Getting list of household with at least one individual inside
            nonEmptyHouseholdList = household_individual.objects.values('householdID').order_by('householdID').distinct().values_list('householdID', flat=True)
            nonEmptyHousehold = household_individual.objects.filter(householdID__in = nonEmptyHouseholdList)

            filtered_Old_List = nonEmptyHousehold.values('householdID').annotate(oldest = Min('DOB')).order_by('householdID')
            filtered_Old_List = filtered_Old_List.filter(oldest__lte = dateToCompare).values_list('householdID', flat=True)
            # 1. Generate date parameter to compare by deducing x years from today's date
            # 2. Group household_individual by householdID, 
            # 3. then find smallest DOB (oldest) in each household as youngest
            # 4. then select householdID where oldest < dateToCompare
            queryset = queryset.filter(id__in=filtered_Old_List)

        # Filter by housingtype
        if housingTypeFilter != None:
            # Get number representation of housing type ('HDB', 'Condo', etc), case insensitive
            housingTypeFilternum = housing_type.objects.filter(housing_type__iexact = housingTypeFilter).values('id')[0]['id']
            # Filter list of household of selected housing type,then get distinct household_id 
            housingTypehouseholdList = Household.objects.filter(housing_type = housingTypeFilternum).values('id').order_by('id').distinct().values_list('id', flat=True)
            queryset = queryset.filter(id__in=housingTypehouseholdList)

        return queryset

class studentEncouragementBonusView(viewsets.ModelViewSet):
    """
    Returns a list households and qualifying family members for Student Encouragement Bonus
        ● Households with children of less than 16 years old.
        ● Household income of less than $150,000.

    get:
    Return a list of all qualifying households
    """
    queryset = Household.objects.all()
    serializer_class = HouseholdSerializer
    http_method_names = ['get']

    def get_queryset(self):
        queryset = Household.objects.all()
        containYoungerThanYears = 16
        dateToCompare = datetime.datetime.now() + relativedelta(years=-containYoungerThanYears)

        nonEmptyHouseholdList = household_individual.objects.values('householdID').order_by('householdID').distinct().values_list('householdID', flat=True)
        nonEmptyHousehold = household_individual.objects.filter(householdID__in = nonEmptyHouseholdList)

        filtered_Young_List = nonEmptyHousehold.values('householdID').annotate(youngest = Max('DOB')).order_by('householdID')
        filtered_Young_List = filtered_Young_List.filter(youngest__gt = dateToCompare).values_list('householdID', flat=True)
        queryset = queryset.filter(id__in=filtered_Young_List)

        below_min_annual_income = 150000        
        filtered_Income_List = nonEmptyHousehold.values('householdID').annotate(total_income = Sum('annual_income')).order_by('householdID').filter(total_income__lte = below_min_annual_income).values_list('householdID', flat=True)
        queryset = queryset.filter(id__in=filtered_Income_List)
        return queryset

class familyTogethernessSchemeView(viewsets.ModelViewSet):
    """
    Returns a list households and qualifying family members for Family Togetherness Scheme 
        ● Households with husband & wife 
        ● Has child(ren) younger than 18 years old.

    get:
    Return a list of all qualifying households
    """
    queryset = Household.objects.all()
    serializer_class = HouseholdSerializer
    http_method_names = ['get']

    def get_queryset(self):
        queryset = Household.objects.all()

        # Getting list of household with at least one individual inside
        nonEmptyHouseholdList = household_individual.objects.values('householdID').order_by('householdID').distinct().values_list('householdID', flat=True)
        nonEmptyHousehold = household_individual.objects.filter(householdID__in = nonEmptyHouseholdList)

        # Getting all distinct householdID
        householdList = nonEmptyHousehold.values('householdID').order_by('householdID').distinct().values_list('householdID', flat=True)
        householdwHusbandnWife = []
        for household in householdList:
            nameList = nonEmptyHousehold.filter(householdID = household).values('name').order_by('householdID').distinct().values_list('name', flat=True)
            spouseList = nonEmptyHousehold.filter(householdID = household).values('spouse').order_by('householdID').distinct().values_list('spouse', flat=True)
            # If 2 elements are the same, means same husband/wife name was found in nameList & spouseList
            counter = len(set(nameList) & set(spouseList))
            if counter >= 2:
                householdwHusbandnWife.append(household)
        queryset = queryset.filter(id__in=householdwHusbandnWife)

        # Filter household than contains people below 18 years of age (Non-inclusive)        
        containOlderThanYears = 18
        dateToCompare = datetime.datetime.now() + relativedelta(years=-containOlderThanYears)
        filtered_Old_List = nonEmptyHousehold.values('householdID').annotate(oldest = Min('DOB')).order_by('householdID')
        filtered_Old_List = filtered_Old_List.filter(oldest__lte = dateToCompare).values_list('householdID', flat=True)
        queryset = queryset.filter(id__in=filtered_Old_List)
        return queryset

class elderBonusView(viewsets.ModelViewSet):
    """
    Returns a list of households and qualifying family members for Elder Bonus
        ● HDB household
        ● with family members above the age of 50.

    get:
    Return a list of all qualifying households
    """
    queryset = Household.objects.all()
    serializer_class = HouseholdSerializer
    http_method_names = ['get']

    def get_queryset(self):
        queryset = Household.objects.all()

        housingTypeFilter = "hdb"
        housingTypeFilternum = housing_type.objects.filter(housing_type__iexact = housingTypeFilter).values('id')[0]['id']
        housingTypehouseholdList = Household.objects.filter(housing_type = housingTypeFilternum).values('id').order_by('id').distinct().values_list('id', flat=True)
        queryset = queryset.filter(id__in=housingTypehouseholdList)


        containOlderThanYears = 50
        dateToCompare = datetime.datetime.now() + relativedelta(years=-containOlderThanYears)

        nonEmptyHouseholdList = household_individual.objects.values('householdID').order_by('householdID').distinct().values_list('householdID', flat=True)
        nonEmptyHousehold = household_individual.objects.filter(householdID__in = nonEmptyHouseholdList)

        filtered_Old_List = nonEmptyHousehold.values('householdID').annotate(oldest = Min('DOB')).order_by('householdID')
        filtered_Old_List = filtered_Old_List.filter(oldest__lte = dateToCompare).values_list('householdID', flat=True)
        queryset = queryset.filter(id__in=filtered_Old_List)
        return queryset

class babySunshineGrantView(viewsets.ModelViewSet):
    """
    Returns a list of households and qualifying family members for Baby Sunshine Grant
        ● Household with young children younger than 5.

    get:
    Return a list of all qualifying households
    """
    queryset = Household.objects.all()
    serializer_class = HouseholdSerializer
    http_method_names = ['get']

    def get_queryset(self):
        queryset = Household.objects.all()
        containYoungerThanYears = 5
        dateToCompare = datetime.datetime.now() + relativedelta(years=-containYoungerThanYears)

        nonEmptyHouseholdList = household_individual.objects.values('householdID').order_by('householdID').distinct().values_list('householdID', flat=True)
        nonEmptyHousehold = household_individual.objects.filter(householdID__in = nonEmptyHouseholdList)
        
        filtered_Young_List = nonEmptyHousehold.values('householdID').annotate(youngest = Max('DOB')).order_by('householdID')
        filtered_Young_List = filtered_Young_List.filter(youngest__gt = dateToCompare).values_list('householdID', flat=True)
        queryset = queryset.filter(id__in=filtered_Young_List)
        return queryset

class yoloGstGrantView(viewsets.ModelViewSet):
    """
    Returns a list of households that qualify for the YOLO GST Grant
        ● HDB households
        ● annual income of less than $100,000

    get:
    Return a list of all qualifying households
    """
    queryset = Household.objects.all()
    serializer_class = HouseholdSerializer
    http_method_names = ['get']

    def get_queryset(self):
        queryset = Household.objects.all()

        housingTypeFilter = "hdb"
        housingTypeFilternum = housing_type.objects.filter(housing_type__iexact = housingTypeFilter).values('id')[0]['id']
        housingTypehouseholdList = Household.objects.filter(housing_type = housingTypeFilternum).values('id').order_by('id').distinct().values_list('id', flat=True)
        queryset = queryset.filter(id__in=housingTypehouseholdList)


        below_min_annual_income = 100000
        nonEmptyHouseholdList = household_individual.objects.values('householdID').order_by('householdID').distinct().values_list('householdID', flat=True)
        nonEmptyHousehold = household_individual.objects.filter(householdID__in = nonEmptyHouseholdList)

        filtered_Income_List = nonEmptyHousehold.values('householdID').annotate(total_income = Sum('annual_income')).order_by('householdID').filter(total_income__lte = below_min_annual_income).values_list('householdID', flat=True)
        queryset = queryset.filter(id__in=filtered_Income_List)
        return queryset

class delete_Household_View(viewsets.ModelViewSet):
    """
    Post:
    Deletes a household and all related family members

    Example parameter
    {"housing_type": 2}
    """
    queryset = Household.objects.all()
    serializer_class = delete_HouseholdSerializer
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        toDelete = serializer['id'].value
        Household.objects.filter(id = toDelete).delete()

        headers = self.get_success_headers(serializer.data)
        return Response({
            'Status': "True",
            'Message': 'Household has been deleted'
            }, status=status.HTTP_201_CREATED, headers=headers)

class household_add_member_View(viewsets.ModelViewSet):
    """
    Post:
    Adds an individual to a household

    Example parameter
    {"id": 19,
    "householdID": 38}
    """
    queryset = household_individual.objects.filter(householdID__isnull=True).all()
    serializer_class = household_add_memberSerializer
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        householdID = serializer['householdID'].value
        individual_id = serializer['id'].value
        household_individual.objects.filter(id = individual_id).update(householdID=householdID)

        headers = self.get_success_headers(serializer.data)
        return Response({
            'Status': "True",
            'Message': 'individual added to household'
            }, status=status.HTTP_201_CREATED, headers=headers)

class household_deleteIndividual_View(viewsets.ModelViewSet):
    """
    Post:
    Removes an individual from a household

    Example parameter
    {"id": 19}
    """
    queryset = household_individual.objects.filter(householdID__isnull=False).all()
    serializer_class = household_remove_memberSerializer
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        individual_id = serializer['id'].value
        household_individual.objects.filter(id = individual_id).update(householdID = None)

        headers = self.get_success_headers(serializer.data)
        return Response({
            'Status': "True",
            'Message': 'individual removed from household'
            }, status=status.HTTP_201_CREATED, headers=headers)