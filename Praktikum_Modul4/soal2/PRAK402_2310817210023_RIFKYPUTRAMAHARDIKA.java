package soal2;

import java.util.Scanner;

public class PRAK402_2310817210023_RIFKYPUTRAMAHARDIKA {
	public static void main (String args[]) {
		Scanner input = new Scanner(System.in);
		System.out.println("Pilih jenis hewan yang ingin diinputkan: ");
		System.out.println("1. Kucing ");
		System.out.println("2. Anjing ");
		System.out.print("Masukkan pilihan: ");
		int pilihan = input.nextInt();
		input.nextLine();
		
		System.out.print("Nama Hewan Peliharaan: ");
		String nama = input.nextLine();
		System.out.print("Ras: ");
		String ras = input.nextLine();
		System.out.print("Warna bulu: ");
		String warnaBulu = input.nextLine();
		
		if(pilihan == 1) {		
			Kucing dataKucing = new Kucing(ras, nama, warnaBulu);
			dataKucing.displayKucing();
		}
		
		else if(pilihan == 2) {	
			System.out.print("Kemampuan: ");
			String kemampuanList = input.nextLine();
			String[] kemampuan = kemampuanList.split(", ");
			
			Anjing dataAnjing = new Anjing(nama, ras, warnaBulu, kemampuan);
			dataAnjing.displayAnjing();
		}

		input.close();
	}
}
