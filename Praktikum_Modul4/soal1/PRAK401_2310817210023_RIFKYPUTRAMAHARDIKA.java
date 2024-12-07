package soal1;

import java.util.Scanner;

public class PRAK401_2310817210023_RIFKYPUTRAMAHARDIKA {
	public static void main(String args[]) {
		Scanner input = new Scanner(System.in);
		System.out.print("Nama Hewan Peliharaan: ");
		String nama = input.nextLine();
		System.out.print("Ras: ");
		String ras = input.nextLine();
		
		HewanPeliharaan displayHewan = new HewanPeliharaan(ras, nama);
		displayHewan.display();
		input.close();
	}
}
