package Soal1_Praktikum;

class classbuah {
	String nama;
	double berat;
	double harga;
	double jumlah;
	
	public void print() {
		 System.out.println("Nama Buah: " + nama);
	     System.out.println("Berat: " + berat + "kg");
	     System.out.println("Harga: " + harga);
	     System.out.println("Jumlah Beli: " + jumlah + "kg");
	     System.out.printf("Harga Sebelum Diskon: Rp %.2f", HargaSebelumDiskon());
	     System.out.printf("\nTotal Diskon: Rp %.2f", Diskon());
	     System.out.printf("\nHarga Setelah Diskon: Rp %.2f", HargaSetelahDiskon());
	     System.out.println(" ");
	}
	
    public double HargaSebelumDiskon() {
        return (jumlah / berat) * harga;
    }
    
    public double Diskon() {
        return Math.floor(jumlah / 4) * 0.02 * 4 * harga;
    }
    
    public double HargaSetelahDiskon() {
    return HargaSebelumDiskon() - Diskon();
    }
}
