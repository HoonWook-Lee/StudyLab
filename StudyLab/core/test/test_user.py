from django.test import TestCase, Client
from core.models import Users
from argon2 import PasswordHasher


# 회원 Test Code 작성
class AuthTestCase(TestCase):
    def setUp(self):
        Users.objects.create(
            username = 'test_user',
            password = 'argon2' + PasswordHasher().hash('qwer12#$'),
            hint = 'answer'
        )

    # 아이디 중복확인 Test
    def test_idcheck(self):
        c = Client()

        # 아이디를 입력하지 않았을 경우
        request = c.post('/user/check?user_id=')
        self.assertEqual(request.status_code, 422)

        # 아이디가 이미 존재하는 경우
        request = c.post('/user/check?user_id='+'test_user')
        self.assertEqual(request.status_code, 422)

        # 아이디가 5자리 미만인 경우
        request = c.post('/user/check?user_id='+'test')
        self.assertEqual(request.status_code, 422)

        # 가입할 수 없는 아이디인 경우 (문자 시작이 아닐 시)
        request = c.post('/user/check?user_id='+'!test_user')
        self.assertEqual(request.status_code, 422)

        # 가입할 수 없는 아이디인 경우 (특수 문자)
        request = c.post('/user/check?user_id='+'test_user#')
        self.assertEqual(request.status_code, 422)

        # 정상입력 아이디
        request = c.post('/user/check?user_id='+'success_user')
        self.assertEqual(request.status_code, 200)

    # 회원가입 Test
    def test_register(self):
        c = Client()

        # 중복 확인을 하지 않은 경우
        body = {
            'user_id' : 'test', 'password' : '1234', 'check_password' : '1234', 
            'hint' : 'answer', 'check' : 'False'
        }
        request = c.post('/user/register', body)

        self.assertEqual(request.status_code, 422)

        # 비밀번호 조건 오류 (6자리 미만)
        body = {
            'user_id' : 'tester', 'password' : '12', 'check_password' : '12', 
            'hint' : 'answer', 'check' : 'True'
        }
        request = c.post('/user/register', body)

        self.assertEqual(request.status_code, 422)

        # 비밀번호 조건 오류 (특수 문자 미 포함)
        body = {
            'user_id' : 'tester', 'password' : 'qw45er', 'check_password' : 'qw45er', 
            'hint' : 'answer', 'check' : 'True'
        }
        request = c.post('/user/register', body)

        self.assertEqual(request.status_code, 422)

        # 비밀번호 매칭 오류
        body = {
            'user_id' : 'tester', 'password' : 'qw12!@', 'check_password' : '1234', 
            'hint' : 'answer', 'check' : 'True'
        }
        request = c.post('/user/register', body)

        self.assertEqual(request.status_code, 422)

        # 회원가입 성공!
        body = {
            'user_id' : 'tester', 'password' : 'qw12!@', 'check_password' : 'qw12!@', 
            'hint' : 'answer', 'check' : 'True'
        }
        request = c.post('/user/register', body)

        self.assertEqual(request.status_code, 200)

    # 로그인 Test
    def test_login(self):
        c = Client()

        # 아이디 비밀번호 일치하지 않음
        body = {'user_id' : 'test_user', 'password' : '12344'}
        request = c.post('/user/login', body)

        self.assertEqual(request.status_code, 422)

        # 로그인 성공
        body = {'user_id' : 'test_user', 'password' : 'qwer12#$'}
        request = c.post('/user/login', body)

        self.assertEqual(request.status_code, 200)