package com.hauspost.repository;

import com.hauspost.model.Abholstation;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface AbholstationRepository extends JpaRepository<Abholstation, Long> {
}
