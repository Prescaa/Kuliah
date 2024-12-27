package soal1_praktikum6;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;

public class Main {
    public static void main(String[] args) {
        Mahasiswa[] dataMahasiswa = {
            new Mahasiswa("1234", "Rifky"),
            new Mahasiswa("1235", "Fajar"),
            new Mahasiswa("1236", "Budi"),
            new Mahasiswa("1237", "Irfan"),
            new Mahasiswa("1238", "David"),
            new Mahasiswa("1239", "Gita"),
            new Mahasiswa("1240", "Ali"),
            new Mahasiswa("1241", "Anna"),
            new Mahasiswa("1242", "Shakira"),
            new Mahasiswa("1243", "Wati")
        };

        JFrame frame = new JFrame("Data Mahasiswa");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(400, 300);

        String[] kolom = {"NIM", "Nama", ""};
        DefaultTableModel modelTabel = new DefaultTableModel(kolom, 0);
        JTable tabel = new JTable(modelTabel);

        for (int i = 0; i < dataMahasiswa.length; i++) {
            String[] baris = {dataMahasiswa[i].getNIM(), dataMahasiswa[i].getNama(), ""};
            modelTabel.addRow(baris);
        }

        JScrollPane panelScroll = new JScrollPane(tabel);
        frame.add(panelScroll, BorderLayout.CENTER);

        frame.setVisible(true);
    }
}
