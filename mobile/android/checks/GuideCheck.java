import es.lexia.piloto.ReadingGuide;
import java.util.Arrays;

public class GuideCheck {
    static void check(int confirmed,int count,int width,int from,int to){
        int[] actual=ReadingGuide.range(confirmed,count,width);
        if(actual[0]!=from||actual[1]!=to)throw new AssertionError(Arrays.toString(actual));
    }
    public static void main(String[] args){
        check(0,5,2,0,2);check(1,5,2,1,3);check(2,5,2,2,4);
        check(0,5,3,0,3);check(1,5,3,1,4);check(2,5,3,2,5);
        check(3,5,3,3,5);check(4,5,3,4,5);check(5,5,3,5,5);
        check(4,5,2,4,5);check(5,5,2,5,5);check(1,5,1,1,2);
        check(-1,5,3,0,3);check(9,5,3,5,5);check(0,0,3,0,0);
        // Relectura: la guía vuelve al intervalo que respalda la posición aceptada.
        check(3,9,3,3,6);check(2,9,3,2,5);
        System.out.println("Guía móvil 1/2/3: extremos, palabra a palabra, final y relectura correctos.");
    }
}
