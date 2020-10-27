
# <Span style = "color: #ff0000;"> <strong> Anleitung </span> </strong>

Sie haben also eine Fähigkeit geschrieben und wollen es übersetzen? Gute Arbeit, kann dann in sie erhalten.

# <Span style = "color: #0000FF;"> <strong> Schnellarbeitsschritte </span> </strong>

** Um diese Fähigkeit zu nutzen **

1. Gehen Sie auf die Fähigkeit Einstellungen

Geben Sie den Namen der Fertigkeit 2. Sie übersetzen in ** ** skillTitle Feld

3. Klicken Sie auf Speichern

Stellen Sie alice zu „übersetzen meine Fähigkeiten“

# <Span style = "color: #0000FF;"> <strong> Geschicklichkeits Übersicht </span> </strong>

- Precheck Modus
 
Dies wird ohne tatsächlich das Senden Übersetzungsdaten zu Google durch den Übersetzungsprozess laufen.
Es ist ein Blindlauf, der alle Dateien nicht ändern, sondern Statistik Feedback am Ende des Prozesses geben.

In diesem Modus wird die Sprachdatei wurde der Mann geschrieben (Satz über ... Geschick Einstellungen >> skillLanguage) Statistiken über den Übersetzungsprozess zu bestimmen,
vor, dass Daten an Google senden. Auf diese Weise können Sie eine fundierte Entscheidung treffen, wenn

1. gibt es Fehler in den Dateien, die den Übersetzungsprozess stoppen

2. Die Dateien sind in Goggle Quote Grenzen oder die Grenzen über und daher eingebaute sicheren Wachen auslösen

Einmal laufen und es keine Fehler zeigt, schalten Sie diesen Modus ausschalten Mann Translation-Modus ausgeführt


## ** Wenn im Übersetzungsmodus laufen: **

Der Fachmann wird die Gespräche Verzeichnis zuerst übersetzen. Wenn die Anfragen an Google, die Quote gemacht wird, sie übersteigen
halten Sie den Code für 70 Sekunden (Pause die Fertigkeit nicht Alice), dann wieder aufnehmen.

Die Fähigkeit wird dann die Dialogdatei übersetzt und macht die gleiche Quote sichere Wachen. (Hinweis: Wenn Zeichenzahl
für eine Instanz überschreitet 1500 wahrscheinlich der Code wird für 1 Stunde Pause)

Während Dialogvorlage Übersetzung extrahiert der Code die: => keyvalue} Teil der Äußerungen
so dass die keyValue doesnt bekommen übersetzt und die Fähigkeit, von der Arbeit aufhören. Anschließend setzen die dieser Code backin
bevor es in Datei schreiben.

Sobald es übersetzt werden dann alle vier Sprachen in die Datei installieren hinzuzufügen.

## ** ** skillPath Feld (optional)

- Das ist praktisch von Ihnen Ihre Fähigkeiten Dateien zu übersetzen, die außerhalb des Fähigkeit Ordners

  - ** IE: **
 
    - Wenn Sie eine Fertigkeit Entwickler und haben einen Master sind kopieren Sie übersetzen möchten, anstatt eine aktive Fähigkeit zu übersetzen
das haben benutzerdefinierte können Äußerungen etc in.

Geben Sie den Pfad ** TO ** die Fertigkeit aber ** NICHT ** die skillname. (Mit dem skillTitle Feld für diese)

Z.B:

- skillPath = / home / pi / DevelopmentSkills
- skillTitle = Homeassistant
.

## ** ** SkillTitle Feld (erforderlich)

Dieses Feld bezeichnet die Fähigkeit, die Sie übersetzen

- Mit diesem Feld gefüllt und ** NICHT ** Das * skillPath * Feld und dann dem Pfad standardmäßig auf den ProjectAlice / Fähigkeiten Ordner
- Mit diesem Feld und skillPath Feld ** NICHT ** ausgefüllt, dann wird diese Fähigkeit durch Standard übersetzen ..
_
## ** ** translateOnlyThis

Für diesen Bereich ...

- Nicht ausgefüllt = Werden alle benötigten Dateien (Standard) übersetzen

- eine der folgenden Geben Sie nur diesen Ordner (optional) zu übersetzen
 - Gespräche
 - Dialog
 - Anleitung
 - Beispieldateien

## ** ** ignoreLanguages

Angenommen, Sie wissen, dass Deutsch und Französisch Übersetzung manuell durch einen @translator in Zwietracht geschehen ist.
so dass Sie möchten, dass Ihre Fähigkeit zu übersetzen, aber die Deutsch und Französisch Übersetzung auszuschließen. Nun können Sie das mit dem tun

** ** ignoreLanguages ​​Feld. In der obigen senario würde geben Sie einfach in das Feld
`` `De, fr```

Bitte beachten Sie: seperate Sprachen mit einem Komma
 _______________________

#Tips

Derzeit .. wenn Sie die Fähigkeit in einer Sprache ausführen und dann die Fähigkeit, in einer anderen Sprache ausführen können Sie einen Fehler schlagen.
Neu starten Alice, wenn Sie die Standardsprachen zwischen den Versuchen wechseln.

- Randnotiz:

 wenn Sie geschehen, um diesen Fehler konsequent zu bekommen ..
 
 `` `Json.decoder.JSONDecodeError: Erwartung Wert: Zeile 1 Spalte 1 (char 0)` ``
 
 Dann möglicherweise, Goggle wird blockiert nur Ihre IP von übersetzen Dateien und Sie werden warten müssen, bis die folgende Mitternacht pazifischer Zeit für sie t nicht blockiert sein

------------------

Google übersetzen neigt Hinzufügen Leerzeichen zu lieben, wo Leerzeichen nicht vorher war. Obwohl diese Fähigkeit Trys zu capture
einige dieser Gelegenheiten können Sie feststellen, dass beim Übersetzen Sie den Anweisungen Ordner, wenn Sie Tags im Abschlags
dass müssen Sie manuell einige weißen Räume nehmen können es richtig angezeigt zu haben.

** Was die Fertigkeit nicht tun **

Derzeit ist die Fähigkeit nicht Abschlag Dateien übersetzen, wie diese Anweisungen. Das ist eine Zukunft Feature hinzugefügt werden

HINWEIS: die Genauigkeit der Übersetzungen ist nicht korrekt sein garantiert. Wir setzen auf Google auch in der Lage zu verstehen,
der Zusammenhang der Rede. Nach der Übersetzung über diese Fähigkeit wird es manuelle Überprüfung von einem @translator erfordert in
die Disharmonie Kanal
 
genießen Sie übersetzen