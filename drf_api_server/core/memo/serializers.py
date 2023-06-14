from rest_framework import serializers
from core.models import *


# 유저 Serializer
class UserSerializer(serializers.ModelSerializer):

    # Users Model 에서 조회하고 싶은 Fields 선택
    class Meta:
        model = Users
        fields = ['username', 'hint', 'date_joined', 'last_login']

# 메모 Serializer
class MemoSerializer(serializers.ModelSerializer):
    writer = UserSerializer(read_only=True)
    keywords = serializers.SlugRelatedField(many=True, read_only=True, slug_field='keyword')

    # Memos Model 에서 모든 Fields 선택
    class Meta:
        model = Memos
        fields = '__all__'

    # 메모 생성
    def create(self, request, data, commit=True):
        # 데이터 지정
        instance = Memos()
        instance.writer_id = request.user.id
        instance.title = data.get('title')
        instance.content = data.get('content')
        instance.img = (lambda x : None if x.get('img') == None else x['img'])(request.FILES)

        # 키워드
        keywords = request.data.getlist('keywords')
        
        if commit:
            # 메모 생성
            instance.save()

            # 키워드가 있다면 키워드 추가
            if keywords:
                list(map(lambda x : instance.keywords.add(Keywords.objects.get(pk=x)), keywords))
        
        return instance
    
    # 메모 수정
    def update(self, request, data, pk, status):
        # 데이터 지정
        instance = Memos.objects.get(pk=pk)
        instance.title = data.get('title')
        instance.content = data.get('content')

        # 키워드
        keywords = request.data.getlist('keywords')

        commit = (
            lambda writer, user, super : True if writer == user or super else False
        )(instance.writer, request.user, request.user.is_superuser)

        if commit:
            # 이미지 변경이 있다면 변경
            if request.FILES.get('img') != None:
                instance.img = request.FILES['img']

            # 메모 수정    
            instance.save()
            res = '메모 수정이 완료되었습니다.', status.HTTP_201_CREATED

            # 키워드가 있다면 키워드 변경
            if keywords:
                instance.keywords.clear() # 기존 삭제
                list(map(lambda x : instance.keywords.add(Keywords.objects.get(pk=x)), keywords))
        else:
            res = '수정할 수 없는 메모입니다.', status.HTTP_403_FORBIDDEN

        return res