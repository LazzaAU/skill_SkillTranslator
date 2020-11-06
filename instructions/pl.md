
# <Span style = "color: #ff0000;"> <strong> Instrukcje </span> </strong>

Więc napisałem umiejętności i chcesz go tłumaczyć? Dobra robota, pozwala dostać się do niego wtedy.

# <Span style = "color: #0000FF;"> <strong> Szybkie kroki operacyjne </span> </strong>

** Aby skorzystać z tej umiejętności **

1. Przejdź do ustawień umiejętności

2. Wprowadź nazwę umiejętności chcesz przetłumaczyć w pole ** ** skillTitle

3. Kliknij przycisk Zapisz

Zapytaj Alice „przetłumaczyć moje umiejętności”

# <Span style = "color: #0000FF;"> <strong> Zręcznościowe Przegląd </span> </strong>

- Tryb Precheck
 
Spowoduje to uruchomienie przez proces translacji bez faktycznie wysyłanie danych tłumaczenie Google.
Jest to run obojętne, które nie będą modyfikować pliki, ale dać statystyczny zwrotne na końcu procesu.

Tryb ten wykorzystuje plik językowy umiejętność została napisana w (ustawiany za pomocą ... umiejętności ustawień >> skillLanguage) w celu ustalenia danych statystycznych dotyczących procesu tłumaczenia
przed wysłaniem tych danych do Google. W ten sposób można dokonać świadomej decyzji, jeżeli

1. istnieją błędy w plikach, które zatrzymują proces tłumaczenia

2. Pliki są w granicach kontyngentów gogle lub nad nim w granicach i dlatego będzie wyzwalać w budowanych bezpiecznych strażników

Po biegu i nie wykazuje żadnych błędów, włącz ten tryb off uruchomić umiejętności w trybie Translation


## ** Po uruchomieniu w trybie translacji: **

Umiejętność przełoży pierwszy katalog rozmów. Jeśli wnioski są wykonane do Google przekroczyć kwoty to będzie
wstrzymać kod 70 sekund (Przerwa umiejętności nie Alicja), a następnie wznowione.

Umiejętność następnie przetłumaczyć plik dialogowe i wykonać bezpieczne strażników samego kontyngentu. (Uwaga: Jeśli liczba znaków
na przykład jedna prawdopodobnie przekraczać 1500 kod zostanie zatrzymana przez 1 godzinę)

Podczas translacji Okno szablonu kod wyodrębnia: => keyvalue} część wypowiedzi
tak że keyvalue robi tłumaczone i zatrzymać umiejętności z pracy. Następnie umieścić że kod Backin
przed zapisaniem go do pliku.

Po przetłumaczeniu będzie następnie dodać wszystkie 4 języki do pliku instalacyjnego.

## ** ** Pole skillPath (opcjonalnie)

- Jest to poręczne od chcesz przetłumaczyć pliki umiejętności, które są poza folderu umiejętności

  - ** IE: **
 
    - Jeśli jesteś dev umiejętności i mieć mistrza skopiować chcesz przetłumaczyć, zamiast przetłumaczyć aktywną umiejętności
które mogą mieć zwyczaj w wypowiedzi itp.

Wpisz ścieżkę ** Aby ** Umiejętność ale ** Nie ** koszt skillname. (W polu skillTitle do tego)

NA PRZYKŁAD:

- skillPath = / Home / PI / DevelopmentSkills
- skillTitle = HomeAssistant
,

## ** ** Pole SkillTitle (obowiązkowe)

To pole wskazuje umiejętności, które chcesz przetłumaczyć

- Dzięki tej dziedzinie i wypełnione ** Nie ** * i * skillPath dziedzinie, jak również wtedy domyślne ścieżka do folderu ProjectAlice / umiejętności
- Dzięki tej dziedzinie i pola skillPath ** ** NIE wypełnia wtedy tłumaczyć tę umiejętność domyślnie ..
_
## ** ** translateOnlyThis

Dla tej dziedzinie ...

- Puste = przełoży wszystkie wymagane pliki (domyślnie)

- Wprowadzić jedną z następujących opcji, aby przetłumaczyć tylko, że katalog (opcjonalnie)
 - rozmowy
 - dialog
 - instrukcje
 - Przykładowe pliki

## ** ** ignoreLanguages

Powiedzmy, że wiem, że niemieckie i francuskie tłumaczenie zostało wykonane ręcznie przez @translator w niezgodzie.
więc chcesz przetłumaczyć swoje umiejętności, ale wyklucza tłumaczenie niemieckich i francuskich. Cóż można zrobić z

** ignoreLanguages ​​** pole. W powyższym senario byłoby po prostu wejść w tej dziedzinie
`` `de, fr```

Uwaga: oddzielne języków z przecinkiem
 _______________________

#Tips

Obecnie .. jeśli uruchomić umiejętności w jednym języku, a następnie uruchomić umiejętności w innym języku można uderzyć błąd.
Restart Alicja jeśli przełączania języków domyślnych między próbami.

- Dygresja:

 jeśli się zdarzają, aby uzyskać ten błąd konsekwentnie ..
 
 `` Json.decoder.JSONDecodeError: wartość Oczekiwano: kolumna 1, wiersz 1 (znak 0) ``
 
 Następnie potencjalnie Gogle właśnie zablokował swój adres IP z przeliczenia plików i będziesz musiał czekać, aż po północy czasu pacyficznego dla niego t być odblokowane

------------------

Google translate dąży do miłości dodając spacje gdzie spacje nie było wcześniej. Chociaż ta umiejętność co¶ do chwytania
niektóre z tych przypadkach może się okazać, że przy tłumaczeniu z instrukcjami Folder jeśli masz znaczniki w promocji cenowych
że być może trzeba będzie ręcznie wyjąć kilka spacji aby wyświetlać prawidłowo.

** Co umiejętności nie zrobi **

Obecnie umiejętność nie przełoży przecenowych plików, takich jak opisane w instrukcji. To cecha należy doliczyć przyszłość

UWAGA: dokładność tłumaczeń nie jest gwarantowane prawidłowe. Stawiamy na google jest w stanie również zrozumieć
kontekst wypowiedzi. Po przeliczeniu poprzez tej umiejętności będzie wymagało ręcznej weryfikacji z @translator w
Niezgodność kanale
 
Ciesz tłumaczenia