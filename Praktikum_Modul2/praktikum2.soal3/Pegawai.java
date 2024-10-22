package praktikum2.soal3;

//pada soal digunakan "public class Employee", yang dimana seharusnya kita menggunakan "Pegawai" dan menjadi "public class Pegawai"
//"public class Employee"
public class Pegawai {
	public String nama; 
	
	//Terjadi error karena tipe pada "public char asal" menggunakan char, char hanyar bisa menyimpan satu karakter, kita bisa merubahnya menjadi String
	//public char asal; 
	public String asal; 
	public String jabatan; 
	public int umur; 
	
	public String getNama() { 
		return nama; 
	    }
	
	public String getAsal() { 
		return asal; 
	    } 
	//Tambah "String j" pada "setJabatan()"
	//public void setJabatan()
	public void setJabatan(String j) { 
		this.jabatan = j; 
	    }
}
