package com.example.doctors.features.doctor.service;

import com.example.doctors.config.exceptions.NotFoundException;
import com.example.doctors.features.doctor.dto.DoctorRegisterDTO;
import com.example.doctors.features.doctor.dto.DoctorResponseDTO;
import com.example.doctors.features.doctor.dto.DoctorUpdateDTO;
import com.example.doctors.features.doctor.model.Doctor;
import com.example.doctors.features.doctor.repository.IDoctorRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

@Service
public class DoctorService implements IDoctorService {

    private final IDoctorRepository doctorRepository;

    public DoctorService(IDoctorRepository doctorRepository) {
        this.doctorRepository = doctorRepository;
    }

    @Override
    public DoctorResponseDTO create(DoctorRegisterDTO doctorRegisterDTO) {
        return new DoctorResponseDTO(doctorRepository.save(new Doctor(doctorRegisterDTO)));
    }

    @Override
    public void deleteById(Long id) {
        Doctor doctor = doctorRepository.findById(id)
                .orElseThrow(() -> new NotFoundException("Doctor no encontrado"));
        doctor.deactive();
    }

    @Override
    public Page<DoctorResponseDTO> findAll(Pageable pagination) {
        return doctorRepository.findAll(pagination).map(DoctorResponseDTO::new);
    }

    @Override
    public DoctorResponseDTO findById(Long id) {
        Doctor doctor = doctorRepository.findById(id)
                .orElseThrow(() -> new NotFoundException(("Doctor no encontrado")));
        return new DoctorResponseDTO(doctor);
    }

    @Override
    public DoctorResponseDTO update(Long id, DoctorUpdateDTO doctorUpdateDTO) {
        Doctor doctor = doctorRepository.findById(id)
                .orElseThrow(() -> new NotFoundException("Doctor no encontrado"));
        doctor.update(doctorUpdateDTO);
        return new DoctorResponseDTO(doctor);
    }
}
