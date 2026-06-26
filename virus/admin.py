from django.contrib import admin
from .models import Kategori, Virus


@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    list_display = ['id', 'nama_kategori', 'deskripsi', 'created_at']
    search_fields = ['nama_kategori']
    ordering = ['nama_kategori']


@admin.register(Virus)
class VirusAdmin(admin.ModelAdmin):
    list_display = ['id', 'nama_virus', 'nama_ilmiah', 'kategori', 'bentuk', 'created_at']
    list_filter = ['kategori', 'bentuk']
    search_fields = ['nama_virus', 'nama_ilmiah']
    ordering = ['nama_virus']