package com.hauspost.controller;

import com.hauspost.model.Abholstation;
import com.hauspost.repository.AbholstationRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/abholstationen")
@RequiredArgsConstructor
public class AbholstationController {

    private final AbholstationRepository abholstationRepository;

    @GetMapping
    public List<Abholstation> findAll() {
        return abholstationRepository.findAll();
    }

    @PostMapping
    public ResponseEntity<Abholstation> create(@RequestBody Abholstation abholstation) {
        return ResponseEntity.ok(abholstationRepository.save(abholstation));
    }
}
