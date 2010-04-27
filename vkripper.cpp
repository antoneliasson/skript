/*
 * vkgoeswild ripper rev. 1
 *
 * Sparar alla mp3-filer från vkgoeswild.com med hjälp av wget.
 *
 * Användning: Gå in på http://www.vkgoeswild.com/?section=mp3&songs=1 och visa
 * HTML-koden för länkarna till mp3-filerna. Den ska vara i formatet
 * <li><a href="downloads.php3?song=355">Guns N' Roses - Estranged</a><li><a href... osv.
 * Kopiera hela raden och spara i filen vkgoeslinks i mappen du står i när du kör programmet.
 * Kör programmet med ./vkripper
 * Det sparar alla filer i vkgoeslinks till mappen du står i.
 *
 * OBS! Jag har inte implementerat någon felhantering alls för jag
 * slängde bara ihop programmet på en halvtimme. Det KAN (läs: kommer att) krasha
 * om något oväntat händer, men det duger för mina behov för tillfället.
 *
 * Koden för funktionen Tokenize har jag tagit utan lov från
 * http://www.oopweb.com/CPP/Documents/CPPHOWTO/Volume/C++Programming-HOWTO-7.html
 * Hoppas att det går bra.
 *
 * All annan kod är skriven av mig
 * (c) Anton Eliasson, 26 april 2010
 * Licens: Creative Commons Attribution-Share Alike 3.0
 *
 */

#include <iostream>
#include <string>
#include <algorithm>
#include <vector>
#include <fstream>
using namespace std;

void Tokenize(const string& str, vector<string>& tokens, const string& delimiters = " ")
{
    // Skip delimiters at beginning.
    string::size_type lastPos = str.find_first_not_of(delimiters, 0);
    // Find first "non-delimiter".
    string::size_type pos     = str.find_first_of(delimiters, lastPos);

    while (string::npos != pos || string::npos != lastPos)
    {
        // Found a token, add it to the vector.
        tokens.push_back(str.substr(lastPos, pos - lastPos));
        // Skip delimiters.  Note the "not_of"
        lastPos = str.find_first_not_of(delimiters, pos);
        // Find next "non-delimiter"
        pos = str.find_first_of(delimiters, lastPos);
    }
}

int main()
{
    ifstream infil;
    vector<string> tokens;

    infil.open("vkgoeslinks");
    if (!infil) {
        cout << "Kunde inte öppna fil!";
        exit(1);
    }

    string str;
    getline(infil, str);    // bör ta hela filen om den är i rätt format
    
    Tokenize(str, tokens, "\"");

    for (unsigned int i = 0; i < tokens.size(); i++) {
/*        if (i % 2 == 1) {   // vi vill endast ha de ojämna strängarna
            cout << tokens.at(i) << endl;
        }*/
        string temp = tokens.at(i); // plockar ut en delsträng
        //cout << temp << endl;
        if (temp.find("downloads.php3?song=") == 0) {    // giltig länk
            string cmd = "wget http://www.vkgoeswild.com/" + temp;  // bygg kommando
//            cout << cmd << endl;
            if (system(cmd.c_str())) {  // spara mha wget
                cout << "status: 1\n";
            } else {
                cout << "status: 0\n";
            }
        }
    }
}

