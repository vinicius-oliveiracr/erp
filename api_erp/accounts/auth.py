from rest_framework.exceptions import AuthenticationFailed, APIException 

from accounts.models import User

from companies.models import Enterprise, Employee

from django.contrib.auth.hashers import check_password, make_password 

from django.contrib.auth import login 

from accounts.backends import EmailBackend


class Authentication:
    def signin(self,request, email=None, password=None) -> User:
        try:
            
            user_exists = User.objects.filter(email=email).exists()

            if not user_exists:
                raise AuthenticationFailed('Invalid Email and/or Password!')

            user = EmailBackend().authenticate(request=request, username=email, password=password)

            if user is None:
                raise AuthenticationFailed('Invalid Email and/or Password!')

            login(request, user, backend='accounts.backends.EmailBackend')

            return user

        except User.DoesNotExist:
            raise AuthenticationFailed('User does not exist!')
        
        except Exception as e:
            
            raise AuthenticationFailed(f'An error occurred: {str(e)}')
    
    def signup(self, name, email, password, account_type='owner', company_id = False) -> User:
        if not name or name == '':
            raise APIException('Name must not be null!')
        
        if not email or email == '':
            raise APIException('Email must not be null!')
        
        if not password or password == '':
            raise APIException('Password must not be null!')
        
        if account_type == 'employee' and not company_id:
            raise APIException('Company id must not be null for employee account!')
        
        user = User

        if user.objects.filter(email=email).exists():
            raise APIException('Email already exists!')
        
        password_hash = make_password(password)

        created_user = user.objects.create(
            name = name,
            email = email,
            password = password_hash,
            is_owner=0  if account_type == 'employee' else 1)
        
        if account_type == "owner":
            try:
                created_enterprise = Enterprise.objects.create(
                    name = 'Enterprise name',
                    user = created_user
                )
            except Exception as exception:
                print(f"error: {exception}")

        if account_type == "employee":
            Employee.objects.create(
                enterprise_id = company_id or created_enterprise.id,
                user_id = created_user.id
            )
        return created_user