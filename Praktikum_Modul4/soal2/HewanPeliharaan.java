package soal2;

public class HewanPeliharaan {
	String nama;
	private String ras;
	
	public HewanPeliharaan(String r, String n) {
		this.nama = n;
		this.ras = r;
	}
	
	public void display() {
		System.out.println("\nDetail Hewan Peliharaan:");
		System.out.println("Nama hewan peliharaanku adalah: " + nama);
		System.out.println("Dengan ras: " + ras);
	}
}
