from django.shortcuts import render, redirect
from .forms import SessionCSEForm, SessionCEMForm, \
    SessionCETForm, SessionCPSForm, SessionCREForm, SessionEECForm, SessionFACForm, \
    SessionFCAForm, SessionFCHForm, SessionFHTForm, SessionFMTForm, SessionFPMForm, \
    SessionFP1Form, SessionFP2Form, SessionMEBForm, SessionNCEForm, SessionOCEForm, \
    SessionPCDForm, SessionPDDForm, SessionPEDForm, SessionPPDForm, SessionTPHForm, \
    JadwalBelajarForm, MetodePembelajaranForm, SessionPCHForm, SessionSPRForm, LampiranFileForm
from .models import RegistrationData, ReferralCode
import datetime
from io import BytesIO
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.template.loader import render_to_string

NAMA_MATA_KULIAH = (
    ("Cell Culture for Engineers", "Cell Culture for Engineers"),
    ("Chemical Engineering Mathematics", "Chemical Engineering Mathematics"),
    ("Chemical Engineering Thermodynamics", "Chemical Engineering Thermodynamics"),
    ("Chemical Process Simulation", "Chemical Process Simulation"),
    ("Chemical Reaction Engineering", "Chemical Reaction Engineering"),
    ("Engineering Economy", "Engineering Economy"),
    ("Fundamentals of Analytical Chemistry", "Fundamentals of Analytical Chemistry"),
    ("Fundamentals of Calculus", "Fundamentals of Calculus"),
    ("Fundamentals of Chemistry", "Fundamentals of Chemistry"),
    ("Fundamentals of Heat Transfer", "Fundamentals of Heat Transfer"),
    ("Fundamentals of Mass Transfer", "Fundamentals of Mass Transfer"),
    ("Fluid and Particles Mechanics", "Fluid and Particles Mechanics"),
    ("Fundamentals of Physics 1", "Fundamentals of Physics 1"),
    ("Fundamentals of Physics 2", "Fundamentals of Physics 2"),
    ("Mass and Energy Balances", "Mass and Energy Balances"),
    ("Numerical Computation for Engineers", "Numerical Computation for Engineers"),
    ("Organic Chemistry for Engineers", "Organic Chemistry for Engineers"),
    ("Process Control and Dynamics", "Process Control and Dynamics"),
    ("Physical Chemistry", "Physical Chemistry"),
    ("Product Design and Development", "Product Design and Development"),
    ("Process Equipment Design", "Process Equipment Design"),
    ("Process Plant Design", "Process Plant Design"),
    ("Statistics and Probability", "Statistics and Probability"),
    ("Transport Phenomena", "Transport Phenomena")
)

registration_number_q1 = 0
registration_number_q2 = 0
registration_number_q3 = 0
registration_number_q4 = 0

registration_number_q1_invoice = ""
registration_number_q2_invoice = ""
registration_number_q3_invoice = ""
registration_number_q4_invoice = ""


# Create your views here.
def home_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        nama_lengkap = request.POST.get('nama_lengkap')
        nomor_telefon = request.POST.get('nomor_telefon')
        program_studi = request.POST.get('program_studi')
        angkatan = request.POST.get('angkatan')
        universitas = request.POST.get('universitas')
        info_torche = str(request.POST.getlist('tentang_torche')).replace("Other",
                                                                          request.POST.get('tentang_torche_other'))
        if program_studi == "Other":
            program_studi = request.POST.get('program_studi_other')
        else:
            program_studi = request.POST.get('program_studi')
        if universitas == "Other":
            universitas = request.POST.get('universitas_other')
        else:
            universitas = request.POST.get('universitas')
        return redirect("metode_pembelajaran", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                        info_torche)
    return render(request, "FormRegistrationApp/index.html")


# ---------------------------------------------------------------------------------------------------------
def metode_pembelajaran(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche):
    context = {'form': MetodePembelajaranForm()}
    if request.method == 'POST':
        form = MetodePembelajaranForm(request.POST)
        if form.is_valid():
            metode_pembelajaran = form.cleaned_data['metode_pembelajaran']
            jumlah_sesi_yang_diikuti = form.cleaned_data['jumlah_sesi_yang_diikuti']
            return redirect("mata_kuliah", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti)
    else:
        form = MetodePembelajaranForm(request.POST)
    return render(request, "FormRegistrationApp/metode_pembelajaran.html", context)


# ---------------------------------------------------------------------------------------------------------
def mata_kuliah(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche,
                metode_pembelajaran, jumlah_sesi_yang_diikuti):
    if request.method == 'POST':
        mata_kuliah = request.POST.get('mata_kuliah')
        if mata_kuliah == "Other":
            mata_kuliah = request.POST.get('mata_kuliah_other')
        else:
            mata_kuliah = request.POST.get('mata_kuliah')
        if mata_kuliah == NAMA_MATA_KULIAH[0][0]:
            return redirect("session_cse", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah)
        elif mata_kuliah == NAMA_MATA_KULIAH[1][0]:
            return redirect("session_cem", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah)
        elif mata_kuliah == NAMA_MATA_KULIAH[2][0]:
            return redirect("session_cet", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah)
        elif mata_kuliah == NAMA_MATA_KULIAH[3][0]:
            return redirect("session_cps", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah)
        elif mata_kuliah == NAMA_MATA_KULIAH[4][0]:
            return redirect("session_cre", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah)
        elif mata_kuliah == NAMA_MATA_KULIAH[5][0]:
            return redirect("session_eec", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah)
        elif mata_kuliah == NAMA_MATA_KULIAH[6][0]:
            return redirect("session_fac", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah)
        elif mata_kuliah == NAMA_MATA_KULIAH[7][0]:
            return redirect("session_fca", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah)
        elif mata_kuliah == NAMA_MATA_KULIAH[8][0]:
            return redirect("session_fch", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah)
        elif mata_kuliah == NAMA_MATA_KULIAH[9][0]:
            return redirect("session_fht", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah)
        elif mata_kuliah == NAMA_MATA_KULIAH[10][0]:
            return redirect("session_fmt", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah)
        elif mata_kuliah == NAMA_MATA_KULIAH[11][0]:
            return redirect("session_fpm", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah)
        elif mata_kuliah == NAMA_MATA_KULIAH[12][0]:
            return redirect("session_fp1", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah)
        elif mata_kuliah == NAMA_MATA_KULIAH[13][0]:
            return redirect("session_fp2", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah)
        elif mata_kuliah == NAMA_MATA_KULIAH[14][0]:
            return redirect("session_meb", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah)
        elif mata_kuliah == NAMA_MATA_KULIAH[15][0]:
            return redirect("session_nce", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah)
        elif mata_kuliah == NAMA_MATA_KULIAH[16][0]:
            return redirect("session_oce", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah)
        elif mata_kuliah == NAMA_MATA_KULIAH[17][0]:
            return redirect("session_pcd", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah)
        elif mata_kuliah == NAMA_MATA_KULIAH[18][0]:
            return redirect("session_pch", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah)
        elif mata_kuliah == NAMA_MATA_KULIAH[19][0]:
            return redirect("session_pdd", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah)
        elif mata_kuliah == NAMA_MATA_KULIAH[20][0]:
            return redirect("session_ped", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah)
        elif mata_kuliah == NAMA_MATA_KULIAH[21][0]:
            return redirect("session_ppd", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah)
        elif mata_kuliah == NAMA_MATA_KULIAH[22][0]:
            return redirect("session_spr", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah)
        elif mata_kuliah == NAMA_MATA_KULIAH[23][0]:
            return redirect("session_tph", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah)
    return render(request, "FormRegistrationApp/mata_kuliah.html")


# ---------------------------------------------------------------------------------------------------------
def session_cse(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche,
                metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah):
    context = {'form': SessionCSEForm()}
    if request.method == 'POST':
        form = SessionCSEForm(request.POST)
        if form.is_valid():
            materi = form.cleaned_data['materi']
            simulasi = "-"
            return redirect("lampiran", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi)
    else:
        form = SessionCSEForm(request.POST)
    return render(request, "FormRegistrationApp/session_cse.html", context)


# ---------------------------------------------------------------------------------------------------------
def session_cem(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche,
                metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah):
    context = {'form': SessionCEMForm()}
    if request.method == 'POST':
        form = SessionCEMForm(request.POST)
        if form.is_valid():
            materi = form.cleaned_data['materi']
            simulasi = "-"
            return redirect("lampiran", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi)
    else:
        form = SessionCEMForm(request.POST)
    return render(request, "FormRegistrationApp/session_cem.html", context)


# ---------------------------------------------------------------------------------------------------------
def session_cet(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche,
                metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah):
    context = {'form': SessionCETForm()}
    if request.method == 'POST':
        form = SessionCETForm(request.POST)
        if form.is_valid():
            materi = form.cleaned_data['materi']
            simulasi = "-"
            return redirect("lampiran", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi)
    else:
        form = SessionCETForm(request.POST)
    return render(request, "FormRegistrationApp/session_cet.html", context)


# ---------------------------------------------------------------------------------------------------------
def session_cps(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche,
                metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah):
    if request.method == 'POST':
        materi = request.POST.getlist('materi')
        simulasi = request.POST.get('simulasi')
        if simulasi == "Other":
            simulasi = request.POST.get('simulasi_other')
        else:
            simulasi = request.POST.get('simulasi')
            return redirect("lampiran", email, nama_lengkap, nomor_telefon, program_studi, angkatan,
                            universitas, info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah,
                            materi, simulasi)
    return render(request, "FormRegistrationApp/session_cps.html")


# ---------------------------------------------------------------------------------------------------------
def session_cre(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche,
                metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah):
    context = {'form': SessionCREForm()}
    if request.method == 'POST':
        form = SessionCREForm(request.POST)
        if form.is_valid():
            materi = form.cleaned_data['materi']
            simulasi = "-"
            return redirect("lampiran", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi)
    else:
        form = SessionCREForm(request.POST)
    return render(request, "FormRegistrationApp/session_cre.html", context)


# ---------------------------------------------------------------------------------------------------------
def session_eec(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche,
                metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah):
    context = {'form': SessionEECForm()}
    if request.method == 'POST':
        form = SessionEECForm(request.POST)
        if form.is_valid():
            materi = form.cleaned_data['materi']
            simulasi = "-"
            return redirect("lampiran", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi)
    else:
        form = SessionEECForm(request.POST)
    return render(request, "FormRegistrationApp/session_eec.html", context)


# ---------------------------------------------------------------------------------------------------------
def session_fac(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche,
                metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah):
    context = {'form': SessionFACForm()}
    if request.method == 'POST':
        form = SessionFACForm(request.POST)
        if form.is_valid():
            materi = form.cleaned_data['materi']
            simulasi = "-"
            return redirect("lampiran", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi)
    else:
        form = SessionFACForm(request.POST)
    return render(request, "FormRegistrationApp/session_fac.html", context)


# ---------------------------------------------------------------------------------------------------------
def session_fca(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche,
                metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah):
    context = {'form': SessionFCAForm()}
    if request.method == 'POST':
        form = SessionFCAForm(request.POST)
        if form.is_valid():
            materi = form.cleaned_data['materi']
            simulasi = "-"
            return redirect("lampiran", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi)
    else:
        form = SessionFCAForm(request.POST)
    return render(request, "FormRegistrationApp/session_fca.html", context)


# ---------------------------------------------------------------------------------------------------------
def session_fch(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche,
                metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah):
    context = {'form': SessionFCHForm()}
    if request.method == 'POST':
        form = SessionFCHForm(request.POST)
        if form.is_valid():
            materi = form.cleaned_data['materi']
            simulasi = "-"
            return redirect("lampiran", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi)
    else:
        form = SessionFCHForm(request.POST)
    return render(request, "FormRegistrationApp/session_fch.html", context)


# ---------------------------------------------------------------------------------------------------------
def session_fht(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche,
                metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah):
    context = {'form': SessionFHTForm()}
    if request.method == 'POST':
        form = SessionFHTForm(request.POST)
        if form.is_valid():
            materi = form.cleaned_data['materi']
            simulasi = "-"
            return redirect("lampiran", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi)
    else:
        form = SessionFHTForm(request.POST)
    return render(request, "FormRegistrationApp/session_fht.html", context)


# ---------------------------------------------------------------------------------------------------------
def session_fmt(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche,
                metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah):
    context = {'form': SessionFMTForm()}
    if request.method == 'POST':
        form = SessionFMTForm(request.POST)
        if form.is_valid():
            materi = form.cleaned_data['materi']
            simulasi = "-"
            return redirect("lampiran", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi)
    else:
        form = SessionFMTForm(request.POST)
    return render(request, "FormRegistrationApp/session_fmt.html", context)


# ---------------------------------------------------------------------------------------------------------
def session_fpm(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche,
                metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah):
    context = {'form': SessionFPMForm()}
    if request.method == 'POST':
        form = SessionFPMForm(request.POST)
        if form.is_valid():
            materi = form.cleaned_data['materi']
            simulasi = "-"
            return redirect("lampiran", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi)
    else:
        form = SessionFPMForm(request.POST)
    return render(request, "FormRegistrationApp/session_fpm.html", context)


# ---------------------------------------------------------------------------------------------------------
def session_fp1(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche,
                metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah):
    context = {'form': SessionFP1Form()}
    if request.method == 'POST':
        form = SessionFP1Form(request.POST)
        if form.is_valid():
            materi = form.cleaned_data['materi']
            simulasi = "-"
            return redirect("lampiran", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi)
    else:
        form = SessionFP1Form(request.POST)
    return render(request, "FormRegistrationApp/session_fp1.html", context)


# ---------------------------------------------------------------------------------------------------------
def session_fp2(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche,
                metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah):
    context = {'form': SessionFP2Form()}
    if request.method == 'POST':
        form = SessionFP2Form(request.POST)
        if form.is_valid():
            materi = form.cleaned_data['materi']
            simulasi = "-"
            return redirect("lampiran", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi)
    else:
        form = SessionFP2Form(request.POST)
    return render(request, "FormRegistrationApp/session_fp2.html", context)


# ---------------------------------------------------------------------------------------------------------
def session_meb(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche,
                metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah):
    context = {'form': SessionMEBForm()}
    if request.method == 'POST':
        form = SessionMEBForm(request.POST)
        if form.is_valid():
            materi = form.cleaned_data['materi']
            simulasi = "-"
            return redirect("lampiran", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi)
    else:
        form = SessionMEBForm(request.POST)
    return render(request, "FormRegistrationApp/session_meb.html", context)


# ---------------------------------------------------------------------------------------------------------
def session_nce(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche,
                metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah):
    context = {'form': SessionNCEForm()}
    if request.method == 'POST':
        form = SessionNCEForm(request.POST)
        if form.is_valid():
            materi = form.cleaned_data['materi']
            simulasi = "-"
            return redirect("lampiran", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi)
    else:
        form = SessionNCEForm(request.POST)
    return render(request, "FormRegistrationApp/session_nce.html", context)


# ---------------------------------------------------------------------------------------------------------
def session_oce(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche,
                metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah):
    context = {'form': SessionOCEForm()}
    if request.method == 'POST':
        form = SessionOCEForm(request.POST)
        if form.is_valid():
            materi = form.cleaned_data['materi']
            simulasi = "-"
            return redirect("lampiran", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi)
    else:
        form = SessionOCEForm(request.POST)
    return render(request, "FormRegistrationApp/session_oce.html", context)


# ---------------------------------------------------------------------------------------------------------
def session_pcd(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche,
                metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah):
    context = {'form': SessionPCDForm()}
    if request.method == 'POST':
        form = SessionPCDForm(request.POST)
        if form.is_valid():
            materi = form.cleaned_data['materi']
            simulasi = "-"
            return redirect("lampiran", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi)
    else:
        form = SessionPCDForm(request.POST)
    return render(request, "FormRegistrationApp/session_pcd.html", context)


# ---------------------------------------------------------------------------------------------------------
def session_pch(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche,
                metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah):
    context = {'form': SessionPCHForm()}
    if request.method == 'POST':
        form = SessionPCHForm(request.POST)
        if form.is_valid():
            materi = form.cleaned_data['materi']
            simulasi = "-"
            return redirect("lampiran", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi)
    else:
        form = SessionPCHForm(request.POST)
    return render(request, "FormRegistrationApp/session_pch.html", context)


# ---------------------------------------------------------------------------------------------------------
def session_pdd(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche,
                metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah):
    context = {'form': SessionPDDForm()}
    if request.method == 'POST':
        form = SessionPDDForm(request.POST)
        if form.is_valid():
            materi = form.cleaned_data['materi']
            simulasi = "-"
            return redirect("lampiran", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi)
    else:
        form = SessionPDDForm(request.POST)
    return render(request, "FormRegistrationApp/session_pdd.html", context)


# ---------------------------------------------------------------------------------------------------------
def session_ped(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche,
                metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah):
    context = {'form': SessionPEDForm()}
    if request.method == 'POST':
        form = SessionPEDForm(request.POST)
        if form.is_valid():
            materi = form.cleaned_data['materi']
            simulasi = "-"
            return redirect("lampiran", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi)
    else:
        form = SessionPEDForm(request.POST)
    return render(request, "FormRegistrationApp/session_ped.html", context)


# ---------------------------------------------------------------------------------------------------------
def session_ppd(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche,
                metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah):
    context = {'form': SessionPPDForm()}
    if request.method == 'POST':
        form = SessionPPDForm(request.POST)
        if form.is_valid():
            materi = form.cleaned_data['materi']
            simulasi = "-"
            return redirect("lampiran", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi)
    else:
        form = SessionPPDForm(request.POST)
    return render(request, "FormRegistrationApp/session_ppd.html", context)


# ---------------------------------------------------------------------------------------------------------
def session_spr(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche,
                metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah):
    context = {'form': SessionSPRForm()}
    if request.method == 'POST':
        form = SessionSPRForm(request.POST)
        if form.is_valid():
            materi = form.cleaned_data['materi']
            simulasi = "-"
            return redirect("lampiran", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi)
    else:
        form = SessionSPRForm(request.POST)
    return render(request, "FormRegistrationApp/session_spr.html", context)


# ---------------------------------------------------------------------------------------------------------
def session_tph(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche,
                metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah):
    context = {'form': SessionTPHForm()}
    if request.method == 'POST':
        form = SessionTPHForm(request.POST)
        if form.is_valid():
            materi = form.cleaned_data['materi']
            simulasi = "-"
            return redirect("lampiran", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi)
    else:
        form = SessionTPHForm(request.POST)
    return render(request, "FormRegistrationApp/session_tph.html", context)


# ---------------------------------------------------------------------------------------------------------
def lampiran(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
             info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi):
    context = {'form': LampiranFileForm()}
    if request.method == 'POST':
        form = LampiranFileForm(request.POST, request.FILES)
        if form.is_valid():
            lampiran = request.FILES['lampiran']
            return redirect("jumlah_peserta", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi,
                            lampiran)
    else:
        form = LampiranFileForm(request.POST, request.FILES)
    return render(request, "FormRegistrationApp/lampiran.html", context)


# ---------------------------------------------------------------------------------------------------------
def jumlah_peserta(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche,
                   metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi, lampiran):
    if request.method == 'POST':
        jumlah_peserta = request.POST.get('jumlah_peserta')
        email_1 = "-"
        nama_lengkap_1 = "-"
        nomor_telefon_1 = "-"
        akun_discord_1 = "-"
        email_2 = "-"
        nama_lengkap_2 = "-"
        nomor_telefon_2 = "-"
        akun_discord_2 = "-"
        email_3 = "-"
        nama_lengkap_3 = "-"
        nomor_telefon_3 = "-"
        akun_discord_3 = "-"
        email_4 = "-"
        nama_lengkap_4 = "-"
        nomor_telefon_4 = "-"
        akun_discord_4 = "-"
        email_5 = "-"
        nama_lengkap_5 = "-"
        nomor_telefon_5 = "-"
        akun_discord_5 = "-"
        email_6 = "-"
        nama_lengkap_6 = "-"
        nomor_telefon_6 = "-"
        akun_discord_6 = "-"
        email_7 = "-"
        nama_lengkap_7 = "-"
        nomor_telefon_7 = "-"
        akun_discord_7 = "-"
        email_8 = "-"
        nama_lengkap_8 = "-"
        nomor_telefon_8 = "-"
        akun_discord_8 = "-"
        email_9 = "-"
        nama_lengkap_9 = "-"
        nomor_telefon_9 = "-"
        akun_discord_9 = "-"
        email_10 = "-"
        nama_lengkap_10 = "-"
        nomor_telefon_10 = "-"
        akun_discord_10 = "-"
        if jumlah_peserta == "1":
            return redirect("jadwal_belajar", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi,
                            lampiran, jumlah_peserta, email_1, nama_lengkap_1, nomor_telefon_1, akun_discord_1,
                            email_2, nama_lengkap_2, nomor_telefon_2, akun_discord_2,
                            email_3, nama_lengkap_3, nomor_telefon_3, akun_discord_3,
                            email_4, nama_lengkap_4, nomor_telefon_4, akun_discord_4,
                            email_5, nama_lengkap_5, nomor_telefon_5, akun_discord_5,
                            email_6, nama_lengkap_6, nomor_telefon_6, akun_discord_6,
                            email_7, nama_lengkap_7, nomor_telefon_7, akun_discord_7,
                            email_8, nama_lengkap_8, nomor_telefon_8, akun_discord_8,
                            email_9, nama_lengkap_9, nomor_telefon_9, akun_discord_9,
                            email_10, nama_lengkap_10, nomor_telefon_10, akun_discord_10)
        else:
            return redirect("anggota_kelompok_1", email, nama_lengkap, nomor_telefon, program_studi, angkatan,
                            universitas, info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah,
                            materi, simulasi, lampiran, jumlah_peserta)
    return render(request, "FormRegistrationApp/jumlah_peserta.html")


# ---------------------------------------------------------------------------------------------------------
def anggota_kelompok_1(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche,
                       metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi, lampiran,
                       jumlah_peserta):
    if request.method == 'POST':
        email_1 = request.POST.get('email_1')
        nama_lengkap_1 = request.POST.get('nama_lengkap_1')
        nomor_telefon_1 = request.POST.get('nomor_telefon_1')
        akun_discord_1 = request.POST.get('akun_discord_1')
        email_2 = "-"
        nama_lengkap_2 = "-"
        nomor_telefon_2 = "-"
        akun_discord_2 = "-"
        email_3 = "-"
        nama_lengkap_3 = "-"
        nomor_telefon_3 = "-"
        akun_discord_3 = "-"
        email_4 = "-"
        nama_lengkap_4 = "-"
        nomor_telefon_4 = "-"
        akun_discord_4 = "-"
        email_5 = "-"
        nama_lengkap_5 = "-"
        nomor_telefon_5 = "-"
        akun_discord_5 = "-"
        email_6 = "-"
        nama_lengkap_6 = "-"
        nomor_telefon_6 = "-"
        akun_discord_6 = "-"
        email_7 = "-"
        nama_lengkap_7 = "-"
        nomor_telefon_7 = "-"
        akun_discord_7 = "-"
        email_8 = "-"
        nama_lengkap_8 = "-"
        nomor_telefon_8 = "-"
        akun_discord_8 = "-"
        email_9 = "-"
        nama_lengkap_9 = "-"
        nomor_telefon_9 = "-"
        akun_discord_9 = "-"
        email_10 = "-"
        nama_lengkap_10 = "-"
        nomor_telefon_10 = "-"
        akun_discord_10 = "-"
        if jumlah_peserta == "1":
            return redirect("jadwal_belajar", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi,
                            lampiran, jumlah_peserta, email_1, nama_lengkap_1, nomor_telefon_1, akun_discord_1,
                            email_2, nama_lengkap_2, nomor_telefon_2, akun_discord_2,
                            email_3, nama_lengkap_3, nomor_telefon_3, akun_discord_3,
                            email_4, nama_lengkap_4, nomor_telefon_4, akun_discord_4,
                            email_5, nama_lengkap_5, nomor_telefon_5, akun_discord_5,
                            email_6, nama_lengkap_6, nomor_telefon_6, akun_discord_6,
                            email_7, nama_lengkap_7, nomor_telefon_7, akun_discord_7,
                            email_8, nama_lengkap_8, nomor_telefon_8, akun_discord_8,
                            email_9, nama_lengkap_9, nomor_telefon_9, akun_discord_9,
                            email_10, nama_lengkap_10, nomor_telefon_10, akun_discord_10
                            )
        else:
            return redirect("anggota_kelompok_2", email, nama_lengkap, nomor_telefon, program_studi, angkatan,
                            universitas, info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah,
                            materi, simulasi, lampiran, jumlah_peserta, email_1, nama_lengkap_1, nomor_telefon_1,
                            akun_discord_1)
    return render(request, "FormRegistrationApp/anggota_kelompok_1.html")


# ---------------------------------------------------------------------------------------------------------
def anggota_kelompok_2(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche,
                       metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi, lampiran,
                       jumlah_peserta, email_1, nama_lengkap_1, nomor_telefon_1, akun_discord_1):
    if request.method == 'POST':
        email_2 = request.POST.get('email_2')
        nama_lengkap_2 = request.POST.get('nama_lengkap_2')
        nomor_telefon_2 = request.POST.get('nomor_telefon_2')
        akun_discord_2 = request.POST.get('akun_discord_2')
        email_3 = "-"
        nama_lengkap_3 = "-"
        nomor_telefon_3 = "-"
        akun_discord_3 = "-"
        email_4 = "-"
        nama_lengkap_4 = "-"
        nomor_telefon_4 = "-"
        akun_discord_4 = "-"
        email_5 = "-"
        nama_lengkap_5 = "-"
        nomor_telefon_5 = "-"
        akun_discord_5 = "-"
        email_6 = "-"
        nama_lengkap_6 = "-"
        nomor_telefon_6 = "-"
        akun_discord_6 = "-"
        email_7 = "-"
        nama_lengkap_7 = "-"
        nomor_telefon_7 = "-"
        akun_discord_7 = "-"
        email_8 = "-"
        nama_lengkap_8 = "-"
        nomor_telefon_8 = "-"
        akun_discord_8 = "-"
        email_9 = "-"
        nama_lengkap_9 = "-"
        nomor_telefon_9 = "-"
        akun_discord_9 = "-"
        email_10 = "-"
        nama_lengkap_10 = "-"
        nomor_telefon_10 = "-"
        akun_discord_10 = "-"
        if jumlah_peserta == "2":
            return redirect("jadwal_belajar", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi,
                            lampiran, jumlah_peserta, email_1, nama_lengkap_1, nomor_telefon_1, akun_discord_1,
                            email_2, nama_lengkap_2, nomor_telefon_2, akun_discord_2,
                            email_3, nama_lengkap_3, nomor_telefon_3, akun_discord_3,
                            email_4, nama_lengkap_4, nomor_telefon_4, akun_discord_4,
                            email_5, nama_lengkap_5, nomor_telefon_5, akun_discord_5,
                            email_6, nama_lengkap_6, nomor_telefon_6, akun_discord_6,
                            email_7, nama_lengkap_7, nomor_telefon_7, akun_discord_7,
                            email_8, nama_lengkap_8, nomor_telefon_8, akun_discord_8,
                            email_9, nama_lengkap_9, nomor_telefon_9, akun_discord_9,
                            email_10, nama_lengkap_10, nomor_telefon_10, akun_discord_10
                            )
        else:
            return redirect("anggota_kelompok_3", email, nama_lengkap, nomor_telefon, program_studi, angkatan,
                            universitas, info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah,
                            materi, simulasi, lampiran, jumlah_peserta, email_1, nama_lengkap_1, nomor_telefon_1,
                            akun_discord_1,
                            email_2, nama_lengkap_2, nomor_telefon_2,
                            akun_discord_2)
    return render(request, "FormRegistrationApp/anggota_kelompok_2.html")


# ---------------------------------------------------------------------------------------------------------
def anggota_kelompok_3(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche,
                       metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi, lampiran,
                       jumlah_peserta, email_1, nama_lengkap_1, nomor_telefon_1, akun_discord_1,
                       email_2, nama_lengkap_2, nomor_telefon_2, akun_discord_2):
    if request.method == 'POST':
        email_3 = request.POST.get('email_3')
        nama_lengkap_3 = request.POST.get('nama_lengkap_3')
        nomor_telefon_3 = request.POST.get('nomor_telefon_3')
        akun_discord_3 = request.POST.get('akun_discord_3')
        email_4 = "-"
        nama_lengkap_4 = "-"
        nomor_telefon_4 = "-"
        akun_discord_4 = "-"
        email_5 = "-"
        nama_lengkap_5 = "-"
        nomor_telefon_5 = "-"
        akun_discord_5 = "-"
        email_6 = "-"
        nama_lengkap_6 = "-"
        nomor_telefon_6 = "-"
        akun_discord_6 = "-"
        email_7 = "-"
        nama_lengkap_7 = "-"
        nomor_telefon_7 = "-"
        akun_discord_7 = "-"
        email_8 = "-"
        nama_lengkap_8 = "-"
        nomor_telefon_8 = "-"
        akun_discord_8 = "-"
        email_9 = "-"
        nama_lengkap_9 = "-"
        nomor_telefon_9 = "-"
        akun_discord_9 = "-"
        email_10 = "-"
        nama_lengkap_10 = "-"
        nomor_telefon_10 = "-"
        akun_discord_10 = "-"
        if jumlah_peserta == "3":
            return redirect("jadwal_belajar", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi,
                            lampiran, jumlah_peserta, email_1, nama_lengkap_1, nomor_telefon_1, akun_discord_1,
                            email_2, nama_lengkap_2, nomor_telefon_2, akun_discord_2, email_3,
                            nama_lengkap_3, nomor_telefon_3, akun_discord_3,
                            email_4, nama_lengkap_4, nomor_telefon_4, akun_discord_4,
                            email_5, nama_lengkap_5, nomor_telefon_5, akun_discord_5,
                            email_6, nama_lengkap_6, nomor_telefon_6, akun_discord_6,
                            email_7, nama_lengkap_7, nomor_telefon_7, akun_discord_7,
                            email_8, nama_lengkap_8, nomor_telefon_8, akun_discord_8,
                            email_9, nama_lengkap_9, nomor_telefon_9, akun_discord_9,
                            email_10, nama_lengkap_10, nomor_telefon_10, akun_discord_10
                            )
        else:
            return redirect("anggota_kelompok_4", email, nama_lengkap, nomor_telefon, program_studi, angkatan,
                            universitas, info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah,
                            materi, simulasi, lampiran, jumlah_peserta, email_1, nama_lengkap_1, nomor_telefon_1,
                            akun_discord_1,
                            email_2, nama_lengkap_2, nomor_telefon_2,
                            akun_discord_2, email_3, nama_lengkap_3, nomor_telefon_3, akun_discord_3)
    return render(request, "FormRegistrationApp/anggota_kelompok_3.html")


# ---------------------------------------------------------------------------------------------------------
def anggota_kelompok_4(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche,
                       metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi, lampiran,
                       jumlah_peserta, email_1, nama_lengkap_1, nomor_telefon_1, akun_discord_1,
                       email_2, nama_lengkap_2, nomor_telefon_2, akun_discord_2, email_3,
                       nama_lengkap_3, nomor_telefon_3, akun_discord_3):
    if request.method == 'POST':
        email_4 = request.POST.get('email_4')
        nama_lengkap_4 = request.POST.get('nama_lengkap_4')
        nomor_telefon_4 = request.POST.get('nomor_telefon_4')
        akun_discord_4 = request.POST.get('akun_discord_4')
        email_5 = "-"
        nama_lengkap_5 = "-"
        nomor_telefon_5 = "-"
        akun_discord_5 = "-"
        email_6 = "-"
        nama_lengkap_6 = "-"
        nomor_telefon_6 = "-"
        akun_discord_6 = "-"
        email_7 = "-"
        nama_lengkap_7 = "-"
        nomor_telefon_7 = "-"
        akun_discord_7 = "-"
        email_8 = "-"
        nama_lengkap_8 = "-"
        nomor_telefon_8 = "-"
        akun_discord_8 = "-"
        email_9 = "-"
        nama_lengkap_9 = "-"
        nomor_telefon_9 = "-"
        akun_discord_9 = "-"
        email_10 = "-"
        nama_lengkap_10 = "-"
        nomor_telefon_10 = "-"
        akun_discord_10 = "-"
        if jumlah_peserta == "4":
            return redirect("jadwal_belajar", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi,
                            lampiran, jumlah_peserta, email_1, nama_lengkap_1, nomor_telefon_1, akun_discord_1,
                            email_2, nama_lengkap_2, nomor_telefon_2, akun_discord_2, email_3,
                            nama_lengkap_3, nomor_telefon_3, akun_discord_3, email_4, nama_lengkap_4, nomor_telefon_4,
                            akun_discord_4,
                            email_5, nama_lengkap_5, nomor_telefon_5, akun_discord_5,
                            email_6, nama_lengkap_6, nomor_telefon_6, akun_discord_6,
                            email_7, nama_lengkap_7, nomor_telefon_7, akun_discord_7,
                            email_8, nama_lengkap_8, nomor_telefon_8, akun_discord_8,
                            email_9, nama_lengkap_9, nomor_telefon_9, akun_discord_9,
                            email_10, nama_lengkap_10, nomor_telefon_10, akun_discord_10
                            )
        else:
            return redirect("anggota_kelompok_5", email, nama_lengkap, nomor_telefon, program_studi, angkatan,
                            universitas, info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah,
                            materi, simulasi, lampiran, jumlah_peserta, email_1, nama_lengkap_1, nomor_telefon_1,
                            akun_discord_1,
                            email_2, nama_lengkap_2, nomor_telefon_2,
                            akun_discord_2, email_3, nama_lengkap_3, nomor_telefon_3, akun_discord_3, email_4,
                            nama_lengkap_4, nomor_telefon_4, akun_discord_4)
    return render(request, "FormRegistrationApp/anggota_kelompok_4.html")


# ---------------------------------------------------------------------------------------------------------
def anggota_kelompok_5(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche,
                       metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi, lampiran,
                       jumlah_peserta, email_1, nama_lengkap_1, nomor_telefon_1, akun_discord_1,
                       email_2, nama_lengkap_2, nomor_telefon_2, akun_discord_2, email_3,
                       nama_lengkap_3, nomor_telefon_3, akun_discord_3, email_4, nama_lengkap_4, nomor_telefon_4,
                       akun_discord_4):
    if request.method == 'POST':
        email_5 = request.POST.get('email_5')
        nama_lengkap_5 = request.POST.get('nama_lengkap_5')
        nomor_telefon_5 = request.POST.get('nomor_telefon_5')
        akun_discord_5 = request.POST.get('akun_discord_5')
        email_6 = "-"
        nama_lengkap_6 = "-"
        nomor_telefon_6 = "-"
        akun_discord_6 = "-"
        email_7 = "-"
        nama_lengkap_7 = "-"
        nomor_telefon_7 = "-"
        akun_discord_7 = "-"
        email_8 = "-"
        nama_lengkap_8 = "-"
        nomor_telefon_8 = "-"
        akun_discord_8 = "-"
        email_9 = "-"
        nama_lengkap_9 = "-"
        nomor_telefon_9 = "-"
        akun_discord_9 = "-"
        email_10 = "-"
        nama_lengkap_10 = "-"
        nomor_telefon_10 = "-"
        akun_discord_10 = "-"
        if jumlah_peserta == "5":
            return redirect("jadwal_belajar", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi,
                            lampiran, jumlah_peserta, email_1, nama_lengkap_1, nomor_telefon_1, akun_discord_1,
                            email_2, nama_lengkap_2, nomor_telefon_2, akun_discord_2, email_3,
                            nama_lengkap_3, nomor_telefon_3, akun_discord_3, email_4, nama_lengkap_4, nomor_telefon_4,
                            akun_discord_4, email_5, nama_lengkap_5, nomor_telefon_5, akun_discord_5,
                            email_6, nama_lengkap_6, nomor_telefon_6, akun_discord_6,
                            email_7, nama_lengkap_7, nomor_telefon_7, akun_discord_7,
                            email_8, nama_lengkap_8, nomor_telefon_8, akun_discord_8,
                            email_9, nama_lengkap_9, nomor_telefon_9, akun_discord_9,
                            email_10, nama_lengkap_10, nomor_telefon_10, akun_discord_10
                            )
        else:
            return redirect("anggota_kelompok_6", email, nama_lengkap, nomor_telefon, program_studi, angkatan,
                            universitas, info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah,
                            materi, simulasi, lampiran, jumlah_peserta, email_1, nama_lengkap_1, nomor_telefon_1,
                            akun_discord_1,
                            email_2, nama_lengkap_2, nomor_telefon_2,
                            akun_discord_2, email_3, nama_lengkap_3, nomor_telefon_3, akun_discord_3, email_4,
                            nama_lengkap_4, nomor_telefon_4, akun_discord_4, email_5, nama_lengkap_5, nomor_telefon_5,
                            akun_discord_5)
    return render(request, "FormRegistrationApp/anggota_kelompok_5.html")


# ---------------------------------------------------------------------------------------------------------
def anggota_kelompok_6(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche,
                       metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi, lampiran,
                       jumlah_peserta, email_1, nama_lengkap_1, nomor_telefon_1, akun_discord_1,
                       email_2, nama_lengkap_2, nomor_telefon_2, akun_discord_2, email_3,
                       nama_lengkap_3, nomor_telefon_3, akun_discord_3, email_4, nama_lengkap_4, nomor_telefon_4,
                       akun_discord_4, email_5, nama_lengkap_5, nomor_telefon_5, akun_discord_5):
    if request.method == 'POST':
        email_6 = request.POST.get('email_6')
        nama_lengkap_6 = request.POST.get('nama_lengkap_6')
        nomor_telefon_6 = request.POST.get('nomor_telefon_6')
        akun_discord_6 = request.POST.get('akun_discord_6')
        email_7 = "-"
        nama_lengkap_7 = "-"
        nomor_telefon_7 = "-"
        akun_discord_7 = "-"
        email_8 = "-"
        nama_lengkap_8 = "-"
        nomor_telefon_8 = "-"
        akun_discord_8 = "-"
        email_9 = "-"
        nama_lengkap_9 = "-"
        nomor_telefon_9 = "-"
        akun_discord_9 = "-"
        email_10 = "-"
        nama_lengkap_10 = "-"
        nomor_telefon_10 = "-"
        akun_discord_10 = "-"
        if jumlah_peserta == "6":
            return redirect("jadwal_belajar", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi,
                            lampiran, jumlah_peserta, email_1, nama_lengkap_1, nomor_telefon_1, akun_discord_1,
                            email_2, nama_lengkap_2, nomor_telefon_2, akun_discord_2, email_3,
                            nama_lengkap_3, nomor_telefon_3, akun_discord_3, email_4, nama_lengkap_4, nomor_telefon_4,
                            akun_discord_4, email_5, nama_lengkap_5, nomor_telefon_5, akun_discord_5, email_6,
                            nama_lengkap_6, nomor_telefon_6, akun_discord_6,
                            email_7, nama_lengkap_7, nomor_telefon_7, akun_discord_7,
                            email_8, nama_lengkap_8, nomor_telefon_8, akun_discord_8,
                            email_9, nama_lengkap_9, nomor_telefon_9, akun_discord_9,
                            email_10, nama_lengkap_10, nomor_telefon_10, akun_discord_10)
        else:
            return redirect("anggota_kelompok_7", email, nama_lengkap, nomor_telefon, program_studi, angkatan,
                            universitas, info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah,
                            materi, simulasi, lampiran, jumlah_peserta, email_1, nama_lengkap_1, nomor_telefon_1,
                            akun_discord_1,
                            email_2, nama_lengkap_2, nomor_telefon_2,
                            akun_discord_2, email_3, nama_lengkap_3, nomor_telefon_3, akun_discord_3, email_4,
                            nama_lengkap_4, nomor_telefon_4, akun_discord_4, email_5, nama_lengkap_5, nomor_telefon_5,
                            akun_discord_5, email_6, nama_lengkap_6, nomor_telefon_6, akun_discord_6)
    return render(request, "FormRegistrationApp/anggota_kelompok_6.html")


# ---------------------------------------------------------------------------------------------------------
def anggota_kelompok_7(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche,
                       metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi, lampiran,
                       jumlah_peserta, email_1, nama_lengkap_1, nomor_telefon_1, akun_discord_1,
                       email_2, nama_lengkap_2, nomor_telefon_2, akun_discord_2, email_3,
                       nama_lengkap_3, nomor_telefon_3, akun_discord_3, email_4, nama_lengkap_4, nomor_telefon_4,
                       akun_discord_4, email_5, nama_lengkap_5, nomor_telefon_5, akun_discord_5, email_6,
                       nama_lengkap_6, nomor_telefon_6, akun_discord_6):
    if request.method == 'POST':
        email_7 = request.POST.get('email_7')
        nama_lengkap_7 = request.POST.get('nama_lengkap_7')
        nomor_telefon_7 = request.POST.get('nomor_telefon_7')
        akun_discord_7 = request.POST.get('akun_discord_7')
        email_8 = "-"
        nama_lengkap_8 = "-"
        nomor_telefon_8 = "-"
        akun_discord_8 = "-"
        email_9 = "-"
        nama_lengkap_9 = "-"
        nomor_telefon_9 = "-"
        akun_discord_9 = "-"
        email_10 = "-"
        nama_lengkap_10 = "-"
        nomor_telefon_10 = "-"
        akun_discord_10 = "-"
        if jumlah_peserta == "7":
            return redirect("jadwal_belajar", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi,
                            lampiran, jumlah_peserta, email_1, nama_lengkap_1, nomor_telefon_1, akun_discord_1,
                            email_2, nama_lengkap_2, nomor_telefon_2, akun_discord_2, email_3,
                            nama_lengkap_3, nomor_telefon_3, akun_discord_3, email_4, nama_lengkap_4, nomor_telefon_4,
                            akun_discord_4, email_5, nama_lengkap_5, nomor_telefon_5, akun_discord_5, email_6,
                            nama_lengkap_6, nomor_telefon_6, akun_discord_6, email_7, nama_lengkap_7, nomor_telefon_7,
                            akun_discord_7,
                            email_8, nama_lengkap_8, nomor_telefon_8, akun_discord_8,
                            email_9, nama_lengkap_9, nomor_telefon_9, akun_discord_9,
                            email_10, nama_lengkap_10, nomor_telefon_10, akun_discord_10
                            )
        else:
            return redirect("anggota_kelompok_8", email, nama_lengkap, nomor_telefon, program_studi, angkatan,
                            universitas, info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah,
                            materi, simulasi, lampiran, jumlah_peserta, email_1, nama_lengkap_1, nomor_telefon_1,
                            akun_discord_1,
                            email_2, nama_lengkap_2, nomor_telefon_2,
                            akun_discord_2, email_3, nama_lengkap_3, nomor_telefon_3, akun_discord_3, email_4,
                            nama_lengkap_4, nomor_telefon_4, akun_discord_4, email_5, nama_lengkap_5, nomor_telefon_5,
                            akun_discord_5, email_6, nama_lengkap_6, nomor_telefon_6, akun_discord_6, email_7,
                            nama_lengkap_7, nomor_telefon_7, akun_discord_7)
    return render(request, "FormRegistrationApp/anggota_kelompok_7.html")


# ---------------------------------------------------------------------------------------------------------
def anggota_kelompok_8(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche,
                       metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi, lampiran,
                       jumlah_peserta, email_1, nama_lengkap_1, nomor_telefon_1, akun_discord_1,
                       email_2, nama_lengkap_2, nomor_telefon_2, akun_discord_2, email_3,
                       nama_lengkap_3, nomor_telefon_3, akun_discord_3, email_4, nama_lengkap_4, nomor_telefon_4,
                       akun_discord_4, email_5, nama_lengkap_5, nomor_telefon_5, akun_discord_5, email_6,
                       nama_lengkap_6, nomor_telefon_6, akun_discord_6, email_7, nama_lengkap_7, nomor_telefon_7,
                       akun_discord_7):
    if request.method == 'POST':
        email_8 = request.POST.get('email_8')
        nama_lengkap_8 = request.POST.get('nama_lengkap_8')
        nomor_telefon_8 = request.POST.get('nomor_telefon_8')
        akun_discord_8 = request.POST.get('akun_discord_8')
        email_9 = "-"
        nama_lengkap_9 = "-"
        nomor_telefon_9 = "-"
        akun_discord_9 = "-"
        email_10 = "-"
        nama_lengkap_10 = "-"
        nomor_telefon_10 = "-"
        akun_discord_10 = "-"
        if jumlah_peserta == "8":
            return redirect("jadwal_belajar", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi,
                            lampiran, jumlah_peserta, email_1, nama_lengkap_1, nomor_telefon_1, akun_discord_1,
                            email_2, nama_lengkap_2, nomor_telefon_2, akun_discord_2, email_3,
                            nama_lengkap_3, nomor_telefon_3, akun_discord_3, email_4, nama_lengkap_4, nomor_telefon_4,
                            akun_discord_4, email_5, nama_lengkap_5, nomor_telefon_5, akun_discord_5, email_6,
                            nama_lengkap_6, nomor_telefon_6, akun_discord_6, email_7, nama_lengkap_7, nomor_telefon_7,
                            akun_discord_7, email_8, nama_lengkap_8, nomor_telefon_8, akun_discord_8,
                            email_9, nama_lengkap_9, nomor_telefon_9, akun_discord_9,
                            email_10, nama_lengkap_10, nomor_telefon_10, akun_discord_10
                            )
        else:
            return redirect("anggota_kelompok_9", email, nama_lengkap, nomor_telefon, program_studi, angkatan,
                            universitas, info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah,
                            materi, simulasi, lampiran, jumlah_peserta, email_1, nama_lengkap_1, nomor_telefon_1,
                            akun_discord_1,
                            email_2, nama_lengkap_2, nomor_telefon_2,
                            akun_discord_2, email_3, nama_lengkap_3, nomor_telefon_3, akun_discord_3, email_4,
                            nama_lengkap_4, nomor_telefon_4, akun_discord_4, email_5, nama_lengkap_5, nomor_telefon_5,
                            akun_discord_5, email_6, nama_lengkap_6, nomor_telefon_6, akun_discord_6, email_7,
                            nama_lengkap_7, nomor_telefon_7, akun_discord_7, email_8, nama_lengkap_8, nomor_telefon_8,
                            akun_discord_8)
    return render(request, "FormRegistrationApp/anggota_kelompok_8.html")


# ---------------------------------------------------------------------------------------------------------
def anggota_kelompok_9(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche,
                       metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi, lampiran,
                       jumlah_peserta, email_1, nama_lengkap_1, nomor_telefon_1, akun_discord_1,
                       email_2, nama_lengkap_2, nomor_telefon_2, akun_discord_2, email_3,
                       nama_lengkap_3, nomor_telefon_3, akun_discord_3, email_4, nama_lengkap_4, nomor_telefon_4,
                       akun_discord_4, email_5, nama_lengkap_5, nomor_telefon_5, akun_discord_5, email_6,
                       nama_lengkap_6, nomor_telefon_6, akun_discord_6, email_7, nama_lengkap_7, nomor_telefon_7,
                       akun_discord_7, email_8, nama_lengkap_8, nomor_telefon_8, akun_discord_8):
    if request.method == 'POST':
        email_9 = request.POST.get('email_9')
        nama_lengkap_9 = request.POST.get('nama_lengkap_9')
        nomor_telefon_9 = request.POST.get('nomor_telefon_9')
        akun_discord_9 = request.POST.get('akun_discord_9')
        email_10 = "-"
        nama_lengkap_10 = "-"
        nomor_telefon_10 = "-"
        akun_discord_10 = "-"
        if jumlah_peserta == "9":
            return redirect("jadwal_belajar", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi,
                            lampiran, jumlah_peserta, email_1, nama_lengkap_1, nomor_telefon_1, akun_discord_1,
                            email_2, nama_lengkap_2, nomor_telefon_2, akun_discord_2, email_3,
                            nama_lengkap_3, nomor_telefon_3, akun_discord_3, email_4, nama_lengkap_4, nomor_telefon_4,
                            akun_discord_4, email_5, nama_lengkap_5, nomor_telefon_5, akun_discord_5, email_6,
                            nama_lengkap_6, nomor_telefon_6, akun_discord_6, email_7, nama_lengkap_7, nomor_telefon_7,
                            akun_discord_7, email_8, nama_lengkap_8, nomor_telefon_8, akun_discord_8, email_9,
                            nama_lengkap_9, nomor_telefon_9, akun_discord_9,
                            email_10, nama_lengkap_10, nomor_telefon_10, akun_discord_10
                            )
        else:
            return redirect("anggota_kelompok_10", email, nama_lengkap, nomor_telefon, program_studi, angkatan,
                            universitas, info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah,
                            materi, simulasi, lampiran, jumlah_peserta, email_1, nama_lengkap_1, nomor_telefon_1,
                            akun_discord_1,
                            email_2, nama_lengkap_2, nomor_telefon_2,
                            akun_discord_2, email_3, nama_lengkap_3, nomor_telefon_3, akun_discord_3, email_4,
                            nama_lengkap_4, nomor_telefon_4, akun_discord_4, email_5, nama_lengkap_5, nomor_telefon_5,
                            akun_discord_5, email_6, nama_lengkap_6, nomor_telefon_6, akun_discord_6, email_7,
                            nama_lengkap_7, nomor_telefon_7, akun_discord_7, email_8, nama_lengkap_8, nomor_telefon_8,
                            akun_discord_8, email_9, nama_lengkap_9, nomor_telefon_9, akun_discord_9)
    return render(request, "FormRegistrationApp/anggota_kelompok_9.html")


# ---------------------------------------------------------------------------------------------------------
def anggota_kelompok_10(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas, info_torche,
                        metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi, lampiran,
                        jumlah_peserta, email_1, nama_lengkap_1, nomor_telefon_1, akun_discord_1,
                        email_2, nama_lengkap_2, nomor_telefon_2, akun_discord_2, email_3,
                        nama_lengkap_3, nomor_telefon_3, akun_discord_3, email_4, nama_lengkap_4, nomor_telefon_4,
                        akun_discord_4, email_5, nama_lengkap_5, nomor_telefon_5, akun_discord_5, email_6,
                        nama_lengkap_6, nomor_telefon_6, akun_discord_6, email_7, nama_lengkap_7, nomor_telefon_7,
                        akun_discord_7, email_8, nama_lengkap_8, nomor_telefon_8, akun_discord_8, email_9,
                        nama_lengkap_9, nomor_telefon_9, akun_discord_9):
    if request.method == 'POST':
        email_10 = request.POST.get('email_10')
        nama_lengkap_10 = request.POST.get('nama_lengkap_10')
        nomor_telefon_10 = request.POST.get('nomor_telefon_10')
        akun_discord_10 = request.POST.get('akun_discord_10')
        if jumlah_peserta == "10":
            return redirect("jadwal_belajar", email, nama_lengkap, nomor_telefon, program_studi, angkatan, universitas,
                            info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti, mata_kuliah, materi, simulasi,
                            lampiran, jumlah_peserta, email_1, nama_lengkap_1, nomor_telefon_1, akun_discord_1,
                            email_2, nama_lengkap_2, nomor_telefon_2, akun_discord_2, email_3,
                            nama_lengkap_3, nomor_telefon_3, akun_discord_3, email_4, nama_lengkap_4, nomor_telefon_4,
                            akun_discord_4, email_5, nama_lengkap_5, nomor_telefon_5, akun_discord_5, email_6,
                            nama_lengkap_6, nomor_telefon_6, akun_discord_6, email_7, nama_lengkap_7, nomor_telefon_7,
                            akun_discord_7, email_8, nama_lengkap_8, nomor_telefon_8, akun_discord_8, email_9,
                            nama_lengkap_9, nomor_telefon_9, akun_discord_9, email_10, nama_lengkap_10,
                            nomor_telefon_10,
                            akun_discord_10)
    return render(request, "FormRegistrationApp/anggota_kelompok_10.html")


# ---------------------------------------------------------------------------------------------------------
def jadwal_belajar(request, email, nama_lengkap, nomor_telefon, program_studi, angkatan,
                   universitas, info_torche, metode_pembelajaran, jumlah_sesi_yang_diikuti,
                   mata_kuliah, materi, simulasi, lampiran, jumlah_peserta,
                   email_1, nama_lengkap_1, nomor_telefon_1, akun_discord_1,
                   email_2, nama_lengkap_2, nomor_telefon_2, akun_discord_2,
                   email_3, nama_lengkap_3, nomor_telefon_3, akun_discord_3,
                   email_4, nama_lengkap_4, nomor_telefon_4, akun_discord_4,
                   email_5, nama_lengkap_5, nomor_telefon_5, akun_discord_5,
                   email_6, nama_lengkap_6, nomor_telefon_6, akun_discord_6,
                   email_7, nama_lengkap_7, nomor_telefon_7, akun_discord_7,
                   email_8, nama_lengkap_8, nomor_telefon_8, akun_discord_8,
                   email_9, nama_lengkap_9, nomor_telefon_9, akun_discord_9,
                   email_10, nama_lengkap_10, nomor_telefon_10, akun_discord_10):
    context = {'form': JadwalBelajarForm()}
    if request.method == 'POST':
        form = JadwalBelajarForm(request.POST, request.FILES)
        if form.is_valid():
            new_data = RegistrationData()

            # Save the Data
            new_data.nama_lengkap = nama_lengkap
            new_data.email = email
            new_data.angkatan = angkatan
            new_data.nomor_telefon = nomor_telefon
            new_data.program_studi = program_studi
            new_data.universitas = universitas
            new_data.metode_pembelajaran = metode_pembelajaran
            new_data.mata_kuliah = mata_kuliah
            new_data.jumlah_peserta = jumlah_peserta
            new_data.aplikasi_simulasi = simulasi
            new_data.jumlah_sesi_yang_diikuti = jumlah_sesi_yang_diikuti
            new_data.lampiran = lampiran

            global registration_number_q1
            global registration_number_q2
            global registration_number_q3
            global registration_number_q4

            global registration_number_q1_invoice
            global registration_number_q2_invoice
            global registration_number_q3_invoice
            global registration_number_q4_invoice

            month_number = datetime.datetime.now().month

            # Invoice Variable
            invoice = "Inv/"
            jumlah_peserta_invoice = ""
            metode_pembelajaran_invoice = ""
            mata_kuliah_invoice = ""
            quartal_invoice = ""

            # Invoice Jumlah Peserta Algorithm
            if jumlah_peserta <= "3":
                invoice += "P/"
                jumlah_peserta_invoice = "P"
            elif jumlah_peserta > "3":
                invoice += "G/"
                jumlah_peserta_invoice = "G"

            # Invoice Tipe Kelas Algorithm
            if metode_pembelajaran == "Consultation Class":
                invoice += "C/"
                metode_pembelajaran_invoice = "C"
            elif metode_pembelajaran == "Lecturing Class":
                invoice += "L/"
                metode_pembelajaran_invoice = "L"
            elif metode_pembelajaran == "Exam Preparation Class":
                invoice += "EP/"
                metode_pembelajaran_invoice = "EP"

            # Invoice Mata Kuliah Algorithm
            if mata_kuliah == NAMA_MATA_KULIAH[0][0]:
                invoice += "CCE/"
                mata_kuliah_invoice = "CCE"
            elif mata_kuliah == NAMA_MATA_KULIAH[1][0]:
                invoice += "CEM/"
                mata_kuliah_invoice = "CEM"
            elif mata_kuliah == NAMA_MATA_KULIAH[2][0]:
                invoice += "CTE/"
                mata_kuliah_invoice = "CTE"
            elif mata_kuliah == NAMA_MATA_KULIAH[3][0]:
                invoice += "CPS/"
                mata_kuliah_invoice = "CPS"
            elif mata_kuliah == NAMA_MATA_KULIAH[4][0]:
                invoice += "CRE/"
                mata_kuliah_invoice = "CRE"
            elif mata_kuliah == NAMA_MATA_KULIAH[5][0]:
                invoice += "EEC/"
                mata_kuliah_invoice = "EEC"
            elif mata_kuliah == NAMA_MATA_KULIAH[6][0]:
                invoice += "FAC/"
                mata_kuliah_invoice = "FAC"
            elif mata_kuliah == NAMA_MATA_KULIAH[7][0]:
                invoice += "FCA/"
                mata_kuliah_invoice = "FCA"
            elif mata_kuliah == NAMA_MATA_KULIAH[8][0]:
                invoice += "FCH/"
                mata_kuliah_invoice = "FCH"
            elif mata_kuliah == NAMA_MATA_KULIAH[9][0]:
                invoice += "FHT/"
                mata_kuliah_invoice = "FHT"
            elif mata_kuliah == NAMA_MATA_KULIAH[10][0]:
                invoice += "FMT/"
                mata_kuliah_invoice = "FMT"
            elif mata_kuliah == NAMA_MATA_KULIAH[11][0]:
                invoice += "FPM/"
                mata_kuliah_invoice = "FPM"
            elif mata_kuliah == NAMA_MATA_KULIAH[12][0]:
                invoice += "FP1/"
                mata_kuliah_invoice = "FP1"
            elif mata_kuliah == NAMA_MATA_KULIAH[13][0]:
                invoice += "FP2/"
                mata_kuliah_invoice = "FP2"
            elif mata_kuliah == NAMA_MATA_KULIAH[14][0]:
                invoice += "MEB/"
                mata_kuliah_invoice = "MEB"
            elif mata_kuliah == NAMA_MATA_KULIAH[15][0]:
                invoice += "NCE/"
                mata_kuliah_invoice = "NCE"
            elif mata_kuliah == NAMA_MATA_KULIAH[16][0]:
                invoice += "OCE/"
                mata_kuliah_invoice = "OCE"
            elif mata_kuliah == NAMA_MATA_KULIAH[17][0]:
                invoice += "PCD/"
                mata_kuliah_invoice = "PCD"
            elif mata_kuliah == NAMA_MATA_KULIAH[18][0]:
                invoice += "PCH/"
                mata_kuliah_invoice = "PCH"
            elif mata_kuliah == NAMA_MATA_KULIAH[19][0]:
                invoice += "PDD/"
                mata_kuliah_invoice = "PDD"
            elif mata_kuliah == NAMA_MATA_KULIAH[20][0]:
                invoice += "PED/"
                mata_kuliah_invoice = "PED"
            elif mata_kuliah == NAMA_MATA_KULIAH[21][0]:
                invoice += "PPD/"
                mata_kuliah_invoice = "PPD"
            elif mata_kuliah == NAMA_MATA_KULIAH[22][0]:
                invoice += "SPR/"
                mata_kuliah_invoice = "SPR"
            elif mata_kuliah == NAMA_MATA_KULIAH[23][0]:
                invoice += "TPH/"
                mata_kuliah_invoice = "TPH"

            # Invoice Number Registration Algorithm
            if 1 <= month_number <= 3:
                registration_number_q1 += 1
                if registration_number_q1 <= 9:
                    invoice += "0" + str(registration_number_q1) + "/"
                    registration_number_q1_invoice = "0" + str(registration_number_q1)
                elif registration_number_q1 >= 10:
                    invoice += str(registration_number_q1) + "/"
                    registration_number_q1_invoice = str(registration_number_q1)
            elif 4 <= month_number <= 6:
                registration_number_q2 += 1
                if registration_number_q2 <= 9:
                    invoice += "0" + str(registration_number_q2) + "/"
                    registration_number_q2_invoice = "0" + str(registration_number_q2)
                elif registration_number_q2 >= 10:
                    invoice += str(registration_number_q2) + "/"
                    registration_number_q2_invoice = str(registration_number_q2)
            elif 7 <= month_number <= 9:
                registration_number_q3 += 1
                if registration_number_q3 <= 9:
                    invoice += "0" + str(registration_number_q3) + "/"
                    registration_number_q3_invoice = "0" + str(registration_number_q3)
                elif registration_number_q3 >= 10:
                    invoice += str(registration_number_q3) + "/"
                    registration_number_q3_invoice = str(registration_number_q3)
            elif 10 <= month_number <= 12:
                registration_number_q4 += 1
                if registration_number_q4 <= 9:
                    invoice += "0" + str(registration_number_q4) + "/"
                    registration_number_q4_invoice = "0" + str(registration_number_q4)
                elif registration_number_q1 >= 10:
                    invoice += str(registration_number_q4) + "/"
                    registration_number_q4_invoice = str(registration_number_q4)

            # Invoice Quartal Algorithm
            if 1 <= month_number <= 3:
                invoice += "1-"
                quartal_invoice = "1-"
            elif 4 <= month_number <= 6:
                invoice += "2-"
                quartal_invoice = "2-"
            elif 7 <= month_number <= 9:
                invoice += "3-"
                quartal_invoice = "3-"
            elif 10 <= month_number <= 12:
                invoice += "4-"
                quartal_invoice = "4-"

            year_number = datetime.datetime.now().year
            invoice += "{}".format(str(year_number)[-2:])
            quartal_invoice += "{}".format(str(year_number)[-2:])
            new_data.nomor_invoice = invoice

            new_data.sesi_hari = str(form.cleaned_data['sesi_hari']).replace("[", "").replace("]", "").replace("'", "")
            new_data.sesi_jam = str(form.cleaned_data['sesi_jam']).replace("[", "").replace("]", "").replace("'", "")

            if form.cleaned_data['notes_for_tutor'] == "":
                new_data.notes_for_tutor = "-"
            else:
                new_data.notes_for_tutor = form.cleaned_data['notes_for_tutor']

            biaya = 0
            if int(jumlah_peserta) <= 3:
                biaya += (175000 * len(materi.split(",")))
            elif int(jumlah_peserta) == 4:
                biaya += (200000 * len(materi.split(",")))
            elif int(jumlah_peserta) == 5:
                biaya += (250000 * len(materi.split(",")))
            elif int(jumlah_peserta) >= 6:
                biaya += ((250000 + ((int(jumlah_peserta) - 5) * 40000)) * len(materi.split(",")))
            new_data.biaya = "{:0,.0f}".format(biaya)

            bulan = ""
            if datetime.datetime.now().month == 1:
                bulan = "Januari"
            elif datetime.datetime.now().month == 2:
                bulan = "Februari"
            elif datetime.datetime.now().month == 3:
                bulan = "Maret"
            elif datetime.datetime.now().month == 4:
                bulan = "April"
            elif datetime.datetime.now().month == 5:
                bulan = "Mei"
            elif datetime.datetime.now().month == 6:
                bulan = "Juni"
            elif datetime.datetime.now().month == 7:
                bulan = "Juli"
            elif datetime.datetime.now().month == 8:
                bulan = "Agustus"
            elif datetime.datetime.now().month == 9:
                bulan = "September"
            elif datetime.datetime.now().month == 10:
                bulan = "Oktober"
            elif datetime.datetime.now().month == 11:
                bulan = "November"
            elif datetime.datetime.now().month == 12:
                bulan = "Desember"
            new_data.tanggal = str(datetime.datetime.now().day) + " " + bulan + " " + str(datetime.datetime.now().year)

            new_data.materi = str(materi).replace("[", "").replace("]", "").replace("'", "")

            new_data.informasi_mengenai_torche = str(info_torche).replace("[", "").replace("]", "").replace("'", "")

            if email_1 == "-" and email_2 == "-" and email_3 == "-" and email_4 == "-" and email_5 == "-" and email_6 == "-" and email_7 == "-" and email_8 == "-" and email_9 == "-" and email_10 == "-":
                new_data.alamat_email_anggota_kelompok = "-"
            else:
                new_data.alamat_email_anggota_kelompok = (
                        email_1 + ", " + email_2 + ", " + email_3 + ", " + email_4 + ", " + email_5 + ", " + email_6 + ", " + email_7 + ", " + email_8 + ", " + email_9 + ", " + email_10).replace(
                    ", -", "")

            if nama_lengkap_1 == "-" and nama_lengkap_2 == "-" and nama_lengkap_3 == "-" and nama_lengkap_4 == "-" and nama_lengkap_5 == "-" and nama_lengkap_6 == "-" and nama_lengkap_7 == "-" and nama_lengkap_8 == "-" and nama_lengkap_9 == "-" and nama_lengkap_10 == "-":
                new_data.nama_lengkap_anggota_kelompok = "-"
            else:
                new_data.nama_lengkap_anggota_kelompok = (
                        nama_lengkap_1 + ", " + nama_lengkap_2 + ", " + nama_lengkap_3 + ", " + nama_lengkap_4 + ", " + nama_lengkap_5 + ", " + nama_lengkap_6 + ", " + nama_lengkap_7 + ", " + nama_lengkap_8 + ", " + nama_lengkap_9 + ", " + nama_lengkap_10).replace(
                    ", -", "")

            if nomor_telefon_1 == "-" and nomor_telefon_2 == "-" and nomor_telefon_3 == "-" and nomor_telefon_4 == "-" and nomor_telefon_5 == "-" and nomor_telefon_6 == "-" and nomor_telefon_7 == "-" and nomor_telefon_8 == "-" and nomor_telefon_9 == "-" and nomor_telefon_10 == "-":
                new_data.nomor_telefon_anggota_kelompok = "-"
            else:
                new_data.nomor_telefon_anggota_kelompok = (
                        nomor_telefon_1 + ", " + nomor_telefon_2 + ", " + nomor_telefon_3 + ", " + nomor_telefon_4 + ", " + nomor_telefon_5 + ", " + nomor_telefon_6 + ", " + nomor_telefon_7 + ", " + nomor_telefon_8 + ", " + nomor_telefon_9 + ", " + nomor_telefon_10).replace(
                    ", -", "")

            if akun_discord_1 == "-" and akun_discord_2 == "-" and akun_discord_3 == "-" and akun_discord_4 == "-" and akun_discord_5 == "-" and akun_discord_6 == "-" and akun_discord_7 == "-" and akun_discord_8 == "-" and akun_discord_9 == "-" and akun_discord_10 == "-":
                new_data.akun_discord_anggota_kelompok = "-"
            else:
                new_data.akun_discord_anggota_kelompok = (
                        akun_discord_1 + ", " + akun_discord_2 + ", " + akun_discord_3 + ", " + akun_discord_4 + ", " + akun_discord_5 + ", " + akun_discord_6 + ", " + akun_discord_7 + ", " + akun_discord_8 + ", " + akun_discord_9 + ", " + akun_discord_10).replace(
                    ", -", "")

            referral_code = form.cleaned_data['referral_code']
            data_referral_code = ReferralCode.objects.all()
            data_referral_code_list = []
            for i in data_referral_code:
                data_referral_code_list.append(i.referral_code)
            if referral_code in data_referral_code_list:
                new_data.referral_code = form.cleaned_data['referral_code']
            else:
                new_data.referral_code = "-"

            try:
                new_data.save()

                if 1 <= month_number <= 3:
                    return redirect("send_email_q1", nama_lengkap, email, nomor_telefon, program_studi, universitas,
                                    metode_pembelajaran, mata_kuliah, materi, jumlah_peserta_invoice,
                                    metode_pembelajaran_invoice, mata_kuliah_invoice, registration_number_q1_invoice,
                                    quartal_invoice)
                elif 4 <= month_number <= 6:
                    return redirect("send_email_q2", nama_lengkap, email, nomor_telefon, program_studi, universitas,
                                    metode_pembelajaran, mata_kuliah, materi, jumlah_peserta_invoice,
                                    metode_pembelajaran_invoice, mata_kuliah_invoice, registration_number_q2_invoice,
                                    quartal_invoice)
                elif 7 <= month_number <= 9:
                    return redirect("send_email_q3", nama_lengkap, email, nomor_telefon, program_studi, universitas,
                                    metode_pembelajaran, mata_kuliah, materi, jumlah_peserta_invoice,
                                    metode_pembelajaran_invoice, mata_kuliah_invoice, registration_number_q3_invoice,
                                    quartal_invoice)
                elif 10 <= month_number <= 12:
                    return redirect("send_email_q4", nama_lengkap, email, nomor_telefon, program_studi, universitas,
                                    metode_pembelajaran, mata_kuliah, materi, jumlah_peserta_invoice,
                                    metode_pembelajaran_invoice, mata_kuliah_invoice, registration_number_q4_invoice,
                                    quartal_invoice)
            except:
                return redirect("pendaftaran_gagal")
    else:
        form = JadwalBelajarForm(request.POST)
    return render(request, "FormRegistrationApp/jadwal_belajar.html", context)


def get_data(request):
    data = RegistrationData.objects.all()
    context = {
        'my_data': data,
    }
    return render(request, 'FormRegistrationApp/get_data.html', context)


def create_pdf_assignment(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def invoice_assignment_q1(request, jumlah_peserta_invoice, metode_pembelajaran_invoice, mata_kuliah_invoice,
                          registration_number_q1_invoice, quartal_invoice):
    data = RegistrationData.objects.get(
        nomor_invoice="Inv/{}/{}/{}/{}/{}".format(jumlah_peserta_invoice, metode_pembelajaran_invoice,
                                                  mata_kuliah_invoice, registration_number_q1_invoice, quartal_invoice))
    sesi_hari = data.sesi_hari.replace("[", "").replace("]", "").replace("'", "")
    sesi_jam = data.sesi_jam.replace("[", "").replace("]", "").replace("'", "")
    sesi_materi = data.materi.replace("[", "").replace("]", "").replace("'", "")
    context = {
        'i': data,
        'sesi_hari': sesi_hari,
        'sesi_jam': sesi_jam,
        'sesi_materi': sesi_materi
    }
    pdf = create_pdf_assignment('FormRegistrationApp/template_pdf_assignment.html', context)
    return HttpResponse(pdf, content_type='application/pdf')


def invoice_assignment_q2(request, jumlah_peserta_invoice, metode_pembelajaran_invoice, mata_kuliah_invoice,
                          registration_number_q2_invoice, quartal_invoice):
    data = RegistrationData.objects.get(
        nomor_invoice="Inv/{}/{}/{}/{}/{}".format(jumlah_peserta_invoice, metode_pembelajaran_invoice,
                                                  mata_kuliah_invoice, registration_number_q2_invoice, quartal_invoice))
    sesi_hari = data.sesi_hari.replace("[", "").replace("]", "").replace("'", "")
    sesi_jam = data.sesi_jam.replace("[", "").replace("]", "").replace("'", "")
    sesi_materi = data.materi.replace("[", "").replace("]", "").replace("'", "")
    context = {
        'i': data,
        'sesi_hari': sesi_hari,
        'sesi_jam': sesi_jam,
        'sesi_materi': sesi_materi
    }
    pdf = create_pdf_assignment('FormRegistrationApp/template_pdf_assignment.html', context)
    return HttpResponse(pdf, content_type='application/pdf')


def invoice_assignment_q3(request, jumlah_peserta_invoice, metode_pembelajaran_invoice, mata_kuliah_invoice,
                          registration_number_q3_invoice, quartal_invoice):
    data = RegistrationData.objects.get(
        nomor_invoice="Inv/{}/{}/{}/{}/{}".format(jumlah_peserta_invoice, metode_pembelajaran_invoice,
                                                  mata_kuliah_invoice, registration_number_q3_invoice, quartal_invoice))
    sesi_hari = data.sesi_hari.replace("[", "").replace("]", "").replace("'", "")
    sesi_jam = data.sesi_jam.replace("[", "").replace("]", "").replace("'", "")
    sesi_materi = data.materi.replace("[", "").replace("]", "").replace("'", "")
    context = {
        'i': data,
        'sesi_hari': sesi_hari,
        'sesi_jam': sesi_jam,
        'sesi_materi': sesi_materi
    }
    pdf = create_pdf_assignment('FormRegistrationApp/template_pdf_assignment.html', context)
    return HttpResponse(pdf, content_type='application/pdf')


def invoice_assignment_q4(request, jumlah_peserta_invoice, metode_pembelajaran_invoice, mata_kuliah_invoice,
                          registration_number_q4_invoice, quartal_invoice):
    data = RegistrationData.objects.get(
        nomor_invoice="Inv/{}/{}/{}/{}/{}".format(jumlah_peserta_invoice, metode_pembelajaran_invoice,
                                                  mata_kuliah_invoice, registration_number_q4_invoice, quartal_invoice))
    sesi_hari = data.sesi_hari.replace("[", "").replace("]", "").replace("'", "")
    sesi_jam = data.sesi_jam.replace("[", "").replace("]", "").replace("'", "")
    sesi_materi = data.materi.replace("[", "").replace("]", "").replace("'", "")
    context = {
        'i': data,
        'sesi_hari': sesi_hari,
        'sesi_jam': sesi_jam,
        'sesi_materi': sesi_materi
    }
    pdf = create_pdf_assignment('FormRegistrationApp/template_pdf_assignment.html', context)
    return HttpResponse(pdf, content_type='application/pdf')


def create_pdf(context):
    html = render_to_string('FormRegistrationApp/template_pdf.html', context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return result.getvalue()
    return None


def send_email_q1(request, nama_lengkap, email, nomor_telefon, program_studi, universitas, metode_pembelajaran,
                  mata_kuliah, materi, jumlah_peserta_invoice, metode_pembelajaran_invoice, mata_kuliah_invoice,
                  registration_number_q1_invoice, quartal_invoice):
    data = RegistrationData.objects.get(
        nomor_invoice="Inv/{}/{}/{}/{}/{}".format(jumlah_peserta_invoice, metode_pembelajaran_invoice,
                                                  mata_kuliah_invoice, registration_number_q1_invoice, quartal_invoice))
    sesi_hari = data.sesi_hari.replace("[", "").replace("]", "").replace("'", "")
    sesi_jam = data.sesi_jam.replace("[", "").replace("]", "").replace("'", "")
    sesi_materi = data.materi.replace("[", "").replace("]", "").replace("'", "")
    context = {
        'i': data,
        'sesi_hari': sesi_hari,
        'sesi_jam': sesi_jam,
        'sesi_materi': sesi_materi
    }
    subject = "Torche Class Registration Form - Inv/{}/{}/{}/{}/{}".format(jumlah_peserta_invoice,
                                                                           metode_pembelajaran_invoice,
                                                                           mata_kuliah_invoice,
                                                                           registration_number_q1_invoice,
                                                                           quartal_invoice)
    message = "Terimakasih {}, anda telah memilih kelas {} dengan materi {}, untuk invoice dapat dilihat pada file berikut".format(
        nama_lengkap, mata_kuliah, sesi_materi)
    emails = [email]
    pdf = create_pdf(context)
    mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, emails)
    mail.attach(
        "Inv/{}/{}/{}/{}/{}.pdf".format(jumlah_peserta_invoice, metode_pembelajaran_invoice, mata_kuliah_invoice,
                                        registration_number_q1_invoice, quartal_invoice), pdf, 'application/pdf')
    mail.send(fail_silently=False)
    return redirect("pendaftaran_berhasil")


def send_email_q2(request, nama_lengkap, email, nomor_telefon, program_studi, universitas, metode_pembelajaran,
                  mata_kuliah, materi, jumlah_peserta_invoice, metode_pembelajaran_invoice, mata_kuliah_invoice,
                  registration_number_q2_invoice, quartal_invoice):
    data = RegistrationData.objects.get(
        nomor_invoice="Inv/{}/{}/{}/{}/{}".format(jumlah_peserta_invoice, metode_pembelajaran_invoice,
                                                  mata_kuliah_invoice, registration_number_q2_invoice, quartal_invoice))
    sesi_hari = data.sesi_hari.replace("[", "").replace("]", "").replace("'", "")
    sesi_jam = data.sesi_jam.replace("[", "").replace("]", "").replace("'", "")
    sesi_materi = data.materi.replace("[", "").replace("]", "").replace("'", "")
    context = {
        'i': data,
        'sesi_hari': sesi_hari,
        'sesi_jam': sesi_jam,
        'sesi_materi': sesi_materi
    }
    subject = "Torche Class Registration Form - Inv/{}/{}/{}/{}/{}".format(jumlah_peserta_invoice,
                                                                           metode_pembelajaran_invoice,
                                                                           mata_kuliah_invoice,
                                                                           registration_number_q2_invoice,
                                                                           quartal_invoice)
    message = "Terimakasih {}, anda telah memilih kelas {} dengan materi {}, untuk invoice dapat dilihat pada file berikut".format(
        nama_lengkap, mata_kuliah, sesi_materi)
    emails = [email]
    pdf = create_pdf(context)
    mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, emails)
    mail.attach(
        "Inv/{}/{}/{}/{}/{}.pdf".format(jumlah_peserta_invoice, metode_pembelajaran_invoice, mata_kuliah_invoice,
                                        registration_number_q1_invoice, quartal_invoice), pdf, 'application/pdf')
    mail.send(fail_silently=False)
    return redirect("pendaftaran_berhasil")


def send_email_q3(request, nama_lengkap, email, nomor_telefon, program_studi, universitas, metode_pembelajaran,
                  mata_kuliah, materi, jumlah_peserta_invoice, metode_pembelajaran_invoice, mata_kuliah_invoice,
                  registration_number_q3_invoice, quartal_invoice):
    data = RegistrationData.objects.get(
        nomor_invoice="Inv/{}/{}/{}/{}/{}".format(jumlah_peserta_invoice, metode_pembelajaran_invoice,
                                                  mata_kuliah_invoice, registration_number_q3_invoice, quartal_invoice))
    sesi_hari = data.sesi_hari.replace("[", "").replace("]", "").replace("'", "")
    sesi_jam = data.sesi_jam.replace("[", "").replace("]", "").replace("'", "")
    sesi_materi = data.materi.replace("[", "").replace("]", "").replace("'", "")
    context = {
        'i': data,
        'sesi_hari': sesi_hari,
        'sesi_jam': sesi_jam,
        'sesi_materi': sesi_materi
    }
    subject = "Torche Class Registration Form - Inv/{}/{}/{}/{}/{}".format(jumlah_peserta_invoice,
                                                                           metode_pembelajaran_invoice,
                                                                           mata_kuliah_invoice,
                                                                           registration_number_q3_invoice,
                                                                           quartal_invoice)
    message = "Terimakasih {}, anda telah memilih kelas {} dengan materi {}, untuk invoice dapat dilihat pada file berikut".format(
        nama_lengkap, mata_kuliah, sesi_materi)
    emails = [email]
    pdf = create_pdf(context)
    mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, emails)
    mail.attach(
        "Inv/{}/{}/{}/{}/{}.pdf".format(jumlah_peserta_invoice, metode_pembelajaran_invoice, mata_kuliah_invoice,
                                        registration_number_q3_invoice, quartal_invoice), pdf, 'application/pdf')
    mail.send(fail_silently=False)
    return redirect("pendaftaran_berhasil")


def send_email_q4(request, nama_lengkap, email, nomor_telefon, program_studi, universitas, metode_pembelajaran,
                  mata_kuliah, materi, jumlah_peserta_invoice, metode_pembelajaran_invoice, mata_kuliah_invoice,
                  registration_number_q4_invoice, quartal_invoice):
    data = RegistrationData.objects.get(
        nomor_invoice="Inv/{}/{}/{}/{}/{}".format(jumlah_peserta_invoice, metode_pembelajaran_invoice,
                                                  mata_kuliah_invoice, registration_number_q4_invoice, quartal_invoice))
    sesi_hari = data.sesi_hari.replace("[", "").replace("]", "").replace("'", "")
    sesi_jam = data.sesi_jam.replace("[", "").replace("]", "").replace("'", "")
    sesi_materi = data.materi.replace("[", "").replace("]", "").replace("'", "")
    context = {
        'i': data,
        'sesi_hari': sesi_hari,
        'sesi_jam': sesi_jam,
        'sesi_materi': sesi_materi
    }
    subject = "Torche Class Registration Form - Inv/{}/{}/{}/{}/{}".format(jumlah_peserta_invoice,
                                                                           metode_pembelajaran_invoice,
                                                                           mata_kuliah_invoice,
                                                                           registration_number_q4_invoice,
                                                                           quartal_invoice)
    message = "Terimakasih {}, anda telah memilih kelas {} dengan materi {}, untuk invoice dapat dilihat pada file berikut".format(
        nama_lengkap, mata_kuliah, sesi_materi)
    emails = [email]
    pdf = create_pdf(context)
    mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, emails)
    mail.attach(
        "Inv/{}/{}/{}/{}/{}.pdf".format(jumlah_peserta_invoice, metode_pembelajaran_invoice, mata_kuliah_invoice,
                                        registration_number_q1_invoice, quartal_invoice), pdf, 'application/pdf')
    mail.send(fail_silently=False)
    return redirect("pendaftaran_berhasil")


def pendaftaran_berhasil(request):
    return render(request, 'FormRegistrationApp/pendaftaran_berhasil.html')


def pendaftaran_gagal(request):
    return render(request, 'FormRegistrationApp/pendaftaran_gagal.html')
