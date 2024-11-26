package soal1;

import java.util.Random;

class Dadu {
    private int valueDadu;
    
    Dadu() {
    	this.valueDadu = valueDadu;
        this.acakNilai();
    }
    
    void acakNilai() {
    	Random rand = new Random();
    	valueDadu = rand.nextInt(6) + 1;
    }
    
    public int getNilai() {
    	return valueDadu;
    }
    
}
