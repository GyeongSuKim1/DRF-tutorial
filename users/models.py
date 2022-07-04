from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
# ㅡㅡㅡ user를 만드는 로직 ㅡㅡㅡ
    def create_user(self, username, password=None):
        if not username:    # username 이 없을때 에러처리
            raise ValueError('Users must have an username')
        user = self.model(
            username=username,
        )
        print("가입 완료 !")
        user.set_password(password) # password 해싱처리 하기 위해 따로 빼줌
        user.save(using=self._db)
        return user

# ㅡㅡㅡ createsuperuser 만드는 로직 ㅡㅡㅡ
    # python manage.py createsuperuser 사용 시 해당 함수가 사용됨
    def create_superuser(self, username, password=None):
        user = self.create_user(
            username=username,
            password=password   # 14번줄에서 password가 걸리게 되어 있어 따로 처리 안함.
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


# ㅡㅡㅡ User 테이블 ㅡㅡㅡ
class User(AbstractBaseUser):
    username = models.CharField("사용자 계정", max_length=40, unique=True)
    password = models.CharField("비밀번호", max_length=130)
    email = models.EmailField("이메일 주소", max_length=100)
    fullname = models.CharField("이름", max_length=20)
    join_date = models.DateTimeField("가입일", auto_now_add=True)
    
    is_active = models.BooleanField(default=True)
    
    is_admin = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'username' # 기본 유저 계정
    
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def __str__(self):
        return f"{self.username} / {self.email} / {self.fullanme}"
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin