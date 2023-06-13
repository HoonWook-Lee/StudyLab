from rest_framework import viewsets, permissions, status
from .serializers import KeywordSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from core.models import Keywords


# 키워드 ViewSet
class KeywordViewSet(viewsets.ModelViewSet):
    # 키워드 쿼리
    queryset = Keywords.objects.order_by('-created_at')
    # 키워드 Serializer
    serializer_class = KeywordSerializer

    # POST METHOD
    def create(self, request):

        serializer = KeywordSerializer(data=request.data)

        if serializer.is_valid():
            rtn = serializer.create(request, serializer.data)

            return (
                lambda r : Response(dict(msg=r), status=status.HTTP_422_UNPROCESSABLE_ENTITY) if r[:2] == '이미'
                    else Response(dict(msg=r), status=status.HTTP_201_CREATED)
            )(rtn)
        else:
            rtn = '유효하지 않은 정보입니다.'
            
            return Response(dict(msg=rtn), status=status.HTTP_400_BAD_REQUEST)

    # DELETE METHOD 
    def destroy(self, request, pk=None):

        d_queryset = self.get_queryset().filter(pk=pk)

        if not d_queryset.exists():
            rtn, sta = ('존재하지 않는 메모입니다.', status.HTTP_404_NOT_FOUND)
        else:
            rtn, sta = (
                lambda writer, user, super : ('삭제가 완료되었습니다.', status.HTTP_200_OK) if writer == user or super
                    else ('삭제 권한을 가지고 있지 않습니다.', status.HTTP_403_FORBIDDEN)
            )(d_queryset[0].writer, request.user, request.user.is_superuser)

        if rtn == '삭제가 완료되었습니다.':
            d_queryset.delete()
        
        return Response(dict(msg=rtn), status=sta)
    
    # 모든 키워드 제공
    @action(detail=False, methods=['get'])
    def all(self, request):
        queryset = self.get_queryset().all()

        res = dict(results = list(map(lambda q : dict(id = q.id, keyword = q.keyword) ,queryset)))

        return Response(res, status=status.HTTP_201_CREATED)
    
