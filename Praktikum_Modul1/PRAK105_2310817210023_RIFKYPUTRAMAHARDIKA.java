import java.util.Scanner;
import java.text.DecimalFormat;

public class PRAK105_2310817210023_RIFKYPUTRAMAHARDIKA {
	public static void main(String[] args) {
		Scanner input = new Scanner(System.in);
		
        System.out.print("Masukkan jari-jari: ");
        double jarijari = input.nextDouble();
        System.out.print("Masukkan tinggi: ");
        double tinggi = input.nextDouble();
        
        double volume = 3.14 * (jarijari * jarijari) * tinggi;
        DecimalFormat df = new DecimalFormat(".000");
        
        System.out.println("Volume tabung dengan jari-jari " + jarijari + " cm dan tinggi " + tinggi + " cm adalah " + df.format(volume) + " m3");
	}
}
