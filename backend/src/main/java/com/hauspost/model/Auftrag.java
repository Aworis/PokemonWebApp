package com.hauspost.model;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;

@Entity
@Table(name = "auftrag")
@Getter
@Setter
@NoArgsConstructor
public class Auftrag {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private LocalDateTime erstelltAm;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private AuftragStatus status;

    @ManyToOne
    @JoinColumn(name = "abholstation_id", nullable = false)
    private Abholstation abholstation;

    @Column(nullable = false)
    private String mitarbeiterName;

    @Column
    private String mitarbeiterAdId;

    @Column(nullable = false)
    private String bueroNummer;

    @PrePersist
    public void prePersist() {
        if (erstelltAm == null) {
            erstelltAm = LocalDateTime.now();
        }
        if (status == null) {
            status = AuftragStatus.NEU;
        }
    }
}
