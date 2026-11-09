package es.lexia.piloto;

/** Intervalo base cero [inicio, fin): cada palabra reconocida desplaza la guía una. */
public final class ReadingGuide {
    private ReadingGuide(){}
    public static int[] range(int confirmed,int count,int width){
        int first=Math.max(0,Math.min(confirmed,count));
        return new int[]{first,Math.min(count,first+Math.max(1,width))};
    }
}
