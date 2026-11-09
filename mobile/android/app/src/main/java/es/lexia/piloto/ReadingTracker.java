package es.lexia.piloto;

import java.text.Normalizer;
import java.util.*;
import java.util.regex.*;

/** Port textual del Tracker original; no adivina tiempos acústicos o puntuación lectora. */
public final class ReadingTracker {
    public static final Pattern TOKEN=Pattern.compile("[\\p{L}\\p{N}]+(?:['’][\\p{L}\\p{N}]+)*");
    public final List<String> story;
    private final int before;
    private final boolean supported;
    public int position=0;
    private int failures=0;
    private Integer recovery=null;
    private List<String> previous=new ArrayList<>();
    public String lastMode="initial",lastReason="initial",lastSearch="local";
    public int lastMatches=0,lastHypothesisWords=0,lastEditCost=0;
    public Integer lastCandidate=null;
    public ReadingTracker(String text){this(text,12);}
    public ReadingTracker(String text,int before){this(text,before,false);}
    public ReadingTracker(String text,int before,boolean supported){
        if(before!=5&&before!=12)throw new IllegalArgumentException("Margen no admitido");
        story=tokens(text);this.before=before;this.supported=supported;
    }
    public static List<String> tokens(String text){
        List<String> out=new ArrayList<>();Matcher m=TOKEN.matcher(Normalizer.normalize(text,Normalizer.Form.NFC));
        while(m.find())out.add(m.group());return out;
    }
    private static String norm(String s){return Normalizer.normalize(s,Normalizer.Form.NFC).toLowerCase(Locale.ROOT);}
    private Integer locate(List<String> hypothesis,boolean global){
        List<String> heard=hypothesis.subList(Math.max(0,hypothesis.size()-8),hypothesis.size());
        int n=heard.size();lastHypothesisWords=n;lastMatches=0;lastEditCost=0;lastCandidate=null;lastSearch=global?"global":"local";
        if(n<2){lastReason="evidencia_insuficiente";return null;}
        // Offset 6 incluye la palabra actual y las cinco anteriores (posición base 1).
        int offset=before==5?6:12;
        int start=global?0:Math.max(0,position-offset),stop=global?story.size():Math.min(story.size(),position+24),m=stop-start;
        if(m==0){lastReason="ventana_vacia";return null;}
        int[][] dp=new int[n+1][m+1];for(int i=1;i<=n;i++)dp[i][0]=i;
        for(int i=1;i<=n;i++)for(int j=1;j<=m;j++){
            int cost=norm(heard.get(i-1)).equals(norm(story.get(start+j-1)))?0:1;
            dp[i][j]=Math.min(dp[i-1][j-1]+cost,Math.min(dp[i-1][j]+1,dp[i][j-1]+1));
        }
        int endpoint=1;
        for(int j=2;j<=m;j++)if(dp[n][j]<dp[n][endpoint] || (dp[n][j]==dp[n][endpoint]&&Math.abs(start+j-position)<Math.abs(start+endpoint-position)))endpoint=j;
        int i=n,j=endpoint,matches=0;Integer candidate=null;
        while(i>0){
            boolean equal=j>0&&norm(heard.get(i-1)).equals(norm(story.get(start+j-1)));
            if(j>0&&dp[i][j]==dp[i-1][j-1]+(equal?0:1)){
                if(equal){matches++;if(candidate==null)candidate=start+j;}i--;j--;
            }else if(dp[i][j]==dp[i-1][j]+1)i--;else j--;
        }
        boolean accepted=matches>=2&&(double)matches/n>=.6&&(double)dp[n][endpoint]/n<=.4;
        lastMatches=matches;lastEditCost=dp[n][endpoint];lastCandidate=accepted?candidate:null;
        lastReason=accepted?"coincidencia_local":"evidencia_incompatible";
        return accepted?candidate:null;
    }
    public int update(String text){return update(text,text);}
    public int update(String text,String currentLine){
        int old=position,oldFailures=failures;Integer oldRecovery=recovery;
        List<String> heard=tokens(text);if(heard.equals(previous)){lastMode="hipotesis_sin_cambios";lastReason="texto_identico";lastCandidate=null;lastMatches=0;lastHypothesisWords=Math.min(8,heard.size());lastEditCost=0;lastSearch="none";return position;}previous=heard;lastMode="local";
        Integer candidate=locate(heard,false);
        if(candidate==null){
            failures++;
            if(failures>=2){Integer global=locate(heard,true);if(global!=null){lastMode="recuperacion_pendiente";if(global.equals(recovery)){candidate=global;lastMode="recuperacion";}recovery=global;}else recovery=null;}
        }else{failures=0;recovery=null;}
        if(candidate!=null)position=candidate;
        if(supported&&position>old){
            boolean terminal=!heard.isEmpty()&&norm(heard.get(heard.size()-1)).equals(norm(story.get(position-1)));
            boolean pair=heard.size()>=2&&position>=2&&terminal&&norm(heard.get(heard.size()-2)).equals(norm(story.get(position-2)));
            if(!terminal||(position-old>1&&!pair)){
                position=old;failures=oldFailures;recovery=oldRecovery;
                lastMode="avance_rechazado";lastReason="sin_apoyo_final";
            }
        }
        if(supported&&position==old){
            List<String> recent=tokens(currentLine);
            for(int size=Math.min(8,recent.size());size>=3;size--){
                boolean distinctive=false;
                for(int k=recent.size()-size;k<recent.size();k++)if(norm(recent.get(k)).length()>=5)distinctive=true;
                if(!distinctive)continue;
                int count=0,destination=0;
                for(int start=0;start<=story.size()-size;start++){
                    boolean equal=true;
                    for(int k=0;k<size;k++)if(!norm(story.get(start+k)).equals(norm(recent.get(recent.size()-size+k)))){equal=false;break;}
                    if(equal){count++;destination=start+size;}
                }
                if(count==1&&destination>old&&destination<=old+24){
                    position=destination;failures=0;recovery=null;
                    lastMode="recuperacion_sufijo_reciente";lastReason="sufijo_exacto_unico";lastSearch="sufijo_reciente";
                    lastMatches=size;lastHypothesisWords=size;lastEditCost=0;lastCandidate=destination;
                    break;
                }
            }
        }
        return position;
    }
}
