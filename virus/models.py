from django.db import models


class Kategori(models.Model):
    nama_kategori = models.CharField(max_length=100, unique=True)
    deskripsi = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'kategori'
        ordering = ['nama_kategori']
        verbose_name = 'Kategori'
        verbose_name_plural = 'Kategori'

    def __str__(self):
        return self.nama_kategori


class Virus(models.Model):
    BENTUK_CHOICES = [
        ('helical', 'Helical'),
        ('icosahedral', 'Icosahedral'),
        ('prolate', 'Prolate'),
        ('envelope', 'Envelope'),
        ('complex', 'Complex'),
    ]

    nama_virus = models.CharField(max_length=200)
    nama_ilmiah = models.CharField(max_length=200, unique=True)
    kategori = models.ForeignKey(
        Kategori,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='virus_list'
    )
    deskripsi = models.TextField()
    cara_berkembang_biak = models.TextField()
    bentuk = models.CharField(max_length=50, choices=BENTUK_CHOICES)
    gambar = models.ImageField(upload_to='virus/gambar/', blank=True, null=True)
    referensi = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'virus'
        ordering = ['nama_virus']
        verbose_name = 'Virus'
        verbose_name_plural = 'Virus'

    def __str__(self):
        return f"{self.nama_virus} ({self.nama_ilmiah})"