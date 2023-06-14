from math import ceil
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import MemoSerializer
from core.models import Memos


# 메모 ViewSet
class MemoViewSet(viewsets.ModelViewSet):
    # 메모 쿼리
    queryset = Memos.objects.order_by('-created_at')
    # 메모 Serializer
    serializer_class = MemoSerializer

    # POST METHOD
    def create(self, request):
        
        serializer = MemoSerializer(data=request.data)

        if serializer.is_valid():
            rtn = serializer.create(request, serializer.data)

            return Response(MemoSerializer(rtn).data, status=status.HTTP_201_CREATED)
        else:
            rtn = '유효하지 않은 정보입니다.'
            
            return Response(dict(msg=rtn), status=status.HTTP_412_PRECONDITION_FAILED)
        
    # PUT METHOD
    def update(self, request, pk=None):

        serializer = MemoSerializer(data=request.data)

        if serializer.is_valid():
            rtn = serializer.update(request, serializer.data, pk, status)

            return Response(dict(msg=rtn[0]), status=rtn[1])
        else:
            rtn = '유효하지 않은 정보입니다.'

            return Response(dict(msg=rtn), status=status.HTTP_412_PRECONDITION_FAILED)
    
    # DELETE METHOD 
    def destroy(self, request, pk=None):

        d_queryset = self.get_queryset().filter(pk=pk)

        if not d_queryset.exists():
            rtn, sta = ('존재하지 않는 메모입니다.', status.HTTP_404_NOT_FOUND)
        else:
            rtn, sta = (
                lambda writer, user, super : ('삭제가 완료되었습니다.', status.HTTP_200_OK) if writer == user or super
                    else ('삭제할 수 없는 메모입니다.', status.HTTP_403_FORBIDDEN)
            )(d_queryset[0].writer, request.user, request.user.is_superuser)

        if rtn == '삭제가 완료되었습니다.':
            d_queryset.delete()
        
        return Response(dict(msg=rtn), status=sta)
        
    # 좋아요 구현    
    @action(detail=True, methods=['get', 'post'])
    def like(self, request, pk=None):
        queryset = self.get_queryset().filter(pk=pk)

        # 메모가 존재하지 않는다면
        if not queryset.exists():
            rtn = '존재하지 않는 메모입니다.'

            return Response(dict(msg=rtn), status=status.HTTP_404_NOT_FOUND)
        else:
            rtn = queryset.first().clicked()

        return Response(dict(msg=rtn), status=status.HTTP_201_CREATED)
    
    # 키워드 검색
    @action(detail=False, methods=['get', 'post'])
    def search(self, request):
        
        # 키워드 및 값 받아오기
        relation = request.GET.get('relation', '내용')
        key = request.GET.get('key', '')

        # 포함하는 값 쿼리
        queryset = (lambda rel, q : q(keywords__keyword__icontains=key) if rel == '키워드' else (
            q(content__icontains=key).all() if rel == '내용' else q(title__icontains=key)
        ))(relation, self.get_queryset().filter)

        # 페이지 구현
        page = int(request.GET.get('page', 1))
        page_count = ceil(len(queryset)/9)

        # 앞으로 가기 / 뒤로 가기
        page_next = (lambda p, pc : f'{request.path}?page={page+1}' if p < pc else None)(page, page_count)
        page_previous = (lambda p : f'{request.path}?page={page-1}' if p > 1 else None)(page)

        page_queryset = self.paginate_queryset(queryset)
        
        serializer = MemoSerializer(page_queryset, many=True)

        # 이미지 앞 도메인 생성
        for ser in serializer.data:
            if ser['img'] is not None :
                ser['img'] = request.build_absolute_uri().split('/apis')[0] + ser['img']
        
        return Response({
            'count' : len(queryset), 'next' : page_next, 'previous' : page_previous, 'results' : serializer.data
        }, status=status.HTTP_201_CREATED)