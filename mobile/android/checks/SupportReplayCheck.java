import es.lexia.piloto.ReadingTracker;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class SupportReplayCheck {
    public static void main(String[] args)throws Exception{
        int count=0;
        for(String path:args){
            List<String> lines=Files.readAllLines(Paths.get(path),StandardCharsets.UTF_8);
            ReadingTracker tracker=new ReadingTracker(decode(lines.get(0)),Integer.parseInt(lines.get(1)),true);
            for(String line:lines.subList(2,lines.size())){
                String[] parts=line.split("\t",-1);
                int actual=tracker.update(decode(parts[1]),decode(parts[2]));
                if(actual!=Integer.parseInt(parts[0]))throw new AssertionError(path+" fila "+count+": "+actual+" != "+parts[0]);
                count++;
            }
        }
        System.out.println("Apoyo de avances y sufijo reciente: "+count+" posiciones Java/Python iguales.");
    }
    private static String decode(String text){return new String(Base64.getDecoder().decode(text),StandardCharsets.UTF_8);}
}
