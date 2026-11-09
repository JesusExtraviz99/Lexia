import es.lexia.piloto.ReadingTracker;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

/** Fixtures generadas desde Python: texto, margen solicitado y posiciones esperadas. */
public class MarginReplayCheck {
    public static void main(String[] args)throws Exception{
        int count=0;
        for(String path:args){
            List<String> lines=Files.readAllLines(Paths.get(path),StandardCharsets.UTF_8);
            String story=new String(Base64.getDecoder().decode(lines.get(0)),StandardCharsets.UTF_8);
            ReadingTracker tracker=new ReadingTracker(story,Integer.parseInt(lines.get(1)));
            for(String line:lines.subList(2,lines.size())){
                String[] parts=line.split("\t",-1);
                String hypothesis=new String(Base64.getDecoder().decode(parts[1]),StandardCharsets.UTF_8);
                int actual=tracker.update(hypothesis),expected=Integer.parseInt(parts[0]);
                if(actual!=expected)throw new AssertionError(path+": "+actual+" != "+expected);
                count++;
            }
        }
        System.out.println("Margen original y cinco palabras: "+count+" posiciones Java/Python iguales.");
    }
}
