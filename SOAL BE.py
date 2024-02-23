import requests
import uuid
from datetime import datetime
import json


# Fungsi untuk mengambil data uraian barang dari API
def get_uraian_barang(kode_barang):
    url = f"https://insw-dev.ilcs.co.id/my/n/barang?hs_code={kode_barang}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["uraian_barang"]
    else:
        return None

# Fungsi untuk mengambil tarif biaya impor dari API
def get_tarif_bm(kode_barang):
    url = f"https://insw-dev.ilcs.co.id/my/n/tarif?hs_code={kode_barang}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["bm"]
    else:
        return None

# Fungsi untuk menyimpan data ke database
def save_data_to_database(kode_barang, uraian_barang, bm, nilai_komoditas):
    id_simulasi = str(uuid.uuid4())
    nilai_bm = nilai_komoditas * bm / 100
    waktu_insert = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    connection = mysql.connector.connect(
        host="localhost",
        user="username",
        password="password",
        database="nama_database"
    )
    cursor = connection.cursor()

    sql = "INSERT INTO tabel_simulasi (id_simulasi, kode_barang, uraian_barang, bm, nilai_komoditas, nilai_bm, waktu_insert) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (id_simulasi, kode_barang, uraian_barang, bm, nilai_komoditas, nilai_bm, waktu_insert)
    cursor.execute(sql, val)

    connection.commit()
    print(cursor.rowcount, "Data berhasil disimpan")

    connection.close()

# Input kode barang dan nilai komoditas
kode_barang = input("Masukkan kode barang (8 Character): ")
nilai_komoditas = float(input("Masukkan nilai komoditas: "))

# Ambil uraian barang dari API
uraian_barang = get_uraian_barang(kode_barang)

if uraian_barang:
    # Ambil tarif bm dari API
    bm = get_tarif_bm(kode_barang)

    if bm is not None:
        # Simpan data ke database
        save_data_to_database(kode_barang, uraian_barang, bm, nilai_komoditas)
    else:
        print("Gagal mengambil tarif bm dari API")
else:
    print("Gagal mengambil uraian barang dari API")
