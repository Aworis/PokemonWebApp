package com.hauspost.controller;

import com.hauspost.model.Auftrag;
import com.hauspost.service.AuftragService;
import com.hauspost.service.PdfExportService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.util.List;

@RestController
@RequestMapping("/api/auftraege")
@RequiredArgsConstructor
public class AuftragController {

    private final AuftragService auftragService;
    private final PdfExportService pdfExportService;

    @GetMapping
    public List<Auftrag> findAll() {
        return auftragService.findAll();
    }

    @PostMapping
    public ResponseEntity<Auftrag> create(@RequestBody Auftrag auftrag) {
        return ResponseEntity.ok(auftragService.create(auftrag));
    }

    @GetMapping("/export/pdf")
    public ResponseEntity<byte[]> exportPdf() {
        byte[] pdfBytes = pdfExportService.exportOffeneAuftraegePdf();

        String filename = "hauspost-offene-auftraege-" + LocalDate.now() + ".pdf";

        return ResponseEntity.ok()
                .contentType(MediaType.APPLICATION_PDF)
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"" + filename + "\"")
                .body(pdfBytes);
    }
}
