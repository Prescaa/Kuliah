import java.util.Scanner;

public class PRAK104_2310817210023_RIFKYPUTRAMAHARDIKA {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);

        System.out.print("Tangan Abu: ");
        String[] tanganAbu = input.nextLine().split(" ");
        System.out.print("Tangan Bagas: ");
        String[] tanganBagas = input.nextLine().split(" ");

        int poinAbu = 0;
        int poinBagas = 0;

        for (int ronde = 0; ronde < 3; ronde++) {
            char pilihanAbu = tanganAbu[ronde].charAt(0);
            char pilihanBagas = tanganBagas[ronde].charAt(0);

            if ((pilihanAbu == 'B' && pilihanBagas == 'G') ||
                (pilihanAbu == 'G' && pilihanBagas == 'K') ||
                (pilihanAbu == 'K' && pilihanBagas == 'B')) {
                poinAbu++;
            } else if ((pilihanBagas == 'B' && pilihanAbu == 'G') ||
                       (pilihanBagas == 'G' && pilihanAbu == 'K') ||
                       (pilihanBagas == 'K' && pilihanAbu == 'B')) {
                poinBagas++;
            }
        }

        if (poinAbu > poinBagas) {
            System.out.println("Output: Abu");
        } else if (poinBagas > poinAbu) {
            System.out.println("Output: Bagas");
        } else {
            System.out.println("Output: Seri");
        }

        input.close();
    }
}
