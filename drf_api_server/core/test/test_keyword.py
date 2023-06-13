from core.models import Keywords, Users
from argon2 import PasswordHasher
from rest_framework.test import APITestCase, APIClient

# 메모 Test Code 작성
class MemosTestCase(APITestCase):
    def setUp(self):
        # 관리자 아이디 등록
        Users.objects.create(
            is_superuser=1,
            username = 'admin',
            password = 'argon2' + PasswordHasher().hash('qw12!@'),
            hint = 'answer'
        )
        
        # 사용자1
        user1 = Users.objects.create(
            username = 'test_user1',
            password = 'argon2' + PasswordHasher().hash('qw12!@'),
            hint = 'answer'
        )

        # 사용자2
        user2 = Users.objects.create(
            username = 'test_user2',
            password = 'argon2' + PasswordHasher().hash('qw12!@'),
            hint = 'answer'
        )

        # 키워드 등록
        Keywords.objects.create(keyword='Django', writer=user1)
        Keywords.objects.create(keyword='Flask', writer=user2)

    # 키워드 Test
    def test_keyword(self):
        c = APIClient()

        # Token 생성
        user1_body = {'username' : 'test_user1', 'password' : 'qw12!@'}
        user2_body = {'username' : 'test_user2', 'password' : 'qw12!@'}
        user1_token = c.post('/api/token/', user1_body).json()['access']
        user2_token = c.post('/api/token/', user2_body).json()['access']

        # header 생성
        user1_headers = {'Authorization' : f'Bearer {user1_token}'}
        user2_headers = {'Authorization' : f'Bearer {user2_token}'}

        # 토큰 없이 키워드 생성한 경우
        body = {'keyword' : 'Django'}
        request = c.post('/apis/keywords/', body)

        self.assertEqual(request.status_code, 401)

        # 키워드를 입력하지 않았을 경우
        body = {'keyword' : ''}
        request = c.post('/apis/keywords/', body, headers=user1_headers)

        self.assertEqual(request.status_code, 400)

        # 키워드 중복 에러
        body = {'keyword' : 'Django'}
        request = c.post('/apis/keywords/', body, headers=user1_headers)

        self.assertEqual(request.status_code, 422)

        # 키워드 중복 에러 (대소문자 구분 x)
        body = {'keyword' : 'django'}
        request = c.post('/apis/keywords/', body, headers=user1_headers)

        self.assertEqual(request.status_code, 422)

        # 키워드 등록
        body = {'keyword' : 'FastAPI'}
        request = c.post('/apis/keywords/', body, headers=user1_headers)

        self.assertEqual(request.status_code, 201)
        
        # 사용자1
        user1 = Users.objects.get(username='test_user1')
        c.force_authenticate(user=user1)

        # 키워드 삭제 권한 제한
        request = c.delete('/apis/keywords/2/', body, headers=user1_headers)

        self.assertEqual(request.status_code, 403)

        # 본인이 작성한 키워드 삭제
        request = c.delete('/apis/keywords/1/', body, headers=user1_headers)

        self.assertEqual(request.status_code, 200)

        # 관리자
        admin = Users.objects.get(username='admin')
        c.force_authenticate(user=admin)

        # 관리자 권한 삭제
        request = c.delete('/apis/keywords/2/', body, headers=user1_headers)

        self.assertEqual(request.status_code, 200)