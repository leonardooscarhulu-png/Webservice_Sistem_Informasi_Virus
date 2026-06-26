from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.db.models import Q

from .models import Kategori, Virus
from .serializers import KategoriSerializer, VirusSerializer, VirusListSerializer


class KategoriViewSet(viewsets.ModelViewSet):
    queryset = Kategori.objects.all()
    serializer_class = KategoriSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nama_kategori', 'deskripsi']
    ordering_fields = ['nama_kategori', 'created_at']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        jumlah_virus = instance.virus_list.count()
        if jumlah_virus > 0:
            return Response(
                {
                    'status': 'error',
                    'message': f'Kategori tidak dapat dihapus karena masih memiliki {jumlah_virus} virus terkait.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_destroy(instance)
        return Response(
            {'status': 'success', 'message': 'Kategori berhasil dihapus.'},
            status=status.HTTP_200_OK
        )


class VirusViewSet(viewsets.ModelViewSet):
    queryset = Virus.objects.select_related('kategori').all()
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nama_virus', 'nama_ilmiah', 'deskripsi', 'kategori__nama_kategori']
    ordering_fields = ['nama_virus', 'bentuk', 'created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return VirusListSerializer
        return VirusSerializer

    def get_queryset(self):
        queryset = Virus.objects.select_related('kategori').all()
        kategori_id = self.request.query_params.get('kategori_id')
        if kategori_id:
            queryset = queryset.filter(kategori_id=kategori_id)
        bentuk = self.request.query_params.get('bentuk')
        if bentuk:
            queryset = queryset.filter(bentuk=bentuk)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                'status': 'success',
                'message': 'Data virus berhasil ditambahkan.',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {
                'status': 'success',
                'message': 'Data virus berhasil diperbarui.',
                'data': serializer.data
            }
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        nama = instance.nama_virus
        if instance.gambar:
            instance.gambar.delete(save=False)
        self.perform_destroy(instance)
        return Response(
            {'status': 'success', 'message': f'Virus "{nama}" berhasil dihapus.'},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response(
                {'status': 'error', 'message': 'Parameter pencarian (q) diperlukan.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        queryset = Virus.objects.filter(
            Q(nama_virus__icontains=query) |
            Q(nama_ilmiah__icontains=query) |
            Q(deskripsi__icontains=query) |
            Q(kategori__nama_kategori__icontains=query)
        ).select_related('kategori')
        serializer = VirusListSerializer(queryset, many=True, context={'request': request})
        return Response({
            'status': 'success',
            'query': query,
            'count': queryset.count(),
            'results': serializer.data
        })

    @action(detail=False, methods=['get'])
    def by_bentuk(self, request):
        bentuk_list = [
            {'value': k, 'label': v}
            for k, v in Virus.BENTUK_CHOICES
        ]
        return Response({
            'status': 'success',
            'data': bentuk_list
        })