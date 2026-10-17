const fs = require('fs');
const path = require('path');

/**
 * Generiert Telefonnummern für einen bestimmten Dienst basierend auf Präfixen, Infixen und Suffix-Kriterien.
 * 
 * @param {string} service - Der Name des Dienstes.
 * @param {string} prefix - Das Länder- oder Providerpräfix (z. B. '+49').
 * @param {string} infix - Das Infix der Nummer.
 * @param {number} length - Die Gesamtlänge der Nummer (ohne Präfix).
 * @param {string} ending - Das gewünschte Suffix-Ende.
 * @param {number} count - Die Anzahl der zu generierenden Nummern.
 * @returns {Promise<string[]>} Ein Array mit den generierten Nummern.
 */
async function generate_numbers_for_service(service = '', prefix = '', infix = '', length = 11, ending = '', count = 40) {
    
    // Hilfsfunktion: Liest eine Datei ein und prüft, ob die Query-Zeile existiert (Nutzt Set für O(1) Suche)
    const check_in_file = (filePath = '', query = '') => {
        try {
            if (!fs.existsSync(filePath)) return false;
            
            const content = fs.readFileSync(filePath, 'utf-8');
            const linesSet = new Set(content.split(/\r?\n/).map(line => line.trim()));
            
            return linesSet.has(query.trim());
        } catch (e) {
            return false;
        }
    };

    const numbers = [];
    
    // Pfade generieren (entspricht der Python-Struktur)
    const unregistered = `/home/lab/programming/unlabeled/apps/phonechecker/49/unregistered/${service}/${ending}/${infix}_${length}.txt`;
    const registered = `/home/lab/programming/unlabeled/apps/phonechecker/49/registered/${service}/${ending}/${infix}_${length}.txt`;

    const suffix_length = length - infix.length;
    if (suffix_length <= 0) return [];

    const maxSuffixValue = Math.pow(10, suffix_length);
    const rangeMax = maxSuffixValue - 500;
    
    // Zufälligen Startwert ermitteln (Sicherheits-Check gegen negative Werte)
    const startRange = rangeMax > 0 ? Math.floor(Math.random() * rangeMax) : 0;

    for (let _suffix = startRange; _suffix < maxSuffixValue; _suffix++) {
        const suffixStr = _suffix.toString();

        if (suffixStr.endsWith(ending)) {
            // Entspricht dem Python-Padding f'{_suffix:0{suffix_length}d}'
            const suffix = suffixStr.padStart(suffix_length, '0');

            // Abgleich gegen die beiden Log-Dateien
            if (!check_in_file(unregistered, suffix) && !check_in_file(registered, suffix)) {
                const phone = `${prefix}${infix}${suffix}`;

                if (!numbers.includes(phone)) {
                    numbers.push(phone);

                    // Wenn die gewünschte Menge erreicht ist, sofort zurückgeben
                    if (numbers.length === count) {
                        return numbers;
                    }
                }
            }
        }
    }

    return numbers;
}

// === Beispiel-Aufruf ===
// (async () => { const generatedList = await generate_numbers_for_service('whatsapp', '+49', '163', 11, '97', 5); console.log(generatedList); })();