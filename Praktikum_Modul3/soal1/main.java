package soal1;

import java.util.LinkedList;
import java.util.Scanner;

public class main {
	public static void main (String args[]) {
		Scanner input = new Scanner(System.in);
		int banyakDadu = input.nextInt();
		
		LinkedList<Dadu> jumlahDadu = new LinkedList<>();
		for (int i = 0; i < banyakDadu; i++) {
			Dadu angkaDadu = new Dadu();
			jumlahDadu.add(angkaDadu);
			System.out.println("Dadu ke-" + (i + 1) + " bernilai " + angkaDadu.getNilai());
		}
		
		int totalAngka = 0;
		for (int i = 0; i < banyakDadu; i++) {
			Dadu dadu = jumlahDadu.get(i);
			totalAngka += dadu.getNilai();
		}
		
		System.out.println("Total nilai dadu keseluruhan " + totalAngka);
		
		input.close();
		
	}
}
