def collect_hrefs_from_xml_sitemap_index_and_store_in_txtfile(index_url='', unprocessed_file='', destination=''):
    """
      XML Sitemap Index URL Collector
    
        Recursively processes an XML sitemap index, discovers nested sitemap files and webpage URLs, stores pending sitemap URLs in an unprocessed queue file, and writes processed sitemap URLs and discovered webpage URLs into the destination text file while avoiding duplicates through streamed XML parsing.
    
    Args:
        index_url (str): URL of the root XML sitemap or sitemap index used as the starting point for traversal.  
        unprocessed_file (str): Path to a text file used as a persistent queue containing sitemap URLs that still need processing. (Defaults to '')
        destination (str): Path to a text file where processed sitemap URLs and discovered webpage URLs are stored.  
    
    Returns:
        Any: Result returned by the internal sitemap processing routine. Primarily performs file-writing side effects and typically returns None.
    
    Example usage:
        >>> result = collect_hrefs_from_xml_sitemap_index_and_store_in_txtfile(index_url='https://huggingface.co/sitemap.xml', unprocessed_file='tmp.txt', destination='sitemap.txt')
	"""

    import os
    import shutil
    import xml.etree.ElementTree as ET
    from urllib.parse import urlparse
    import requests
    #WORKS
    
    def is_link_in_file(file_path, target_link):
        """Prüft zeilenweise auf der Festplatte, ob ein Link existiert (0 MB RAM)."""
        if not os.path.exists(file_path):
            return False
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip() == target_link:
                    return True
        return False
    
    
    def remove_link_from_unprocessed(file_path, link_to_remove):
        """Entfernt eine abgearbeitete Sitemap vom Datenträger via Temp-Datei."""
        temp_path = file_path + ".tmp"
        with (
            open(file_path, "r", encoding="utf-8") as fin,
            open(temp_path, "w", encoding="utf-8") as fout,
        ):
            for line in fin:
                if line.strip() != link_to_remove:
                    fout.write(line)
        shutil.move(temp_path, file_path)
    
    
    def get_next_sitemap(file_path):
        """Holt die nächste zu verarbeitende Sitemap aus der Unprocessed-Datei."""
        if not os.path.exists(file_path):
            return None
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                cleaned = line.strip()
                if cleaned:
                    return cleaned
        return None
    
    
    def is_xml_sitemap(url):
        """Prüft, ob die URL eine XML-Sitemap ist."""
        return url.lower().endswith(".xml") or "sitemap" in url.lower()
        
    
    def collect_hrefs_from_xml_sitemap(index_url, unprocessed_file, processed_file):
        """Verarbeitet Sitemaps: XMLs in unprocessed, normale URLs direkt in processed.
        """
        # Dateien initialisieren
        for path in [unprocessed_file, processed_file]:
            if not os.path.exists(path):
                with open(path, "w", encoding="utf-8") as f:
                    pass
    
        # Index-URL prüfen und als erste Aufgabe in Unprocessed ablegen
        if not is_link_in_file(processed_file, index_url) and not is_link_in_file(unprocessed_file, index_url):
            with open(unprocessed_file, "a", encoding="utf-8") as f:
                f.write(index_url + "\n")
    
        # Hauptschleife: Arbeitet die Unprocessed-Liste ab
        while True:
            current_sitemap = get_next_sitemap(unprocessed_file)
    
            # Keine Sitemaps mehr übrig -> Fertig!
            if not current_sitemap:
                print("\nAlle Sitemaps erfolgreich verarbeitet!")
                break
    
            print(f"\nÖffne Sitemap: {current_sitemap}")
    
            try:
                # XML-Inhalt streamen (schont den RAM)
                response = requests.get(current_sitemap, stream=True, timeout=15)
                response.raise_for_status()
    
                # Element für Element parsen
                context = ET.iterparse(response.raw, events=("end",))
    
                for event, elem in context:
                    # Namespace entfernen für sauberen Abgleich
                    tag_name = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
    
                    if tag_name == "loc" and elem.text:
                        link = elem.text.strip()
                        parsed_url = urlparse(link)
    
                        # Validierung
                        if parsed_url.scheme in ["http", "https"] and parsed_url.netloc:
    
                            # Fall 1: Gefundener Link ist eine Unter-Sitemap -> In Unprocessed speichern
                            if is_xml_sitemap(link):
                                if not is_link_in_file( unprocessed_file, link ) and not is_link_in_file(processed_file, link):
                                    with open( unprocessed_file, "a", encoding="utf-8" ) as f:
                                        f.write(link + "\n")
                                    print(f" -> Sub-Sitemap gemerkt: {link}")
    
                            # Fall 2: Gefundener Link ist eine normale URL -> DIREKT in Processed speichern
                            else:
                                if not is_link_in_file(processed_file, link):
                                    with open( processed_file, "a", encoding="utf-8" ) as f:
                                        f.write(link + "\n")
                                    print(f" -> Web-URL direkt gespeichert: {link}")
    
                    # Speicher direkt wieder freigeben
                    elem.clear()
    
                # Nach erfolgreichem Parsen: Aktuelle Sitemap als verarbeitet markieren
                if not is_link_in_file(processed_file, current_sitemap):
                    with open(processed_file, "a", encoding="utf-8") as f:
                        f.write(current_sitemap + "\n")
                remove_link_from_unprocessed(unprocessed_file, current_sitemap)
    
            except Exception as e:
                print(f"Fehler bei Sitemap {current_sitemap}: {e}")
                # Bei Fehlern (z.B. HTTP 404) in Processed loggen, damit sie aus der Schleife fliegt
                with open(processed_file, "a", encoding="utf-8") as f:
                    f.write(f"{current_sitemap} (FAILED: {e})\n")
                remove_link_from_unprocessed(unprocessed_file, current_sitemap)
    return collect_hrefs_from_xml_sitemap(index_url, unprocessed_file, destination)
                
#collect_hrefs_from_xml_sitemap_index_and_store_in_txtfile('https://huggingface.co/sitemap-doc.xml', 'testxml.txt') 
#collect_hrefs_from_xml_sitemap_index_and_store_in_txtfile('https://huggingface.co/sitemap.xml', 'tmp.txt', 'sitemap.txt')