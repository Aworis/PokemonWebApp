package com.hauspost.service;

import com.hauspost.model.Auftrag;
import com.hauspost.model.AuftragStatus;
import com.hauspost.repository.AuftragRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class AuftragService {

    private static final List<AuftragStatus> OPEN_STATUSES =
            List.of(AuftragStatus.NEU, AuftragStatus.OFFEN, AuftragStatus.IN_BEARBEITUNG);

    private final AuftragRepository auftragRepository;

    public List<Auftrag> findAll() {
        return auftragRepository.findAll();
    }

    public Auftrag create(Auftrag auftrag) {
        return auftragRepository.save(auftrag);
    }

    public List<Auftrag> findOpenOrders() {
        return auftragRepository.findByStatusIn(OPEN_STATUSES);
    }
}
