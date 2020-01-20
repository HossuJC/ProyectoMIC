/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package scraping;

import com.opencsv.CSVWriter;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

/**
 *
 * @author Grupo7
 */
public class Scraping {

    private static final String BASEURL = "https://www.tripadvisor.co";
    private static HashSet<String> users = new HashSet<>();

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {

        ArrayList<String> links = new ArrayList<>();
        links.add("/Attractions-g294307-Activities-c57-t68-Ecuador.html");
        links.add("/Attractions-g294307-Activities-c61-t52-Ecuador.html");
        links.add("/Attractions-g294307-Activities-c57-t70-Ecuador.html");
        links.add("/Attractions-g294307-Activities-c57-t162-Ecuador.html");
        links.add("/Attractions-g294307-Activities-c57-t20-Ecuador.html");
        links.add("/Attractions-g294307-Activities-c57-t95-Ecuador.html");
        links.add("/Attractions-g294307-Activities-c57-t58-Ecuador.html");
        links.add("/Attractions-g294307-Activities-c57-t67-Ecuador.html");
        links.add("/Attractions-g294307-Activities-c57-t94-Ecuador.html");
        links.add("/Attractions-g294307-Activities-c61-t87-Ecuador.html");
        links.add("/Attractions-g294307-Activities-c61-t134-Ecuador.html");
        links.add("/Attractions-g294307-Activities-c57-t57-Ecuador.html");
        links.add("/Attractions-g294307-Activities-c57-t59-Ecuador.html");
        links.add("/Attractions-g294307-Activities-c57-t66-Ecuador.html");
        links.add("/Attractions-g294307-Activities-c57-t61-Ecuador.html");
        links.add("/Attractions-g294307-Activities-c57-t54-Ecuador.html");
        links.add("/Attractions-g294307-Activities-c61-t83-Ecuador.html");
        links.add("/Attractions-g294307-Activities-c57-t119-Ecuador.html");
        links.add("/Attractions-g294307-Activities-c57-t164-Ecuador.html");
        links.add("/Attractions-g294307-Activities-c57-t53-Ecuador.html");
        links.add("/Attractions-g294307-Activities-c57-t266-Ecuador.html");

        links.forEach((link) -> {
            datosAtracciones(link);
        });
        
        System.out.println("Cantidad de usuarios individuales: " + users.size());

    }

    public static void datosAtracciones(String url) {

        try {
            Document doc = Jsoup.connect(BASEURL + url).maxBodySize(0).timeout(0).get();
            String categoria = doc.selectFirst("div.adjust-for-heading").text().replace(" en Ecuador", "");
            try (FileOutputStream os = new FileOutputStream("DatasetsUsers/" + categoria + ".csv")) {
                os.write(0xef);
                os.write(0xbb);
                os.write(0xbf);
                CSVWriter writerAtracciones = new CSVWriter(new OutputStreamWriter(os), '|', '"', '"', "\n");
                String[] header = {"Destino", "Categoria", "Atraccion", "Comentario", "Usuario", "Calificación", "Año"};
                writerAtracciones.writeNext(header);
                Elements atracciones;
                atracciones = doc.select("div.listing_title");
                atracciones.forEach((e) -> {
                    try {
                        String atraccion = e.selectFirst("a").text();
                        String destino = e.selectFirst("var").text();
                        String atracUrl = e.selectFirst("a").attr("href");
                        System.out.println(atraccion + " --- " + destino + " --- " + atracUrl);
                        datosAtracciones(atracUrl, destino, categoria, atraccion, writerAtracciones);
                    } catch (IOException ex) {
                        Logger.getLogger(Scraping.class.getName()).log(Level.SEVERE, null, ex);
                    }
                });
            }
        } catch (IOException ex) {
            Logger.getLogger(Scraping.class.getName()).log(Level.SEVERE, null, ex);
        }

    }

    public static void datosAtracciones(String newUrl, String destino, String categoria, String atrac, CSVWriter writer) throws IOException {
        Document doc1 = Jsoup.connect(BASEURL + newUrl).maxBodySize(0).timeout(0).get();
        Element pageLast = doc1.getElementsByClass("pageNum").last();
        ArrayList<String> paginas = new ArrayList<>();
        paginas.add(newUrl);
        if (pageLast != null) {
            int numPage = 5;
            while (numPage < Integer.valueOf(pageLast.text()) * 5) {
                paginas.add(newUrl.replaceFirst("-Reviews", "-Reviews-or" + numPage));
                numPage += 5;
            }
//            paginas.forEach((p) -> {
//                System.out.println(p);
//            });
        }
        paginas.forEach((link) -> {
            try {
                Document doc2 = Jsoup.connect(BASEURL + link).maxBodySize(0).timeout(0).get();
                if (doc2.baseUri().equals(BASEURL + link)) {
                    System.out.println("****");
                    System.out.println(BASEURL + link);
                    System.out.println(doc2.baseUri());
                    System.out.println("****");
                    Elements coments = doc2.select("div.location-review-card-Card__ui_card--2Mri0.location-review-card-Card__card--o3LVm.location-review-card-Card__section--NiAcw");
                    for (Element coment : coments) {
                        String[] atraccion = {"", "", "", "", "", "", ""};
                        atraccion[0] = destino;
                        atraccion[1] = categoria;
                        atraccion[2] = atrac;
                        atraccion[3] = coment.select("div._2f_ruteS._1bona3Pu > div > q > span").text();
                        String user = coment.select("div.social-member-event-MemberEventOnObjectBlock__event_type--3njyv > span > a").text();
                        atraccion[4] = user;
                        users.add(user);
                        atraccion[5] = coment.selectFirst("div.location-review-review-list-parts-RatingLine__container--2bjtw > div > span").toString().substring(37, 38);
                        Element anio = null;
                        anio = coment.selectFirst("div.location-review-review-content-ttd-review-content-ttd__footer--VYYV8 > span");
                        if (anio != null) {
                            atraccion[6] = getNumeros(anio.text());
                        }
                        writer.writeNext(atraccion);
                        System.out.println(Arrays.toString(atraccion));
                    }
                }
            } catch (IOException ex) {
                Logger.getLogger(Scraping.class.getName()).log(Level.SEVERE, null, ex);
            }
        });

    }

    public static String getNumeros(String cadena) {
        char[] cadena_div = cadena.toCharArray();
        String n = "";
        for (int i = 0; i < cadena_div.length; i++) {
            if (Character.isDigit(cadena_div[i])) {
                n += cadena_div[i];
            }
        }
        return n;
    }

}
