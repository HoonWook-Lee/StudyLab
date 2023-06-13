from rest_framework import serializers
from core.models import Keywords, Users


# 유저 Serializer
class UserSerializer(serializers.ModelSerializer):

    # Users Model 에서 조회하고 싶은 Fields 선택
    class Meta:
        model = Users
        fields = ['username']

# 키워드 Serializer
class KeywordSerializer(serializers.ModelSerializer):
    writer = UserSerializer(read_only=True)
    count = serializers.IntegerField(source="memos.count", read_only=True)

    # Keywords Model 에서 모든 Fields 선택
    class Meta:
        model = Keywords
        fields = ['id', 'keyword', 'writer', 'count', 'created_at']

    # 키워드 생성
    def create(self, request, data):
        instance = Keywords()
        instance.keyword = data.get('keyword')
        instance.writer_id = request.user.id

        try:
            # iexact = 같은 문자열 찾기 (대소문자 구분하지 않음)
            Keywords.objects.get(keyword__iexact=data.get('keyword'))
        except:
            # 키워드 생성
            instance.save()
            msg = '키워드 등록이 완료되었습니다.'
        else:
            # 중복 오류
            msg = '이미 등록된 키워드입니다.'

        return msg