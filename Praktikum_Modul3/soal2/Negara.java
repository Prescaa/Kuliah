package soal2;

import java.util.HashMap;

class Negara {
	private String nama;
	private String jenisKepemimpinan;
	private String namaPemimpin;
	private int tanggalKemerdekaan;
	private int bulanKemerdekaan;
	private int tahunKemerdekaan;
	
    Negara(String nama, String jenisKepemimpinan, String namaPemimpin) {
        this.nama = nama;
        this.jenisKepemimpinan = jenisKepemimpinan;
        this.namaPemimpin = namaPemimpin;
    }
	
	Negara(String nama, String jenisKepemimpinan, String namaPemimpin, int tanggalKemerdekaan, int bulanKemerdekaan, int tahunKemerdekaan){
		this.nama = nama;
		this.jenisKepemimpinan = jenisKepemimpinan;
		this.namaPemimpin = namaPemimpin;
		this.tanggalKemerdekaan = tanggalKemerdekaan;
		this.bulanKemerdekaan = bulanKemerdekaan;
		this.tahunKemerdekaan = tahunKemerdekaan;
	}
	
    private HashMap<Integer, String> namaBulan = new HashMap<Integer, String>();
    {
        namaBulan.put(1, "Januari");
        namaBulan.put(2, "Februari");
        namaBulan.put(3, "Maret");
        namaBulan.put(4, "April");
        namaBulan.put(5, "Mei");
        namaBulan.put(6, "Juni");
        namaBulan.put(7, "Juli");
        namaBulan.put(8, "Agustus");
        namaBulan.put(9, "September");
        namaBulan.put(10, "Oktober");
        namaBulan.put(11, "November");
        namaBulan.put(12, "Desember");
    }
	
	public String getNama() {
		return nama;
	}
	
	public String getJenisKepemimpinan() {
		return jenisKepemimpinan;
	}
	
	public String getNamaPemimpin() {
		return namaPemimpin;
	}
	
	public int getTanggalKemerdekaan() {
		return tanggalKemerdekaan;
	}
		
	public int getBulanKemerdekaan() {
		return bulanKemerdekaan;
	}
	
	
	public int getTahunKemerdekaan() {
		return tahunKemerdekaan;
	}
	
    public String getNamaBulan(int bulan) {
        return namaBulan.get(bulan);
    }
}

