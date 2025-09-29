package com.example.auth_service.Controllers;

import com.example.auth_service.Models.Dtos.*;
import com.example.auth_service.Services.AuthService;
import com.example.auth_service.Services.PasswordService;
import com.example.auth_service.Services.RegistrationService;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import jakarta.mail.MessagingException;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.security.Principal;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/auth")
public class AuthController {

    private final AuthService authService;
    private final RegistrationService registrationService;
    private final PasswordService passwordService;

    @PostMapping("/register")
    @ResponseStatus(HttpStatus.CREATED)
    public void register(@RequestBody RegisterUserDTO registerUserDTO) throws MessagingException {
        registrationService.register(registerUserDTO);
    }

    @PostMapping("/login")
    @ResponseStatus(HttpStatus.OK)
    public LoginResponse login(@RequestBody LoginUserDTO loginUserDTO){
        return authService.login(loginUserDTO);
    }

    @PostMapping("/verify")
    @ResponseStatus(HttpStatus.OK)
    public void verifyUser(@RequestBody VerifyUserDTO verifyUserDTO){
        registrationService.verifyUser(verifyUserDTO);
    }

    @PostMapping("/resend")
    @ResponseStatus(HttpStatus.OK)
    public void resendVerificationCode(@RequestParam String email) throws MessagingException {
        registrationService.reenviarCodigoVerificacion(email);
    }

    @PostMapping("/change-password")
    @SecurityRequirement(name = "bearerAuth")
    @ResponseStatus(HttpStatus.OK)
    public void changePassword(@RequestBody ChangePasswordDTO dto, Principal principal){
        passwordService.cambiarPassword(principal.getName(),dto);
    }

    @PostMapping("/solicitar-reset-password")
    @ResponseStatus(HttpStatus.OK)
    public void solicitarResetPassword(@RequestParam String email) throws MessagingException {
        passwordService.solicitarResetPassword(email);
    }

    @PostMapping("/reset-password")
    @ResponseStatus(HttpStatus.OK)
    public void resetPassword(@RequestBody ResetPasswordDTO dto){
        passwordService.resetPassword(dto);
    }
}
