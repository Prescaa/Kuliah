package soal1_praktikum6;

public class Mahasiswa {
	private String nim;
	private String nama;
	
	public Mahasiswa(String nim, String nama) {
		this.nim = nim;
		this.nama = nama;
	}
    
    public String getNIM() {
        return nim;
    }
    
    public void setNIM(String nim) {
        this.nim = nim;
    }
    
    public String getNama() {
        return nama;
    }
    
    public void setNama(String nama) {
        this.nama = nama;
    }
}
