from pypdf import PdfWriter

def merge_pdfs(filenames: list, playlist_id: str):
    writer = PdfWriter()  # Use PdfWriter instead of PdfMerger
    for filename in filenames:
        with open(filename, "rb") as f:
            writer.append(f)  # Append each PDF file to the writer
    with open("PlaylistSummary/"+playlist_id+".pdf", "wb") as output_file:
        writer.write(output_file)  # Write the merged PDF to an output file
    print("pdf merged : "+playlist_id+".pdf")
    return playlist_id+".pdf  Generated ✅" 