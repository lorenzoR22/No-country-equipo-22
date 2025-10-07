package com.example.auth_service.Repositories;


import com.example.auth_service.Models.Entities.ERole;
import com.example.auth_service.Models.Entities.Role;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface RoleRepository extends JpaRepository<Role, Long> {
    Optional<Role> findByName(ERole name);
}
