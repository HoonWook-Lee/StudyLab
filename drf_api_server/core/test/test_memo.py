from core.models import Users, Keywords, Memos
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

        # 메모 등록
        Memos.objects.create(title='title', content='content', writer=user1)
        Memos.objects.create(title='title', content='content', writer=user2)

    # 메모 Test
    def test_memo(self):
        c = APIClient()

        # Token 생성
        user1_body = {'username' : 'test_user1', 'password' : 'qw12!@'}
        user2_body = {'username' : 'test_user2', 'password' : 'qw12!@'}
        user1_token = c.post('/api/token/', user1_body).json()['access']
        user2_token = c.post('/api/token/', user2_body).json()['access']

        # header 생성
        user1_headers = {'Authorization' : f'Bearer {user1_token}'}
        user2_headers = {'Authorization' : f'Bearer {user2_token}'}

        
        # 토큰 없이 메모 생성한 경우
        body = {'title' : 'title', 'content' : '메모 Test'}
        request = c.post('/apis/memos/', body)

        self.assertEqual(request.status_code, 401)

        # 제목을 입력하지 않았을 경우
        body = {'title' : '', 'content' : '메모 Test'}
        request = c.post('/apis/memos/', body, headers=user1_headers)

        self.assertEqual(request.status_code, 412)

        # 내용을 입력하지 않았을 경우
        body = {'title' : '메모 Test', 'content' : ''}
        request = c.post('/apis/memos/', body, headers=user1_headers)

        self.assertEqual(request.status_code, 412)

        # 메모 등록
        body = {'title' : '메모 Test', 'content' : '매모 Test'}
        request = c.post('/apis/memos/', body, headers=user1_headers)

        self.assertEqual(request.status_code, 201)

        # 메모 수정
        body = {'title' : '메모 Test', 'content' : '매모 Test'}
        request = c.put('/apis/memos/1/', body, headers=user1_headers)

        self.assertEqual(request.status_code, 201)

        # 메모 좋아요 
        request = c.get('/apis/memos/1/like/', body)

        self.assertEqual(request.status_code, 201)

        # 메모 검색
        body = {'relation' : '메모'}
        request = c.get('/apis/memos/search/', body)

        self.assertEqual(request.status_code, 201)

        # 사용자1
        user1 = Users.objects.get(username='test_user1')
        c.force_authenticate(user=user1)

        # 삭제 권한 없는 메모 삭제
        request = c.delete('/apis/memos/2/', body)

        self.assertEqual(request.status_code, 403)

        # 삭제 권한 있는 메모 삭제
        request = c.delete('/apis/memos/1/', body)

        self.assertEqual(request.status_code, 200)

        # 관리자
        admin = Users.objects.get(username='admin')
        c.force_authenticate(user=admin)

        # 관리자 권한 삭제
        request = c.delete('/apis/memos/2/', body)

        self.assertEqual(request.status_code, 200)
        