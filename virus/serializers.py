from rest_framework import serializers
from .models import Kategori, Virus


class KategoriSerializer(serializers.ModelSerializer):
    jumlah_virus = serializers.SerializerMethodField()

    class Meta:
        model = Kategori
        fields = [
            'id', 'nama_kategori', 'deskripsi',
            'jumlah_virus', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_jumlah_virus(self, obj):
        return obj.virus_list.count()


class VirusListSerializer(serializers.ModelSerializer):
    kategori_nama = serializers.CharField(source='kategori.nama_kategori', read_only=True)
    bentuk_display = serializers.CharField(source='get_bentuk_display', read_only=True)
    gambar_url = serializers.SerializerMethodField()

    class Meta:
        model = Virus
        fields = [
            'id', 'nama_virus', 'nama_ilmiah', 'kategori_nama',
            'bentuk_display', 'gambar_url', 'created_at'
        ]

    def get_gambar_url(self, obj):
        request = self.context.get('request')
        if obj.gambar and request:
            return request.build_absolute_uri(obj.gambar.url)
        return None


class VirusSerializer(serializers.ModelSerializer):
    kategori_detail = KategoriSerializer(source='kategori', read_only=True)
    gambar_url = serializers.SerializerMethodField()
    bentuk_display = serializers.CharField(source='get_bentuk_display', read_only=True)

    class Meta:
        model = Virus
        fields = [
            'id', 'nama_virus', 'nama_ilmiah', 'kategori', 'kategori_detail',
            'deskripsi', 'cara_berkembang_biak', 'bentuk', 'bentuk_display',
            'gambar', 'gambar_url', 'referensi', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'gambar': {'write_only': True, 'required': False},
            'kategori': {'write_only': True, 'required': False},
        }

    def get_gambar_url(self, obj):
        request = self.context.get('request')
        if obj.gambar and request:
            return request.build_absolute_uri(obj.gambar.url)
        return None