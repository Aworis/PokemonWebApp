package com.hauspost.controller;

import com.hauspost.model.Abholstation;
import com.hauspost.model.Auftrag;
import com.hauspost.model.AuftragStatus;
import com.hauspost.repository.AbholstationRepository;
import com.hauspost.repository.AuftragRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

import java.time.LocalDateTime;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
class AuftragControllerPdfExportTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private AuftragRepository auftragRepository;

    @Autowired
    private AbholstationRepository abholstationRepository;

    @BeforeEach
    void setUp() {
        auftragRepository.deleteAll();
        abholstationRepository.deleteAll();

        Abholstation station = new Abholstation();
        station.setName("Eingang EG");
        station = abholstationRepository.save(station);

        Auftrag openAuftrag = new Auftrag();
        openAuftrag.setStatus(AuftragStatus.NEU);
        openAuftrag.setErstelltAm(LocalDateTime.now());
        openAuftrag.setAbholstation(station);
        openAuftrag.setMitarbeiterName("Max Mustermann");
        openAuftrag.setBueroNummer("3.007");
        auftragRepository.save(openAuftrag);

        Auftrag closedAuftrag = new Auftrag();
        closedAuftrag.setStatus(AuftragStatus.ERLEDIGT);
        closedAuftrag.setErstelltAm(LocalDateTime.now());
        closedAuftrag.setAbholstation(station);
        closedAuftrag.setMitarbeiterName("Erika Muster");
        closedAuftrag.setBueroNummer("2.001");
        auftragRepository.save(closedAuftrag);
    }

    @Test
    void exportPdf_returnsStatusOkAndContentTypePdf() throws Exception {
        mockMvc.perform(get("/api/auftraege/export/pdf"))
                .andExpect(status().isOk())
                .andExpect(content().contentType(MediaType.APPLICATION_PDF))
                .andExpect(header().string("Content-Disposition",
                        org.hamcrest.Matchers.containsString("attachment")))
                .andExpect(header().string("Content-Disposition",
                        org.hamcrest.Matchers.containsString("hauspost-offene-auftraege")));
    }

    @Test
    void exportPdf_responseBodyIsNonEmpty() throws Exception {
        byte[] body = mockMvc.perform(get("/api/auftraege/export/pdf"))
                .andExpect(status().isOk())
                .andReturn()
                .getResponse()
                .getContentAsByteArray();

        assert body.length > 0 : "PDF body must not be empty";
    }
}
