package soal2;

import java.util.LinkedList;
import java.util.Scanner;

public class main {
	public static void main(String args[]) {
		Scanner input = new Scanner(System.in);
		int banyakNegara = input.nextInt();
		input.nextLine();
		
		LinkedList<Negara> dataNegara = new LinkedList<>();
		for (int i = 0; i < banyakNegara; i++) {
			String nama = input.nextLine();
			String jenisKepemimpinan = input.nextLine();
			String namaPemimpin = input.nextLine();
			
			if (jenisKepemimpinan.equalsIgnoreCase("monarki")) {
				dataNegara.add(new Negara(nama, jenisKepemimpinan, namaPemimpin));
			} else {
				int tanggalKemerdekaan = input.nextInt();
				int bulanKemerdekaan = input.nextInt();
				int tahunKemerdekaan = input.nextInt();
				input.nextLine();
				dataNegara.add(new Negara(nama, jenisKepemimpinan, namaPemimpin, tanggalKemerdekaan, bulanKemerdekaan, tahunKemerdekaan));
			}
		}
		
        for (Negara negara : dataNegara) {
            if (negara.getJenisKepemimpinan().equalsIgnoreCase("monarki")) {
                System.out.println("Negara " + negara.getNama() + " mempunyai Raja bernama " + negara.getNamaPemimpin());
                System.out.println(" ");
            } else {
                System.out.println("Negara " + negara.getNama() + " mempunyai " + negara.getJenisKepemimpinan() + " bernama " + negara.getNamaPemimpin() + "\nDeklarasi Kemerdekaan pada Tanggal " + negara.getTanggalKemerdekaan() + " " + negara.getNamaBulan(negara.getBulanKemerdekaan()) + " " + negara.getTahunKemerdekaan());
                System.out.println(" ");
            }
        }
		input.close();
	}
}
