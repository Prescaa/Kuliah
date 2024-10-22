package praktikum2.soal3;

public class Soal3Main {
	public static void main(String[] args) { 
    Pegawai p1 = new Pegawai();
    
    //terjadi error karena tidak ada titik koma (;)
    //p1.nama = "Roi"
    p1.nama = "Roi";
    p1.asal = "Kingdom of Orvel";
    p1.setJabatan("Assasin"); 
    
    //inisiasi nilai "17" pada variabel "umur", karena sebelumnya tidak ditetapkan
    p1.umur = 17;
    
    System.out.println("Nama Pegawai: " + p1.getNama()); 
    System.out.println("Asal: " + p1.getAsal()); 
    System.out.println("Jabatan: " + p1.jabatan);
    
    //Menambah " tahun" pada bagian ("Umur: " + p1.umur), agar sesuai dengan output yang diminta
    //System.out.println("Umur: " + p1.umur); 
    System.out.println("Umur: " + p1.umur + " tahun"); 
    }
}
