/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package apiparser;

import java.util.Scanner;
import java.io.*;
import java.math.BigInteger;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;

/**
 *
 * @author leoll
 */
public class APIParser {

    /**
     * @param args the command line arguments
     */
    static String readFile(String filename) {
        File f = new File(filename);
        try {
            byte[] bytes = Files.readAllBytes(f.toPath());
            return new String(bytes, "UTF-8");
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return "";
    }

    public static void main(String[] args) {

        String wikitext = ""; //takes entire text of every episode (except ep 375 due to disambiguation page)
        wikitext = readFile("D:/projects/apicallresults.txt");
        String[] eptext = wikitext.split("===Pokxc3xa9mon===|=== Pokxc3xa9mon ==="); //splits wikiktext to seperate episodes
        
        //make sure it's just the pokemon section being considered
        for (int i = 1; i < eptext.length; i++) {
            eptext[i] = eptext[i].split("==")[0];
        }

        for (int i = 1; i < eptext.length; i++) {

            System.out.println("EP: " + (i));
            String[] pokemon = eptext[i].split("POKETIME");
            HashSet pokemoncheck = new HashSet(); //used to check for duplicates
            
            for (int j = 1; j < pokemon.length; j++) {
                //check for duplicates since HashSet.add can't add duplicates.
                if (pokemoncheck.add(pokemon[j].split("}}")[0])) {
                  System.out.println(pokemon[j].split("}}")[0]);
                }

            }
        }

    }

}
