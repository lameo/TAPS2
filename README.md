# TAPS

Q2. Backend Technical Assessment



## Requirements

- Python 3.6
- Django 3.0.3
- Django REST Framework

## Installation

```bash
git clone git@github.com:lameo/TAPS.git
# Loading the virtual environment to isolate our package dependencies locally
env\Scripts\activate
# Getting into file directory
cd api_server
# Running api server
python manage.py runserver
```

## API Endpoints

Admin panel accessible via: http://127.0.0.1:8000/admin/

```
Username: admin
Password: admin
```

API panel accessible via: http://127.0.0.1:8000/

| Endpoint                                       | HTTP Method | CRUD Method | Result                                                       |
| ---------------------------------------------- | ----------- | ----------- | ------------------------------------------------------------ |
| housingType/create                             | POST        | CREATE      | Create a new housing Type                                    |
| individual/create                              | POST        | CREATE      | Create a new individual                                      |
| household/create_empty                         | POST        | CREATE      | Create a new house                                           |
| household/list                                 | GET         | READ        | List all household in the database                           |
| household/list                                 | POST        | CREATE      | Create household with individuals inside                     |
| household/show                                 | GET         | READ        | Shows the details of a household in the database after `params` filtering |
| household/delete                               | POST        | DELETE      | Delete household                                             |
| household/addindividual                        | POST        | UPDATE      | Adds an individual to a household                            |
| household/deleteindividual                     | POST        | UPDATE      | Removes individual from a household                          |
| household_qualifying/studentEncouragementBonus | GET         | READ        | Display household eligible for  studentEncouragementBonus    |
| household_qualifying/familyTogethernessScheme  | GET         | READ        | Display household eligible for familyTogethernessScheme      |
| household_qualifying/elderbonus                | GET         | READ        | Display household eligible for elderbonus                    |
| household_qualifying/babySunshineGrant         | GET         | READ        | Display household eligible for babySunshineGrant             |
| household_qualifying/yoloGstGrant              | GET         | READ        | Display household eligible for yoloGstGrant                  |

