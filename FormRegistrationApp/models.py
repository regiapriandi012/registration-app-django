from django.db import models

class RegistrationData(models.Model):
    nomor_invoice = models.CharField(max_length=254, unique=True)
    tanggal = models.CharField(max_length=254)
    email = models.EmailField(max_length=254)
    nama_lengkap = models.CharField(max_length=254)
    nomor_telefon = models.CharField(max_length=254)
    program_studi = models.CharField(max_length=254)
    universitas = models.CharField(max_length=254)
    informasi_mengenai_torche = models.CharField(max_length=254)
    metode_pembelajaran = models.CharField(max_length=254)
    mata_kuliah = models.CharField(max_length=254)
    materi = models.CharField(max_length=5000)
    aplikasi_simulasi = models.CharField(max_length=254)
    jumlah_sesi_yang_diikuti = models.CharField(max_length=254)
    jumlah_peserta = models.CharField(max_length=10)
    lampiran = models.FileField(upload_to='documents/%Y/%m/%d')
    sesi_hari = models.CharField(max_length=254)
    sesi_jam = models.CharField(max_length=254)
    biaya = models.CharField(max_length=254)
    notes_for_tutor = models.CharField(max_length=5000)
    referral_code = models.CharField(max_length=254)
    email_1 = models.CharField(max_length=1000)
    nama_lengkap_1 = models.CharField(max_length=1000)
    nomor_telefon_1 = models.CharField(max_length=1000)
    akun_discord_1 = models.CharField(max_length=1000)
    email_2 = models.CharField(max_length=1000)
    nama_lengkap_2 = models.CharField(max_length=1000)
    nomor_telefon_2 = models.CharField(max_length=1000)
    akun_discord_2 = models.CharField(max_length=1000)
    email_3 = models.CharField(max_length=1000)
    nama_lengkap_3 = models.CharField(max_length=1000)
    nomor_telefon_3 = models.CharField(max_length=1000)
    akun_discord_3 = models.CharField(max_length=1000)
    email_4 = models.CharField(max_length=1000)
    nama_lengkap_4 = models.CharField(max_length=1000)
    nomor_telefon_4 = models.CharField(max_length=1000)
    akun_discord_4 = models.CharField(max_length=1000)
    email_5 = models.CharField(max_length=1000)
    nama_lengkap_5 = models.CharField(max_length=1000)
    nomor_telefon_5 = models.CharField(max_length=1000)
    akun_discord_5 = models.CharField(max_length=1000)
    email_6 = models.CharField(max_length=1000)
    nama_lengkap_6 = models.CharField(max_length=1000)
    nomor_telefon_6 = models.CharField(max_length=1000)
    akun_discord_6 = models.CharField(max_length=1000)
    email_7 = models.CharField(max_length=1000)
    nama_lengkap_7 = models.CharField(max_length=1000)
    nomor_telefon_7 = models.CharField(max_length=1000)
    akun_discord_7 = models.CharField(max_length=1000)
    email_8 = models.CharField(max_length=1000)
    nama_lengkap_8 = models.CharField(max_length=1000)
    nomor_telefon_8 = models.CharField(max_length=1000)
    akun_discord_8 = models.CharField(max_length=1000)
    email_9 = models.CharField(max_length=1000)
    nama_lengkap_9 = models.CharField(max_length=1000)
    nomor_telefon_9 = models.CharField(max_length=1000)
    akun_discord_9 = models.CharField(max_length=1000)
    email_10 = models.CharField(max_length=1000)
    nama_lengkap_10 = models.CharField(max_length=1000)
    nomor_telefon_10 = models.CharField(max_length=1000)
    akun_discord_10 = models.CharField(max_length=1000)

class ReferralCode(models.Model):
    referral_code = models.CharField(max_length=254)