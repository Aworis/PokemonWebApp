package com.hauspost.service;

import com.hauspost.model.Auftrag;
import com.lowagie.text.*;
import com.lowagie.text.Font;
import com.lowagie.text.pdf.PdfPCell;
import com.lowagie.text.pdf.PdfPTable;
import com.lowagie.text.pdf.PdfWriter;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.awt.*;
import java.io.ByteArrayOutputStream;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;

@Service
@RequiredArgsConstructor
public class PdfExportService {

    private static final DateTimeFormatter FORMATTER =
            DateTimeFormatter.ofPattern("dd.MM.yyyy HH:mm");

    private final AuftragService auftragService;

    public byte[] exportOffeneAuftraegePdf() {
        List<Auftrag> offeneAuftraege = auftragService.findOpenOrders();
        return generatePdf(offeneAuftraege);
    }

    private byte[] generatePdf(List<Auftrag> auftraege) {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();

        Document document = new Document(PageSize.A4.rotate());
        PdfWriter.getInstance(document, baos);
        document.open();

        // Title
        Font titleFont = new Font(Font.HELVETICA, 16, Font.BOLD);
        Paragraph title = new Paragraph("Offene Aufträge – Hausbote", titleFont);
        title.setAlignment(Element.ALIGN_CENTER);
        document.add(title);

        // Timestamp
        Font metaFont = new Font(Font.HELVETICA, 10, Font.ITALIC);
        Paragraph timestamp = new Paragraph(
                "Exportiert am: " + LocalDateTime.now().format(FORMATTER), metaFont);
        timestamp.setAlignment(Element.ALIGN_CENTER);
        timestamp.setSpacingAfter(16f);
        document.add(timestamp);

        // Table
        PdfPTable table = new PdfPTable(6);
        table.setWidthPercentage(100);
        table.setWidths(new float[]{1.5f, 2.5f, 2f, 3f, 3f, 2f});

        addHeaderCell(table, "ID");
        addHeaderCell(table, "Erstellt am");
        addHeaderCell(table, "Status");
        addHeaderCell(table, "Abholstation");
        addHeaderCell(table, "Mitarbeiter");
        addHeaderCell(table, "Büro");

        Font cellFont = new Font(Font.HELVETICA, 9);
        for (Auftrag a : auftraege) {
            addCell(table, String.valueOf(a.getId()), cellFont);
            addCell(table, a.getErstelltAm() != null ? a.getErstelltAm().format(FORMATTER) : "", cellFont);
            addCell(table, a.getStatus() != null ? a.getStatus().name() : "", cellFont);
            String abholstationText = "";
            if (a.getAbholstation() != null) {
                abholstationText = a.getAbholstation().getId()
                        + (a.getAbholstation().getName() != null
                        ? " – " + a.getAbholstation().getName() : "");
            }
            addCell(table, abholstationText, cellFont);
            addCell(table, a.getMitarbeiterName() != null ? a.getMitarbeiterName() : "", cellFont);
            addCell(table, a.getBueroNummer() != null ? a.getBueroNummer() : "", cellFont);
        }

        document.add(table);
        document.close();

        return baos.toByteArray();
    }

    private void addHeaderCell(PdfPTable table, String text) {
        Font headerFont = new Font(Font.HELVETICA, 10, Font.BOLD, Color.WHITE);
        PdfPCell cell = new PdfPCell(new Phrase(text, headerFont));
        cell.setBackgroundColor(new Color(33, 86, 140));
        cell.setPadding(6f);
        cell.setHorizontalAlignment(Element.ALIGN_CENTER);
        table.addCell(cell);
    }

    private void addCell(PdfPTable table, String text, Font font) {
        PdfPCell cell = new PdfPCell(new Phrase(text, font));
        cell.setPadding(5f);
        cell.setHorizontalAlignment(Element.ALIGN_LEFT);
        table.addCell(cell);
    }
}
