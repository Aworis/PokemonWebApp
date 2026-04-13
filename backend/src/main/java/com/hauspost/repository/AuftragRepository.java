package com.hauspost.repository;

import com.hauspost.model.Auftrag;
import com.hauspost.model.AuftragStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface AuftragRepository extends JpaRepository<Auftrag, Long> {

    List<Auftrag> findByStatusIn(List<AuftragStatus> statuses);
}
